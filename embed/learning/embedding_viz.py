"""
Embeddings Explorer - Interactive Embedding Visualization & Arithmetic

An educational tool to help students build intuition for embeddings through
hands-on exploration of semantic relationships in vector space.

Usage:
    python embedding_viz.py

Dependencies:
    pip install openai numpy matplotlib scikit-learn
"""

import json
import os
import subprocess
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536
CACHE_FILE = Path(__file__).parent / "embedding_cache.json"
OUTPUT_DIR = Path(__file__).parent / "output"

# Default path to the config file that holds the OpenAI API key.
# Override by setting the CONFIG_PATH environment variable.
DEFAULT_CONFIG_PATH = Path(r"C:\Users\mtr26\Desktop\repos\cs452\aisql\config.json")

# Pre-loaded word sets from the README
WORD_SETS = {
    "Gender & Royalty": ["King", "Queen", "Man", "Woman", "Prince", "Princess"],
    "Geography & Capitals": ["France", "Paris", "Germany", "Berlin", "Italy", "Rome"],
    "Comparatives": ["Big", "Bigger", "Biggest", "Small", "Smaller", "Smallest"],
    "Opposites": ["Hot", "Cold", "Happy", "Sad", "Fast", "Slow", "Light", "Dark"],
    "Professions": ["Doctor", "Nurse", "Teacher", "Student", "Chef", "Cook"],
    "Animals & Sounds": ["Dog", "Bark", "Cat", "Meow", "Cow", "Moo"],
}


# ---------------------------------------------------------------------------
# API Key Loading
# ---------------------------------------------------------------------------

def load_api_key() -> str:
    """Load OpenAI API key from environment variable or config.json."""
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key

    config_path = Path(os.environ.get("CONFIG_PATH", str(DEFAULT_CONFIG_PATH)))
    if config_path.exists():
        with open(config_path, "r") as f:
            data = json.load(f)
        key = data.get("openaiKey")
        if key:
            return key

    print("ERROR: No OpenAI API key found.")
    print("Set OPENAI_API_KEY env var, or ensure config.json exists at:")
    print(f"  {DEFAULT_CONFIG_PATH}")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Embedding Cache
# ---------------------------------------------------------------------------

def load_cache() -> dict[str, list[float]]:
    """Load cached embeddings from disk."""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_cache(cache: dict[str, list[float]]) -> None:
    """Save embeddings cache to disk."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


# ---------------------------------------------------------------------------
# Core Functions
# ---------------------------------------------------------------------------

def embed_words(words: list[str], client, cache: dict) -> dict[str, np.ndarray]:
    """
    Embed a list of words using OpenAI's text-embedding-3-small model.

    Returns a dict mapping each word (lowercase) to its numpy embedding vector.
    Uses a local cache to avoid redundant API calls.
    """
    result: dict[str, np.ndarray] = {}
    words_to_fetch: list[str] = []

    for w in words:
        key = w.strip().lower()
        if key in cache:
            result[key] = np.array(cache[key])
        else:
            words_to_fetch.append(w.strip())

    if words_to_fetch:
        print(f"  Fetching embeddings for {len(words_to_fetch)} new word(s)...")
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=words_to_fetch,
        )
        for item, word in zip(response.data, words_to_fetch):
            key = word.lower()
            vec = item.embedding
            cache[key] = vec
            result[key] = np.array(vec)
        save_cache(cache)
    else:
        print("  All words loaded from cache.")

    return result


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    dot = np.dot(vec1, vec2)
    norm = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    if norm == 0:
        return 0.0
    return float(dot / norm)


def vector_arithmetic(
    embeddings: dict[str, np.ndarray],
    positive: list[str],
    negative: list[str],
) -> np.ndarray:
    """
    Perform vector arithmetic: sum(positive) - sum(negative).

    Example: vector_arithmetic(emb, ["king", "woman"], ["man"])
             computes King - Man + Woman.
    """
    result = np.zeros(EMBEDDING_DIM)
    for w in positive:
        result += embeddings[w.lower()]
    for w in negative:
        result -= embeddings[w.lower()]
    return result


def find_closest(
    target: np.ndarray,
    embeddings: dict[str, np.ndarray],
    exclude: set[str] | None = None,
    top_n: int = 5,
) -> list[tuple[str, float]]:
    """Find the top-N most similar words to *target* by cosine similarity."""
    exclude = exclude or set()
    scored = []
    for word, vec in embeddings.items():
        if word in exclude:
            continue
        sim = cosine_similarity(target, vec)
        scored.append((word, sim))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]


# ---------------------------------------------------------------------------
# Visualization Helpers
# ---------------------------------------------------------------------------

_fig_counter = 0

def show_figure(fig, name: str) -> None:
    """Save figure as PNG to output/ and open with the default viewer."""
    global _fig_counter
    OUTPUT_DIR.mkdir(exist_ok=True)
    _fig_counter += 1
    path = OUTPUT_DIR / f"{name}_{_fig_counter}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved → {path}")
    os.startfile(path)


# ---------------------------------------------------------------------------
# Visualization Functions
# ---------------------------------------------------------------------------

def visualize_dimensions(embeddings: dict[str, np.ndarray], top_n: int = 15) -> None:
    """
    Color-coded dimension bars for each word.

    Shows the top-N dimensions (by variance across all words) as
    horizontal bar segments — highlighting where words differ most.
    """
    words = list(embeddings.keys())
    matrix = np.array([embeddings[w] for w in words])

    # Pick the top_n dimensions with highest variance across words
    variance = np.var(matrix, axis=0)
    top_dims = np.argsort(variance)[-top_n:][::-1]

    cmap = plt.cm.get_cmap("tab20", top_n)
    fig, ax = plt.subplots(figsize=(14, max(4, len(words) * 0.6)))

    for i, word in enumerate(words):
        left = 0.0
        for j, dim_idx in enumerate(top_dims):
            val = abs(matrix[i, dim_idx])
            ax.barh(i, val, left=left, color=cmap(j), edgecolor="none", height=0.6)
            left += val

    ax.set_yticks(range(len(words)))
    ax.set_yticklabels(words, fontsize=11)
    ax.invert_yaxis()
    ax.set_xlabel("Cumulative dimension magnitude")
    ax.set_title(f"Top {top_n} Most Variable Dimensions")
    plt.tight_layout()
    show_figure(fig, "dimension_bars")


def similarity_heatmap(embeddings: dict[str, np.ndarray]) -> None:
    """Display a pairwise cosine-similarity heatmap."""
    words = list(embeddings.keys())
    n = len(words)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i, j] = cosine_similarity(
                embeddings[words[i]], embeddings[words[j]]
            )

    fig, ax = plt.subplots(figsize=(max(6, n * 0.8), max(5, n * 0.7)))
    im = ax.imshow(matrix, cmap="RdYlGn", vmin=-1, vmax=1)
    ax.set_xticks(range(n))
    ax.set_xticklabels(words, rotation=45, ha="right", fontsize=10)
    ax.set_yticks(range(n))
    ax.set_yticklabels(words, fontsize=10)

    # Annotate cells
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", fontsize=8)

    plt.colorbar(im, ax=ax, label="Cosine Similarity")
    ax.set_title("Pairwise Cosine Similarity")
    plt.tight_layout()
    show_figure(fig, "similarity_heatmap")


def plot_2d(embeddings: dict[str, np.ndarray], method: str = "pca") -> None:
    """
    Reduce embeddings to 2D via PCA (default) or t-SNE, then scatter-plot.
    """
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE

    words = list(embeddings.keys())
    matrix = np.array([embeddings[w] for w in words])

    if method == "tsne" and len(words) >= 4:
        perplexity = min(30, len(words) - 1)
        reducer = TSNE(n_components=2, perplexity=perplexity, random_state=42)
    else:
        reducer = PCA(n_components=2)

    coords = reducer.fit_transform(matrix)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(coords[:, 0], coords[:, 1], s=120, c="steelblue", edgecolors="white", zorder=5)
    for i, word in enumerate(words):
        ax.annotate(
            word,
            (coords[i, 0], coords[i, 1]),
            textcoords="offset points",
            xytext=(8, 6),
            fontsize=11,
            fontweight="bold",
        )
    ax.set_title(f"2D Projection ({method.upper()})")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    show_figure(fig, f"scatter_2d_{method}")


def plot_3d(embeddings: dict[str, np.ndarray]) -> None:
    """Reduce embeddings to 3D via PCA and show an interactive 3D scatter plot."""
    from sklearn.decomposition import PCA

    words = list(embeddings.keys())
    matrix = np.array([embeddings[w] for w in words])

    coords = PCA(n_components=3).fit_transform(matrix)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], s=120, c="steelblue", edgecolors="white")
    for i, word in enumerate(words):
        ax.text(coords[i, 0], coords[i, 1], coords[i, 2], f"  {word}", fontsize=10, fontweight="bold")
    ax.set_title("3D Projection (PCA)")
    plt.tight_layout()
    show_figure(fig, "scatter_3d")


# ---------------------------------------------------------------------------
# Interactive CLI
# ---------------------------------------------------------------------------

def print_menu() -> None:
    print("\n" + "=" * 50)
    print("  Embeddings Explorer")
    print("=" * 50)
    print("  1) Embed words")
    print("  2) Embed a pre-loaded word set")
    print("  3) Vector arithmetic  (A - B + C ≈ ?)")
    print("  4) Show similarity between two words")
    print("  5) Similarity heatmap")
    print("  6) Dimension bars visualization")
    print("  7) 2D scatter plot (PCA)")
    print("  8) 3D scatter plot (PCA)")
    print("  9) List embedded words")
    print("  0) Quit")
    print("=" * 50)


def main() -> None:
    from openai import OpenAI

    api_key = load_api_key()
    client = OpenAI(api_key=api_key)
    cache = load_cache()
    embeddings: dict[str, np.ndarray] = {}

    # Restore any cached embeddings into the active session
    for word, vec in cache.items():
        embeddings[word] = np.array(vec)

    print("\nWelcome to the Embeddings Explorer!")
    print(f"Model: {EMBEDDING_MODEL}  |  Dimensions: {EMBEDDING_DIM}")
    print(f"Cache: {len(cache)} word(s) loaded from {CACHE_FILE.name}")

    while True:
        print_menu()
        choice = input("\nChoose an option: ").strip()

        # ---- 1. Embed custom words ----
        if choice == "1":
            raw = input("Enter words (comma-separated): ")
            words = [w.strip() for w in raw.split(",") if w.strip()]
            if words:
                new_embs = embed_words(words, client, cache)
                embeddings.update(new_embs)
                print(f"  ✓ {len(new_embs)} word(s) embedded. Total: {len(embeddings)}")

        # ---- 2. Load a pre-built word set ----
        elif choice == "2":
            print("\nAvailable word sets:")
            set_names = list(WORD_SETS.keys())
            for idx, name in enumerate(set_names, 1):
                print(f"  {idx}) {name}: {', '.join(WORD_SETS[name])}")
            sel = input("Pick a set (number): ").strip()
            try:
                name = set_names[int(sel) - 1]
                new_embs = embed_words(WORD_SETS[name], client, cache)
                embeddings.update(new_embs)
                print(f"  ✓ '{name}' loaded. Total: {len(embeddings)}")
            except (ValueError, IndexError):
                print("  Invalid selection.")

        # ---- 3. Vector arithmetic ----
        elif choice == "3":
            if len(embeddings) < 3:
                print("  Need at least 3 embedded words. Embed some first!")
                continue
            print("  Compute:  A - B + C ≈ ?")
            a = input("  Word A: ").strip().lower()
            b = input("  Word B: ").strip().lower()
            c = input("  Word C: ").strip().lower()
            if all(w in embeddings for w in [a, b, c]):
                target = vector_arithmetic(embeddings, [a, c], [b])
                closest = find_closest(target, embeddings, exclude={a, b, c})
                print(f"\n  {a} - {b} + {c} ≈")
                for word, sim in closest:
                    print(f"    {word:>15s}  (similarity: {sim:.4f})")
            else:
                missing = [w for w in [a, b, c] if w not in embeddings]
                print(f"  Words not embedded yet: {', '.join(missing)}")

        # ---- 4. Pairwise similarity ----
        elif choice == "4":
            w1 = input("  First word: ").strip().lower()
            w2 = input("  Second word: ").strip().lower()
            if w1 in embeddings and w2 in embeddings:
                sim = cosine_similarity(embeddings[w1], embeddings[w2])
                print(f"\n  cosine_similarity({w1}, {w2}) = {sim:.4f}")
            else:
                missing = [w for w in [w1, w2] if w not in embeddings]
                print(f"  Words not embedded yet: {', '.join(missing)}")

        # ---- 5. Heatmap ----
        elif choice == "5":
            if len(embeddings) < 2:
                print("  Need at least 2 words.")
                continue
            similarity_heatmap(embeddings)

        # ---- 6. Dimension bars ----
        elif choice == "6":
            if not embeddings:
                print("  No words embedded yet.")
                continue
            visualize_dimensions(embeddings)

        # ---- 7. 2D plot ----
        elif choice == "7":
            if len(embeddings) < 3:
                print("  Need at least 3 words for 2D projection.")
                continue
            method = input("  Method (pca/tsne) [pca]: ").strip().lower() or "pca"
            plot_2d(embeddings, method=method)

        # ---- 8. 3D plot ----
        elif choice == "8":
            if len(embeddings) < 4:
                print("  Need at least 4 words for 3D projection.")
                continue
            plot_3d(embeddings)

        # ---- 9. List words ----
        elif choice == "9":
            if embeddings:
                print(f"\n  {len(embeddings)} embedded word(s):")
                for w in sorted(embeddings.keys()):
                    vals = ", ".join(f"{v:.4f}" for v in embeddings[w][:10])
                    preview = vals[:30] + "..." if len(vals) > 30 else vals
                    print(f"    • {w:20s} [{preview}]")
            else:
                print("  No words embedded yet.")

        # ---- 0. Quit ----
        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("  Invalid choice, try again.")


if __name__ == "__main__":
    main()
