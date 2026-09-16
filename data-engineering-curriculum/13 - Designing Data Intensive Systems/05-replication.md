Distributed data section

What happens if multiple machines are involved in storage and retrieval of data?

There are various reasons why you might want to distribute a database across multiple machines: 
- scalability
- fault tolerance / high availability 
- low latency

## Scaling to higher load
**Shared-memory architecture**: Many CPUs, many RAM chips, and many disks can be joined together under `one operating system`, and a fast interconnect allows any CPU to access any part of the memory or disk. All the components can be treated as a single machine. Problem: the cost grows faster than linearly, and a machine twice the size cannot necessarily handle twice the load. Limited fault tolerance, with single geographic location. 

**Shared-disk architecture**: Uses several machines with independent CPUs and RAM, but `stores data on an array of disks that is shared between the machines`, which are connected via a fast network. It is used for some data warehousing workloads, but contention and the overhead of locking limit the scalability of the shared-disk approach. 

**Shared-nothing architecture**: Each machine or virtual machine running the database software is called a node. `Each node uses its CPUs, RAM, and disks independently`. Any coordination between nodes is done at the software level, using a conventional network. Can distribute data across multiple geographic regions, go get better fault tolerance and increased availability. Can be very powerful, but incurs additional complexity for applications and sometimes limits the expressiveness of the data models you can use. 

Two common ways data is distributed across multiple nodes, and they often go together:
- `Replication`: Keep a copy of the same data on several different nodes, potentially in different locations. Provides redundancy: if some nodes are unavailable, the data can still be served from the remaining nodes. Replication can also help improve performance. 
- `Partitioning`: Split a big database into smaller subsets (partitions), different partitions can be assigned to different nodes (sharding). 

# 5. Replication
Replication: keeping a copy of the same data on multiple machines that are connected via a network. It reduces latency, increases availability, and increase read throughput. 

`3 popular algorithms for replicating changes between nodes: single-leader, multi-leader, and leaderless replication.` Almost all distributed databases use one of these three approaches.

Each node that stores a copy of the database is called a `replica`. Every write to the database needs to be processed by every replica, so they have same data. 

Leader-based replication: One of the replicas is designated the leader - `every write to the db has to go through the leader`, and it writes new data to its local storage. This leader also send the data change to all of its followers (other replicas), so followers can update their local copy. `Clients can query any replicas, but only leader takes writes.` It is used in PostgreSQL, MySQL, Oracle, SQL Server, MongoDB, Kafka, ...

Synchronous replication: Advantage: follower is guaranteed to have up-to-date data consistent with the leader, so data is still available on follower if leader fails. Disadvantage: if sync follower is unavailable, the write halts. 

Asynchronous replication: Advantage: leader can still process writes when follower not available. Disadvantage: if leader fails and unrecoverable, the writes that are not synced yet are lost. 

## Achieve high availability with leader-based replication
Follower failure: on local disk, each follower keeps a log of the data changes it has received from the leader. After it is back, it checks the log and get missed data changes from the leader. 

Leader failure: Using failover - promote a follower to be the new leader, clients reconfigured to send writes to the new leader, other follower start to take data changes from the new leader. It can be manual or automatic. 

In certain fault scenarios, it could happen that two nodes both believe that they are the leader (split brain), and it can cause lost or corrupted data. 

## Implement Replication Logs
- Statement-based replication: The leader logs every write request that it executes and sends this statement log to its followers. Potential issues: nondeterministic statement, order of execution. Used by VoltDB. 
- Write-ahead log (WAL) shipping: Every write is originally appended to a log, this exact same log can be used to build a replica on another node. Potential issues: this log is low level (which bytes changed on the which disk blocks), so coupled to the storage engine. Cannot handle it if storage format of the db changes, so requires same version of db software on all nodes. Need downtime to update db versions, so no rolling upgrade possible. Used by PostgreSQL and Oracle. 
- Logical (row-based) log replication: decouple physical storage engine and log using logical log. Allows for different storage formats on different nodes, and hence rolling upgrade. MySQL binlog when using row-based replication can do change data capture, and can send these changes to DWH for analysis. 
- Trigger-based replication: Oracle GoldenGate allow app to read the database log to do custom replication. Alternative is triggers and SPs. 

## Replication lag
If an application reads from an asynchronous follower, it may see outdated information if the follower has fallen behind. The followers will eventually catch up with the leader (eventual consistency). Problems and solutions:
- When user read their own writes, will need `read-after-write consistency`. Solution: read user editable contents from leader only; track last update and read from leader only if within 1 min of that; read from follower only if it's at least up to date with the last write timestamp
- User may see things moving backward in time due to reading from different replicas, so we need `monotonic reads`. This guarantee is stronger than eventual consistency. Solution: each user always read from the same replica. 
- Violation of causal dependency due to different replication lag for different writes, so we need `consistent prefix reads guarantee`, which maintains order in writes. It is a problem with partitioned dbs. Solution: make causal writes into the same shard. 

Solutions for Replication lag: Database can provide stronger guarantees so that the application code can be simpler. 

## Multi-Leader Replication
With multi-leader replication, >= 2 nodes can accept writes, and forward the writes to other nodes. So that if you have multiple datacenters, you can have a leader in each datacenter, instead of only have one leader in one of the datacenters. This allow you to tolerate failure of an entire datacenter, and allow writes to be closer to your users, and tolerant network problems. In each datacenter, regular leader-follower replication is used; while between datacenters, each datacenter's leader replicates its own changes to the leaders in other datacenters. Downside: multi-leader replication is a tricky thing to get right. Use cases also include clients with offline operation, and collaborative editing. 

### Handling write conflicts
`Multi-leader replication requires conflict resolution` (different users applied different changes to the same item, accepted by different leaders, the conflict is detected when the changes are async replicated). Because it is async, it may be too late to ask the user to resolve the conflict. 
- Avoid conflicts: ensure all writes for a particular record go through the same leader
- Converge conflicts: last write wins, etc
- Custom logic: use application code with custom logic to resolve conflicts. on write / on read

### Multi-Leader Replication Topologies
It is the communication paths along which writes are propagated from one node to another. 
- all-to-all
- circular
- star

## Leaderless Replication
Allowing any replica to directly accept writes from clients. Examples: Dynamo style dbs: Riak, Cassandra, and Voldemort. Write requests are sent to all notes, and read requests are also sent to all nodes. In case a node has stale values, version numbers are used to determine which value is newer. If stale data are detected, "Read repair" mechanism will writes newer value to this node. Additionally, Anti-entropy process can update stale vals in the background. Uses quorum read and writes. 

Dynamo-style databases are generally optimized for use cases that can tolerate eventual consistency. The parameters w and r allow you to adjust the probability of stale values being read, but it’s wise to not take them as absolute guarantees.

For conflict resolution, last-write-wins may cause data loss. 

Two operations are `concurrent` if neither happens before the other (i.e., neither knows about the other). Thus, whenever you have two operations A and B, there are three possibilities: either A happened before B, or B happened before A, or A and B are concurrent. We need to tell whether two operations are concurrent or not. If one operation happened before another, the later operation should overwrite the earlier operation, but if the operations are concurrent, we have a conflict that needs to be resolved.

`Version vectors` (version number per replica per key) can be used to distinguish overwrites and concurrent writes. The application can use this to merge siblings. 
