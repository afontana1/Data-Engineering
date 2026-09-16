# 11. Stream Processing
In reality, a lot of data is unbounded because it arrives gradually over time. In general, a “stream” refers to data that is incrementally made available over time. In a stream processing context, a record is more commonly known as an event. An event is generated once by a producer (also known as a publisher or sender), and then potentially processed by multiple consumers (subscribers or recipients). Related events are usually grouped together into a topic or stream.

A common approach for notifying consumers about new events is to use a messaging system: a producer sends a message containing the event, which is then pushed to consumers. A messaging system allows multiple producer nodes to send messages to the same topic and allows multiple consumer nodes to receive messages in a topic.

When multiple consumers read messages in the same topic, two main patterns of messaging are used:
- Load balancing: Each message is delivered to one of the consumers
- Fan-out: Each message is delivered to all of the consumers.

The two patterns can be combined: for example, two separate groups of consumers may each subscribe to a topic, such that each group receives all messages, but within each group only one of the nodes receives each message. 

In order to ensure that the message is not lost, message brokers use acknowledgments: a client must explicitly tell the broker when it has finished processing a message so that the broker can remove it from the queue. 

Log-based message brokers combine the durable storage approach of databases with the low-latency notification facilities of messaging. In order to scale to higher throughput than a single disk can offer, the log can be partitioned. Within each partition, the broker assigns a monotonically increasing sequence number, or offset, to every message. Such a sequence number makes sense because a partition is append-only, so the messages within a partition are totally ordered. There is no ordering guarantee across different partitions. Apache Kafka, Amazon Kinesis Streams, and Twitter’s DistributedLog are such log-based message brokers. Even though these message brokers write all messages to disk, they are able to achieve throughput of millions of messages per second by partitioning across multiple machines, and fault tolerance by replicating messages. To achieve load balancing across a group of consumers, instead of assigning individual messages to consumer clients, the broker can assign entire partitions to nodes in the consumer group.

In situations where messages may be expensive to process and you want to parallelize processing on a message-by-message basis, and where message ordering is not so important, the JMS/AMQP style of message broker is preferable. On the other hand, in situations with high message throughput, where each message is fast to process and where message ordering is important, the log-based approach works very well.

If you only ever append to the log, you will eventually run out of disk space. To reclaim disk space, the log is actually divided into segments, and from time to time old segments are deleted or moved to archive storage. In practice, the log can typically keep a buffer of several days’ or even weeks’ worth of messages.

If a consumer does fall too far behind and starts missing messages, only that consumer is affected; it does not disrupt the service for other consumers. This fact is a big operational advantage: you can experimentally consume a production log for development, testing, or debugging purposes, without having to worry much about disrupting production services. When a consumer is shut down or crashes, it stops consuming resources—the only thing that remains is its consumer offset.

More recently, there has been growing interest in change data capture (CDC), which is the process of observing all data changes written to a database and extracting them in a form in which they can be replicated to other systems. CDC is especially interesting if changes are made available as a stream, immediately as they are written. The derived data systems are just consumers of the change stream. Essentially, change data capture makes one database the leader (the one from which the changes are captured), and turns the others into followers.

Log compaction is supported by Apache Kafka - it allows the message broker to be used for durable storage, not just for transient messaging.

API support for change streams - Increasingly, databases are beginning to support change streams as a first-class interface. For example, RethinkDB allows queries to subscribe to notifications when the results of a query change, Firebase and CouchDB provide data synchronization based on a change feed that is also made available to applications, and Meteor uses the MongoDB oplog to subscribe to data changes and update the user interface. 

In event sourcing, the application logic is explicitly built on the basis of immutable events that are written to an event log. The event store is append-only, and updates or deletes are discouraged or prohibited. Events are designed to reflect things that happened at the application level, rather than low-level state changes in CDC. Event sourcing is a powerful technique for data modeling: from an application point of view it is more meaningful to record the user’s actions as immutable events. Applications that use event sourcing need to take the log of events and transform it into application state that is suitable for showing to a user. 

A stream processor consumes input streams in a read-only fashion and writes its output to a different location in an append-only fashion. The one crucial difference to batch jobs is that a stream never ends.

In principle, any stream processor could be used for materialized view maintenance. 

Joins can be stream-stream join, stream-table join, and table-table join. The stream processor’s local copy of the database needs to be kept up to date. This issue can be solved by change data capture. 

If the ordering of events across streams is undetermined, the join becomes nondeterministic, which means you cannot rerun the same job on the same input and necessarily get the same result: the events on the input streams may be interleaved in a different way when you run the job again. In data warehouses, this issue is known as a slowly changing dimension (SCD), and it is often addressed by using a unique identifier for a particular version of the joined record. 

An idempotent operation is one that you can perform multiple times, and it has the same effect as if you performed it only once.



