# Inverted Index Storage: the Database Abstraction vs. Real Disk Formats

[`architecture.md`](./architecture.md) defines *Inverted Index Storage* as a
generic component, and [`mongodb-cluster-setup.md`](./mongodb-cluster-setup.md)
shows one way to back it with MongoDB. That's a deliberate simplification.
This doc spells out how the storage actually looks in a production search
engine (e.g. Lucene, which powers Elasticsearch/Solr), and why it differs
from "store postings as documents in a database."

## What a database gives you

Storing `{ "word1": [doc_id1, doc_id2], ... }` as documents in MongoDB (or
any general-purpose database) gets you, for free:

- Durable persistence and replication.
- Sharding / horizontal scaling (see `mongodb-cluster-setup.md`).
- A query language and driver ecosystem.

But MongoDB is itself just a layer on top of a real storage engine
(WiredTiger) that persists BSON documents to disk in *its own* general-purpose
format. It was not designed around the specific access pattern of an
inverted index — read a term's postings sequentially, intersect/union them
with other postings, and stop early when possible. That mismatch costs
space and query latency.

## What real search engines actually store on disk

Instead of rows/documents, a segment on disk is a small set of purpose-built
binary files:

### Term dictionary

A mapping from term → byte offset into the postings file, typically stored
as a sorted structure or a **finite state transducer (FST)** so that even
dictionaries with millions of terms fit in a small amount of memory and
support fast prefix/range lookups.

### Postings list

For each term, a sorted list of doc IDs, plus (depending on the ranking
model) term frequency and positions within each document. This is where
most of the size and speed work happens:

- **Delta encoding:** since doc IDs are stored sorted, only the *gaps*
  between consecutive IDs are stored (e.g. `[5, 9, 40]` → `[5, 4, 31]`).
  Gaps are usually much smaller numbers than raw IDs.
- **Variable-byte / integer compression:** small gap values are packed into
  as few bytes as possible (variable-byte encoding, PForDelta, or
  Roaring bitmaps for dense posting lists). This is the single biggest lever
  on index size — often an order of magnitude smaller than storing raw
  32/64-bit integers.
- **Skip lists:** every N postings, a "skip pointer" lets a query jump ahead
  without decoding every entry in between — critical for fast AND
  intersections between a rare term and a common one.

### Segments are immutable

A segment, once written, is never modified in place. New documents go into
new segments; deletes are recorded as a bitmask rather than rewriting the
segment. A background **merge** process periodically combines small segments
into larger ones and drops deleted entries. This trades some write
amplification for simple, lock-free concurrent reads and much simpler
compression (compression schemes generally assume the data won't change
once written).

## Where this project's design sits

| | This project (docs) | Real engine (e.g. Lucene) |
|---|---|---|
| Storage unit | MongoDB document per term | Binary postings file + FST term dictionary |
| Doc ID encoding | Plain JSON array of ints | Delta-encoded + compressed (var-byte / PForDelta / Roaring) |
| Fast AND/OR | Set intersection in application code (`inverted_index.py`) | Same idea, but skip lists let it avoid decoding full postings |
| Updates | Presumably in-place document update | New immutable segment + background merge |
| Scaling | MongoDB sharding | Segments distributed across shards/replicas at the search-engine layer (e.g. Elasticsearch shards) |

The database-backed design in this repo is a reasonable choice for a class
project: it's fast to build, and MongoDB's sharded cluster (see
`mongodb-cluster-setup.md`) gives horizontal scaling without writing a custom
storage engine. The tradeoff is real, though — at scale, a
purpose-built binary postings format on disk will be both smaller and
faster for the read pattern an inverted index actually needs.
