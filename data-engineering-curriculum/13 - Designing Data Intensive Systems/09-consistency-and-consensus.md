# 9. Consistency and Consensus
Algorithms and protocols for building fault-tolerant distributed systems.

Consensus: getting all of the nodes to agree on something.

For a database with single-leader replication, if two nodes both believe that they are the leader, that situation is called `split brain`, and it often leads to data loss.

Most replicated databases provide at least eventual consistency, which means that if you stop writing to the database and wait for some unspecified length of time, then eventually all read requests will return the same value. In this case, if you write a value and then immediately read it again, there is no guarantee that you will see the value you just wrote, because the read may be routed to a different replica. 

Systems with stronger guarantees may have worse performance or be less fault-tolerant than systems with weaker guarantees. Nevertheless, stronger guarantees can be appealing because they are easier to use correctly.

## Linearizability
Make a system appear as if there were only one copy of the data, and all operations on it are atomic. Therefore, even though there may be multiple replicas in reality, the application does not need to worry about them.

Maintaining the illusion of a single copy of the data means guaranteeing that the value read is the most recent, up-to-date value, and doesn't come from a stale cache or replica.

A system that uses single-leader replication needs to ensure that there is indeed only one leader, not several (split brain). One way of electing a leader is to use a lock. No matter how this lock is implemented, it must be linearizable: all nodes must agree which node owns the lock.

Coordination services like Apache ZooKeeper and etcd are often used to implement distributed locks and leader election.

If you want to enforce unique constraint as the data is written (such that if two people try to concurrently create a user or a file with the same name, one of them will be returned an error), you need linearizability. Similar issues arise if you want to ensure that a bank account balance never goes negative, or that you don't sell more items than you have in stock in the warehouse, or that two people don't concurrently book the same seat on a flight or in a theater.

Implement linearizable systems: 
- `Consensus algorithms can implement linearizable storage safely`. This is how ZooKeeper and etcd work. 
- Systems with multi-leader replication are generally not linearizable, because they concurrently process writes on multiple nodes and asynchronously replicate them to other nodes.
- Leaderless replication is probably not linearizable, considering network delays and clock skew. 

Linearizability is slow  -  and this is true all the time, not only during a network fault.

## Ordering Guarantees
There are deep connections between ordering, linearizability, and consensus.

A total order allows any two elements to be compared. `In a linearizable system, we have a total order of operations.` Causality defines a partial order, not a total order. 

Causal consistency is the strongest possible consistency model that does not slow down due to network delays, and remains available in the face of network failures. 

The key idea about `Lamport timestamps`, which makes them consistent with causality, is the following: every node and every client keeps track of `the maximum counter value it has seen so far`, and includes that maximum on every request. When a node receives a request or response with a maximum counter value greater than its own counter value, it immediately increases its own counter to that maximum. `Lamport timestamps always enforce a total ordering.`

Problem: The problem here is that the total order of operations only emerges after you have collected all of the operations. If another node has generated some operations, but you don't yet know what they are, you cannot construct the final ordering of operations: the unknown operations from the other node may need to be inserted at various positions in the total order. `When a node has just received a request from a user to create a username, and needs to decide right now whether the request should succeed or fail. At that moment, the node does not know whether another node is concurrently in the process of creating an account with the same username, and what timestamp that other node may assign to the operation.`

To conclude: `in order to implement something like a uniqueness constraint for usernames, it's not sufficient to have a total ordering of operations - you also need to know when that order is finalized.`

`Total Order Broadcast`/atomic broadcast: Usually described as a protocol for exchanging messages between nodes. It must ensure that the reliability (no messages are lost) and ordering properties (messages are delivered to the every node in the same order) are always satisfied, even if a node or the network is faulty.

Consensus services such as ZooKeeper and etcd implement total order broadcast. 

`Total order broadcast is asynchronous`: messages are guaranteed to be delivered reliably in a fixed order, but there is no guarantee about when a message will be delivered (so one recipient may lag behind the others). By contrast, linearizability is a recency guarantee: a read is guaranteed to see the latest value written.

A `linearizable compare-and-set register` and `total order broadcast` are both equivalent to `consensus`. 

## Distributed Transactions and Consensus
- Leader election: Consensus is important to avoid a bad failover, resulting in a split brain situation in which two nodes both believe themselves to be the leader. 
- Atomic commit: In a database that supports transactions spanning several nodes or partitions, we have the problem that a transaction may fail on some nodes but succeed on others. If we want to maintain transaction atomicity, we have to get all nodes to agree on the outcome of the transaction: either they all abort/roll back (if anything goes wrong) or they all commit (if nothing goes wrong). This instance of consensus is known as the atomic commit problem.

`Distributed systems can usually achieve consensus in practice.`

`Two-phase commit` is an algorithm for achieving atomic transaction commit across multiple nodes - i.e., to ensure that either all nodes commit or all nodes abort.

2PC uses a new component that does not normally appear in single-node transactions: a coordinator (also known as transaction manager). When the application is ready to commit, the coordinator begins phase 1: it sends a prepare request to each of the nodes, asking them whether they are able to commit. The coordinator then tracks the responses from the participants. If one of the participants or the network fails during 2PC: if any of the prepare requests fail or time out, the coordinator aborts the transaction; if any of the commit or abort requests fail, the coordinator retries them indefinitely. If the coordinator crashes, the only way 2PC can complete is by waiting for the coordinator to recover. This is why the coordinator must write its commit or abort decision to a transaction log on disk before sending commit or abort requests to participants. 

X/Open XA (eXtended Architecture) is a standard for implementing two-phase commit across heterogeneous technologies. It is a C API for interfacing with a transaction coordinator.

The consensus problem is normally formalized as follows: one or more nodes may propose values, and the consensus algorithm decides on one of those values. `The core idea of consensus: everyone decides on the same outcome, and once you have decided, you cannot change your mind.` A large-scale outage can stop the system from being able to process requests, but it cannot corrupt the consensus system by causing it to make invalid decisions.

Consensus systems always require a strict majority to operate. Sometimes, consensus algorithms are particularly sensitive to network problems. 

ZooKeeper and etcd are designed to hold small amounts of data that can fit entirely in memory (although they still write to disk for durability) - so you wouldn't want to store all of your application's data here. That small amount of data is replicated across all the nodes using a fault-tolerant total order broadcast algorithm. Total order broadcast is what you need for database replication. 

Trying to perform majority votes over so many nodes would be terribly inefficient. Instead, ZooKeeper runs on a fixed number of nodes (usually three or five) and performs its majority votes among those nodes while supporting a potentially large number of clients.

ZooKeeper, etcd, and Consul are also often used for `service discovery` - that is, to find out which IP address you need to connect to in order to reach a particular service. 

A membership service determines which nodes are currently active and live members of a cluster.
