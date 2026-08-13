# Knowledge, Skills, and Results

## Knowledge and skills gained

**Inverted Index:**

- Understanding of the structure and role of the inverted index in
  optimizing search queries.
- Solid grasp of text preprocessing techniques: tokenization, normalization,
  stop-word removal, and handling special phrases (e.g. `"ma túy"`).
- Basic understanding of ranking algorithms such as TF-IDF and cosine
  similarity.

**MongoDB Sharded Cluster:**

- Understanding of the role of each component: shards, config servers, and
  mongos routers.
- Solid grasp of how to set up replica sets and sharding to ensure high
  availability and horizontal scaling.
- Understanding of how mongos routers distribute queries to balance load.

**Docker:**

- Creating and managing a custom Docker network to isolate containers.
- Deploying MongoDB containers with specific parameters (`--shardsvr`,
  `--configsvr`, `--replSet`).
- Using `docker exec` to inspect and configure running containers.

**Load balancing:** understanding the role of mongos routers in distributing
queries across shards.

**System analysis and design:** analyzing requirements and proposing an
architecture that integrates an inverted index with a MongoDB sharded
cluster.

## Results

**Search system architecture:**

- Successfully proposed 5 core components: Query Processing, Inverted Index
  Database, Index Worker, Database, and Cache.
- Ensured these components integrate with a MongoDB sharded cluster.

**MongoDB Sharded Cluster:**

- Successfully set up a cluster with:
  - 2 shards, each with a 3-node replica set.
  - 1 replica set for the config server, with 3 nodes.
  - 2 mongos routers for load balancing.
- The cluster runs stably in Docker on an isolated network.
- Connection string: `mongodb://localhost:27100,localhost:27200`.

**Performance:** faster query processing thanks to the inverted index and
sharding.

**Documentation:** detailed documentation of the cluster setup steps (see
[`mongodb-cluster-setup.md`](./mongodb-cluster-setup.md)).
