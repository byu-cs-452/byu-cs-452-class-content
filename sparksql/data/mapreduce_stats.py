# Written by Claude (Anthropic's AI model) for Professor Reynolds, CS 452, November 2026.
# Computes the numbers shown in the "MapReduce, Step by Step" animation (Part 2: eight machines).
"""Simulate a MapReduce word count on the Book of Mormon and report how many bytes exist at each step.

    python mapreduce_stats.py                 # 8 machines, bookOfMormon.txt next to this script
    python mapreduce_stats.py --machines 4
    python mapreduce_stats.py --file bible.txt --json

How it counts (a simplification of what Hadoop or Spark really store):
  - The Project Gutenberg license header and footer are removed; what's left is the book text.
  - Split: the text is cut into N equal byte ranges, each ending at a line break.
  - Map: words are lowercased and matched with [a-z']+. Each word becomes one "word<TAB>1<NEWLINE>" line.
  - Shuffle: a word goes to reducer crc32(word) mod N. (Hadoop uses Java's hashCode(), so the reducer
    that gets a given word differs, but some reducer always gets the very common words.)
  - Combine (optional step in real systems): each mapper sums its own words first, "word<TAB>count<NEWLINE>".
  - Reduce: each reducer writes one "word<TAB>count<NEWLINE>" line per distinct word it owns.
"""
import argparse
import collections
import json
import re
import zlib
from pathlib import Path

WORD = re.compile(r"[a-z']+")


def book_text(path):
    t = Path(path).read_text(encoding="utf-8-sig")
    start, end = t.find("*** START OF"), t.find("*** END OF")
    if start != -1 and end != -1:
        t = t[t.index("\n", start) + 1:end]
    return t.encode("utf-8")


def split(data, n):
    """Cut into n roughly equal byte ranges, each ending at a newline."""
    cuts, size = [0], len(data) // n
    for i in range(1, n):
        cuts.append(data.index(b"\n", i * size) + 1)
    cuts.append(len(data))
    return [data[cuts[i]:cuts[i + 1]] for i in range(n)]


def line_bytes(word, count):
    return len(word) + 1 + len(str(count)) + 1   # word, tab, count, newline


def run(path, n):
    data = book_text(path)
    owner = lambda w: zlib.crc32(w.encode()) % n
    total = collections.Counter()
    mappers, shuffle, shuffle_combined = [], [[0] * n for _ in range(n)], [[0] * n for _ in range(n)]
    for i, chunk in enumerate(split(data, n)):
        words = WORD.findall(chunk.decode("utf-8").lower())
        local = collections.Counter(words)
        total += local
        for w in words:
            shuffle[i][owner(w)] += line_bytes(w, 1)
        for w, c in local.items():
            shuffle_combined[i][owner(w)] += line_bytes(w, c)
        mappers.append({
            "input_bytes": len(chunk),
            "words": len(words),
            "map_output_bytes": sum(line_bytes(w, 1) for w in words),
            "combined_bytes": sum(line_bytes(w, c) for w, c in local.items()),
        })
    reducers = []
    for r in range(n):
        mine = {w: c for w, c in total.items() if owner(w) == r}
        reducers.append({
            "distinct_words": len(mine),
            "input_bytes": sum(shuffle[i][r] for i in range(n)),
            "input_bytes_with_combiner": sum(shuffle_combined[i][r] for i in range(n)),
            "output_bytes": sum(line_bytes(w, c) for w, c in mine.items()),
            "top_words": sorted(mine.items(), key=lambda x: -x[1])[:3],
        })
    return {
        "file": str(path), "machines": n, "input_bytes": len(data),
        "words": sum(total.values()), "distinct_words": len(total),
        "map_output_bytes": sum(m["map_output_bytes"] for m in mappers),
        "shuffle_bytes_with_combiner": sum(m["combined_bytes"] for m in mappers),
        "result_bytes": sum(r["output_bytes"] for r in reducers),
        "top_words": total.most_common(15),
        "mappers": mappers, "reducers": reducers,
    }


def kb(b):
    return f"{b / 1000:,.1f} KB"


def report(s):
    print(f"{s['file']}: {kb(s['input_bytes'])}, {s['words']:,} words, {s['distinct_words']:,} distinct, {s['machines']} machines\n")
    print("Mapper   input       map output   with combiner")
    for i, m in enumerate(s["mappers"], 1):
        print(f"{i:>6}   {kb(m['input_bytes']):>10}   {kb(m['map_output_bytes']):>10}   {kb(m['combined_bytes']):>10}")
    print("\nReducer  input       w/ combiner  output     distinct  top words")
    for i, r in enumerate(s["reducers"], 1):
        top = ", ".join(f"{w} {c:,}" for w, c in r["top_words"])
        print(f"{i:>7}  {kb(r['input_bytes']):>10}  {kb(r['input_bytes_with_combiner']):>10}  {kb(r['output_bytes']):>9}  {r['distinct_words']:>8}  {top}")
    print(f"\nTotals: input {kb(s['input_bytes'])} -> map output {kb(s['map_output_bytes'])}"
          f" -> shuffled {kb(s['map_output_bytes'])} ({kb(s['shuffle_bytes_with_combiner'])} with a combiner)"
          f" -> result {kb(s['result_bytes'])}")
    print("Most common:", ", ".join(f"{w} {c:,}" for w, c in s["top_words"][:10]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default=Path(__file__).with_name("bookOfMormon.txt"))
    ap.add_argument("--machines", type=int, default=8)
    ap.add_argument("--json", action="store_true", help="print everything as JSON")
    a = ap.parse_args()
    stats = run(a.file, a.machines)
    print(json.dumps(stats, indent=1)) if a.json else report(stats)
