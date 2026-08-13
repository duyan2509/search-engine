#!/usr/bin/env bash
# One-time initialization of the MongoDB sharded cluster started by
# docker-compose.yml: initiates each replica set, then registers both
# shards with the router. Run after `docker compose up -d` once all
# containers are healthy.
set -euo pipefail

echo "Initiating config server replica set..."
docker exec mongo-config-server-1 mongosh --port 27017 --eval "
rs.initiate({
  _id: 'mongo-config-server-rs',
  members: [
    { _id: 0, host: 'mongo-config-server-1:27017' },
    { _id: 1, host: 'mongo-config-server-2:27017' },
    { _id: 2, host: 'mongo-config-server-3:27017' }
  ]
})"

echo "Initiating shard 1 replica set..."
docker exec mongo-shard1-1 mongosh --port 27017 --eval "
rs.initiate({
  _id: 'mongo-shard1-rs',
  members: [
    { _id: 0, host: 'mongo-shard1-1:27017' },
    { _id: 1, host: 'mongo-shard1-2:27017' },
    { _id: 2, host: 'mongo-shard1-3:27017' }
  ]
})"

echo "Initiating shard 2 replica set..."
docker exec mongo-shard2-1 mongosh --port 27017 --eval "
rs.initiate({
  _id: 'mongo-shard2-rs',
  members: [
    { _id: 0, host: 'mongo-shard2-1:27017' },
    { _id: 1, host: 'mongo-shard2-2:27017' },
    { _id: 2, host: 'mongo-shard2-3:27017' }
  ]
})"

echo "Waiting for replica sets to elect primaries..."
sleep 15

echo "Registering shards with mongos-router-1..."
docker exec mongos-router-1 mongosh --port 27017 --eval "
sh.addShard('mongo-shard1-rs/mongo-shard1-1:27017,mongo-shard1-2:27017,mongo-shard1-3:27017');
sh.addShard('mongo-shard2-rs/mongo-shard2-1:27017,mongo-shard2-2:27017,mongo-shard2-3:27017');
"

echo "Cluster status:"
docker exec mongos-router-1 mongosh --port 27017 --eval "sh.status()"
