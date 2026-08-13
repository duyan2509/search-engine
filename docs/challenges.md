# Challenges

**Understanding the Inverted Index:**

- Difficulty grasping TF-IDF and cosine similarity due to lack of hands-on
  experience.
- Processing Vietnamese text (e.g. the phrase `"ma túy"`) requires special
  handling.

**Setting up the MongoDB Sharded Cluster:**

- Unfamiliarity with replica set and sharding configuration led to early
  errors.
- Difficulty setting up the Docker network so containers could communicate
  correctly.
- Synchronizing config servers, shards, and mongos routers required a lot of
  trial and error.

**Limited hands-on implementation:** components like Cache and load
balancing were only studied at a theoretical level and not actually
implemented.

**Architecture integration:** integrating the inverted index with the
MongoDB sharded cluster requires careful consideration of data storage and
querying.
