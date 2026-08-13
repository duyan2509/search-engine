# Simple Search Engine

A learning project exploring the core building blocks of a search engine:
web crawling, text preprocessing, inverted indexing, and vector space
retrieval, along with a proposed architecture for scaling it out.

## Documentation

- [`architecture.md`](./docs/architecture.md) — why an inverted index, and
  the proposed 5-component system architecture (Query Processing, Inverted
  Index Storage, Index Worker, Database, Cache).
- [`preprocessing.md`](./docs/preprocessing.md) — the text preprocessing
  pipeline (tokenization, normalization, stemming/lemmatization, stop-word
  removal) and where it fits in the architecture.
- [`index-storage-internals.md`](./docs/index-storage-internals.md) — how the
  database-backed storage in this project compares to the compressed,
  byte-level postings format a production search engine actually persists to
  disk.
- [`mongodb-cluster-setup.md`](./docs/mongodb-cluster-setup.md) — setting up
  a MongoDB Sharded Cluster (via `docker-compose.yml` or step-by-step with
  Docker) for horizontal scaling.
- [`knowledge-and-results.md`](./docs/knowledge-and-results.md) — knowledge
  and skills gained, and the results achieved.
- [`challenges.md`](./docs/challenges.md) — challenges encountered along the
  way.
