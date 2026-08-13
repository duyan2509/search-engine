# Simple Search Engine

A learning project exploring the core building blocks of a search engine:
web crawling, text preprocessing, inverted indexing, and vector space
retrieval.

## Project structure

```
search-engine/
├── web-spidering/
│   ├── web_spider.py              # BFS crawler storing pages into SQLite
│   └── crawled_pages.db           # SQLite DB of crawled pages
└── information-retrieval/
    ├── inverted_index.py          # Inverted index build + AND-query search
    ├── vector_space_retrieval.py  # TF-IDF + cosine similarity ranking
    ├── lemmatization_tokenization.py  # NLTK tokenization + lemmatization
    ├── stemming.py                # Porter stemming demo
    └── stopwords_remove.py        # NLTK stopword removal demo
```

## Modules

### Web Spider (`web-spidering/web_spider.py`)

A simple breadth-first crawler:

- Starts from a seed URL and follows `<a>` links up to `max_pages`.
- Skips already-visited URLs and in-page anchors (`#...`).
- Persists each crawled page's URL and raw HTML into a local SQLite database
  (`crawled_pages.db`).

### Inverted Index (`information-retrieval/inverted_index.py`)

- Builds a mapping of `term -> {doc_id: [positions]}` from a set of
  documents.
- Supports keyword search that intersects document sets across all query
  terms (AND semantics) and returns matching documents with term positions.

### Vector Space Retrieval (`information-retrieval/vector_space_retrieval.py`)

- Computes TF-IDF vectors for each document in a small in-memory corpus.
- Ranks documents for a query using cosine similarity between the query
  vector and each document vector.

### Text preprocessing demos

- `lemmatization_tokenization.py` — tokenizes a sentence with NLTK and
  lemmatizes each word using `WordNetLemmatizer`.
- `stemming.py` — stems a list of words using the Porter stemming algorithm.
- `stopwords_remove.py` — tokenizes text and filters out English stopwords.

## Requirements

- Python 3
- `requests`
- `beautifulsoup4`
- `nltk` (with the `punkt`, `punkt_tab`, `stopwords`, and `wordnet` corpora
  downloaded)

Install dependencies:

```bash
pip install requests beautifulsoup4 nltk
```

## Running the demos

Each script is self-contained and can be run directly, e.g.:

```bash
python search-engine/information-retrieval/inverted_index.py
python search-engine/information-retrieval/vector_space_retrieval.py
python search-engine/information-retrieval/lemmatization_tokenization.py
python search-engine/information-retrieval/stemming.py
python search-engine/information-retrieval/stopwords_remove.py
python search-engine/web-spidering/web_spider.py
```

## Documentation

The `docs/` folder covers the design behind this prototype in more depth:

- [`architecture.md`](./docs/architecture.md) — why an inverted index, and
  the proposed 5-component system architecture (Query Processing, Inverted
  Index Database, Index Worker, Database, Cache).
- [`preprocessing.md`](./docs/preprocessing.md) — the text preprocessing
  pipeline (tokenization, normalization, stemming/lemmatization, stop-word
  removal) and where it fits in the architecture.
- [`mongodb-cluster-setup.md`](./docs/mongodb-cluster-setup.md) — step-by-step
  setup of a MongoDB Sharded Cluster with Docker (2 shards × 3-node replica
  sets, a 3-node config server replica set, 2 `mongos` routers) for
  horizontal scaling.
- [`index-storage-internals.md`](./docs/index-storage-internals.md) — how the
  database-backed storage in this project compares to the compressed,
  byte-level postings format a production search engine actually persists to
  disk.
- [`knowledge-and-results.md`](./docs/knowledge-and-results.md) — knowledge
  and skills gained, and the results achieved.
- [`challenges.md`](./docs/challenges.md) — challenges encountered along the
  way.

## Status

This is an early-stage prototype. Components like caching and load balancing
are documented at the design level but not yet implemented in code.
