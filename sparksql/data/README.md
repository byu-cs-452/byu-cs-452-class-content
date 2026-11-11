# Text data for the Spark notebooks

Our own copies, so class doesn't depend on archive.org or gutenberg.org being up.

| File | Source |
|---|---|
| `bookOfMormon.txt` | Project Gutenberg eBook #17, https://www.gutenberg.org/ebooks/17 |
| `bible.txt` | Project Gutenberg eBook #10 (King James Version), https://www.gutenberg.org/ebooks/10 |

Both are public domain and include the Project Gutenberg license text. Notebooks download them with:

```
!curl -L https://raw.githubusercontent.com/byu-cs-452/byu-cs-452-class-content/main/sparksql/data/bookOfMormon.txt > bookOfMormon.txt
!curl -L https://raw.githubusercontent.com/byu-cs-452/byu-cs-452-class-content/main/sparksql/data/bible.txt > bible.txt
```

## mapreduce_stats.py

Simulates a MapReduce word count on 8 machines (`--machines N` to change) and prints how many bytes exist
at each step: input chunks, map output, shuffle (with and without a combiner) and reduce output. These are
the numbers in the "MapReduce, Step by Step" animation. Run `python mapreduce_stats.py`; `--help` explains
how sizes are counted.
