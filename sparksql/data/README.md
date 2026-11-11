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
