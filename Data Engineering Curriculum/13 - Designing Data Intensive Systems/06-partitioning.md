# 6. Partitioning
For very large datasets or very high query throughput, to get better scalability, we need to break the data up into partitions (sharding). Different partitions can be placed on different nodes in a shared-nothing cluster, so a large dataset can be distributed across many disks, and the query load can be distributed across many processors.

Normally, each piece of data (record/row/document) belongs to exactly one partition. A node may store more than one partition.

Partitioning is usually combined with replication so that copies of each partition are stored on multiple nodes. If leader-follower replication is used, each partition’s leader is assigned to one node, and its followers are assigned to other nodes. Each node may be the leader for some partitions and a follower for other partitions. The choice of partitioning scheme is mostly independent of the choice of replication scheme. 

## Partitioning of Key-Value data
Our goal with partitioning is to spread the data and the query load evenly across nodes. The presence of skew makes partitioning much less effective.
- Partition by key range. The partition boundaries can be chosen manually, or automatically by the db. Within each partition, keys can be kept in sorted order (easy for range scans). However, certain access patterns can cause hot spots. 
- Partition by hash of key. Used to avoid skew and hot spots. Assign each partition a range of hashes. Cannot do efficient range queries - and range query has to be sent to all partitions. Cassandra combines both ways using compound primary key. 

Partition by hash of key can help reduce hot spots, but it can’t avoid them entirely, such as when a celebrity makes a tweet. For now, it is the responsibility of application to reduce the skew. 

## Partitioning of Secondary Indexes
Document-based partitioning: each partition maintains its own secondary indexes, covering only the documents in that partition. Querying a partitioned database is  known as scatter/ gather. Prone to tail latency amplification. Used by MongoDB, Riak, Cassandra, Elasticsearch, SolrCloud and VoltDB. 

Term-based partitioning: construct a global index that covers data in all partitions, this global index is also partitioned. Makes read more efficient, but writes are slower. In practice, updates to global secondary indexes are often async. 

## Rebalancing Partitions
`Rebalancing`: moving load from one node in the cluster to another.
- Fixed number of partitions: create many more partitions than there are nodes, and assign several partitions to each node. When a new node is added, it grabs a few partitions from each existing nodes. Used in Riak, Elasticsearch, Couchbase and Voldemort. 
- Dynamic partitioning: When a partition grows to exceed a configured size, it is then divided into two partitions; shrinked partitions can also be merged into one. So the number of partitions adapts to the total data volume. Used in HBase and RethinkDB. 
- Fixed number of partitions per node. Used by Cassandra and Ketama. 

Couchbase, Riak, and Voldemort generate a suggested partition assignment automatically, but require an administrator to commit it before it takes effect. It can be a good thing to have a human in the loop for rebalancing. It’s slower than a fully automatic process, but it can help prevent operational surprises.

Request routing (service discovery) - Many distributed data systems (Espresso, HBase, SolrCloud, Kafka) rely on a separate coordination service such as ZooKeeper to keep track of this cluster metadata. Each node registers itself in ZooKeeper, and ZooKeeper maintains the authoritative mapping of partitions to nodes. Cassandra and Riak use a gossip protocol among the nodes to disseminate any changes in cluster state, which avoids the dependency on an external coordination service such as ZooKeeper.

The MPP query optimizer (for analytics) breaks this complex query into a number of execution stages and partitions, many of which can be executed in parallel on different nodes of the database cluster. Queries that involve scanning over large parts of the dataset particularly benefit from such parallel execution.






