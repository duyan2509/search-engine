# Architecture

## Why an Inverted Index

An inverted index is a mapping from a term to the list of documents that
contain it. It allows fast lookup of relevant documents by keyword, instead
of scanning the entire database. Example:

```json
{
  "word1": [doc_id1, doc_id2],
  "word2": [doc_id2, doc_id3],
  ...
}
```

Building it requires a preprocessing pipeline over the raw text: tokenization,
normalization, stop-word removal, and merging of special phrases. See
[`preprocessing.md`](./preprocessing.md) for details on that pipeline.

## Proposed system components

The system is organized into 5 main components, aimed at keeping search
efficient and scalable.

### Query Processing

**Functions:**

- **Preprocess the user query:**
  - **Tokenization:** split the query into words/phrases.
    Example: `"tìm kiếm thông tin"` → `["tìm", "kiếm", "thông", "tin"]`.
  - **Normalization:**
    - Lowercasing: `"TÌM KIẾM"` → `"tìm kiếm"`.
    - Stemming/lemmatization: `"tìm kiếm"` → `"tìm"`.
    - Stop-word removal: drop words such as `"và"`, `"của"`, `"là"`
      ("and", "of", "is").
    - Merge special phrases: `"ma túy"` → `"ma_túy"`.
  - Turn the query into a normalized set of keywords to search the inverted
    index with.
- **Query the Inverted Index Storage:** for each processed keyword, get the
  corresponding list of `doc_id`s, then perform an intersection (AND) or
  union (OR) over the lists depending on the query type.
- **Query the source Database:** fetch the full content of the resulting
  `doc_id`s to return the final result.

**Role:** ensure the user query is processed quickly and returns accurate
results.

### Inverted Index Storage

**Structure:**

```json
{
  "word1": [doc_id1, doc_id2],
  "word2": [doc_id2, doc_id3],
  ...
}
```

**Functions:** store the inverted index, mapping keywords to the documents
that contain them, optimized for fast keyword lookup.

**Role:** the core component for search performance. This is a storage
abstraction, not a specific product — at a high level it can be backed by
MongoDB (see [`mongodb-cluster-setup.md`](./mongodb-cluster-setup.md)), any
other database, or a custom format; ultimately, whatever is chosen still
comes down to structures persisted on disk. See
[`index-storage-internals.md`](./index-storage-internals.md) for how a
production search engine stores this on disk versus the database-backed
approach used here.

### Index Worker

**Functions:**

- Read documents from the source database.
- Preprocess them (tokenization, stop-word filtering, normalization).
- Update the Inverted Index Storage: for each keyword, add the `doc_id` to
  the related list if it isn't already present.

**Role:** keep the inverted index up to date, either in real time or on a
schedule.

### Database (original data source)

**Function:** store all text content, documents, legal texts, or other raw
data.

**Role:** provide the source data for the system to process and return
results from.

### Cache

**Function:** store popular queries or frequently accessed data from the
Inverted Index Storage and the source Database.

**Role:** reduce load and speed up responses for repeated queries.

## Component diagram

```
                      ┌───────┐
                      │ Cache │
                      └───┬───┘
                          │ read
                          ▲
 user query   ┌──────────────────┐  read   ┌─────────────────────┐  write   ┌──────────────┐
──────────────▶│  Query Processing │───────▶│ Inverted Index      │◀─────────│ Index Worker │
              └─────────┬────────┘         │ Database            │          └──────┬───────┘
                        │ read              └─────────────────────┘                 │ read
                        │                                                            ▼
                        │                                              ┌──────────────────┐
                        └─────────────────────────────────────────────▶│     Database      │
                                                                        └──────────────────┘
```

For one possible horizontal-scaling backend behind the *Inverted Index
Storage* and *Database* boxes, see
[`mongodb-cluster-setup.md`](./mongodb-cluster-setup.md).
