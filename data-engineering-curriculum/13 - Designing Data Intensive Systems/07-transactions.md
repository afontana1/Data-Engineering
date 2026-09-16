# 7. Transactions
This chapter talks about ideas and algorithms mostly in the context of a database running on a single machine.

A `transaction` a mechanism for grouping multiple operations on multiple objects into one unit of execution. All the reads and writes in a transaction are executed as one operation: either the entire transaction succeeds (commit) or it fails (abort, rollback). If it fails, the application can safely retry. `With transactions, application doesn't need to worry about partial failure`. 

Historically, the safety guarantees provided by transactions are known as ACID, which is vague: 
- Atomicity: means abortability - a transaction can be rolled back if there's an error in the middle. 
- Consistency: the application makes sure that certain statements (invariants) are always true.
- Isolation: concurrent transactions are isolated from each other (serializability)
- Durability: Once a transaction has committed, the data will not get lost, even with hardware fault or database crash. Means the data is written to disk, or got replicated. Perfect durability does not exist. 

Multi-object operations: These definitions assume that you want to modify several objects (rows, documents, records) at once. Such multi-object transactions are often needed if several pieces of data need to be kept in sync. Multi-object transactions need a way to determine which read and write operations belong to the same transaction. In relational databases, that is typically done based on the client’s TCP connection to the database server: on any particular connection, everything between a BEGIN TRANSACTION and a COMMIT statement is considered to be part of the same transaction. 

Single-object operations: storage engines almost universally aim to provide atomicity and isolation on the level of a single object on one node. Atomicity can be implemented using a log for crash recovery, and isolation can be implemented using a lock on each object.

Cases when multi-object transactions are needed: 
- In a relational data model, when updating one row in a table, and this row has a foreign key reference to a row in another table
- In a document data model, when denormalized data needs to be updated, transaction make sure this type of data are in sync
- dbs with secondary indexes, these indexes also need to be updated when value is updated. 

## Weak isolation levels
Concurrency bugs caused by weak transaction isolation have caused serious issues in production.

### Read Committed
Most basic level of transaction isolation:
- `No dirty reads`: `You only read committed data`, will not see the database in a partially updated state. 
- `No dirty writes`: `You can only over-write/modify committed data`, not the data that are currently being modified in another transaction. 

It is the default setting in Oracle 11g, PostgreSQL, SQL Server 2012, MemSQL, etc. 

Databases usually prevent dirty writes by using row-level locks. Only one transaction can hold the lock for any given object. 

Databases usually prevent dirty reads by remembering both the old committed value and the new value set by the on-going transaction. So other transactions that are reading the objects are just given the old value. 

### Snapshot isolation
Problem with read committed transaction isolation level: Alice has 2 bank account, each have $500. Alice checks account 1, and saw 500$. A transfer of $100 from account 2 to account 1 happens, and then completes. Alice now checks account 2, and saw 400$. It seems between her 2 checks, 100$ disappeared. 

Such "non-repeatable read" (read skew) over a time period can cause problems with db backups that takes time to complete (will cause old data and new data over a span of time to be spliced together in a backup). It also cause problem to a time consuming analytical query, or integrity checks to check for system corruption. `Read skew: When a read transaction is going on, a write transaction writes a value to what is going to be read by read transaction, so the values got read are from different time points mixed together. `

Snapshot isolation is the most common solution to this problem - `Each transaction reads (sees) from a snapshot of the database taken at one single point of time, instead of over a time span`. 

Snapshot isolation is supported by PostgreSQL, MySQL with InnoDB storage engine, Oracle, SQL Server, etc. 

The database must potentially keep several different committed versions of an object, because various in-progress transactions may need to see the state of the database at different points in time. Because it maintains several versions of an object side by side, this technique is known as multiversion concurrency control (MVCC). When a transaction reads from the database, transaction IDs are used to decide which objects it can see and which are invisible.

Many dbs that implement snapshot isolation call it by different names. In Oracle it is called `serializable`, and in PostgreSQL and MySQL it is called `repeatable read`. 

The `lost update problem` can occur if an application reads some value from the database, modifies it, and writes back the modified value (a read-modify-write cycle). `If two transactions do read-modify-write cycle concurrently, for the same record, one of the modifications can be lost, because the second write does not include the first modification.` Cases are:
- Incrementing a counter or updating an account balance (a read-modify-write cycle)
- Making a local change to a complex value, e.g., adding an element to a list within a JSON document (requires parsing the document, making the change, and writing back the modified document)
- Two users editing a wiki page at the same time, where each user saves their changes by sending the entire page contents to the server, overwriting whatever is currently in the database. 

Solutions to the `lost update problem`: 
- Atomic write operation: remove the need to implement read-modify-write cycles in application code. Usually implemented by taking an exclusive lock on the object when it is read so that no other transaction can read it until the update has been applied. eg: UPDATE counters SET value = value + 1 WHERE key = 'foo';. 
- Explicit locking: the application explicitly lock the objects that are going to be updated. Then the application can perform a read-modify-write cycle, and if any other transaction tries to concurrently read the same object, it is forced to wait until the first read-modify-write cycle has completed. eg: select * from ... where ... FOR UPDATE. 
- Automatically detect lost updates: allow transactions to execute in parallel, and if the transaction manager detects a lost update, abort the transaction and force it to retry. This is less error prone compared with the first two solutions. PostgreSQL's repeatable read, Oracle's serializable, and SQL Server's snapshot isolation levels automatically do this. But MySQL, InnoDB's repeatable read doesn't do this. 
- Compare-and-set: in dbs that do not provide transactions, it avoids lost updates by allowing an update to happen only if the value has not changed since you last read it. It may not be safe, depends on the db. eg: UPDATE wiki_pages SET content = 'new content' WHERE id = 1234 AND content = 'old content';

For replicated dbs, to prevent lost updates, a common approach is to allow concurrent writes to create several conflicting versions of a value (siblings), and to use application code or special data structures to resolve and merge these versions after the fact. 

`Write skew`: `concurrent multi-object updates that violates a pre-checked condition, such as meeting room doubly booked concurrently`: 
- A hospital must have at least one doctor on call. Doctor A and Doctor B both check how many doctors are there at the same time, and both request leave at the same time, resulting 0 doctor on call. They both modified their own records via a transaction, so it is neither a dirty write nor a lost update. 
- Meeting room booking system: two users concurrently inserting a conflicting meeting. 
- Multiplayer game: two players move different chess to the same position. 
- Claiming a username: two new user concurrently choose a same user name. Can use unique constraint to avoid this one. 

`Phantom`: `the result of a search query in a transaction is no longer valid after a write in another transaction. (What the query saw was only valid for a fraction of time of this transaction). Snapshot isolation can cause write skew in such read-write transactions. `

Solution: 
- Automatically preventing write skew requires true serializable isolation. 
- If you can’t use a serializable isolation level, you can explicitly lock the rows that the transaction depends on, using the FOR UPDATE clause (only doable if there are objects/rows to attach lock to). 
- Materializing conflicts: If there is no object to attach the locks, you can create (materialize) rows, such as creating rows for each time slots. This lets a concurrency control mechanism leak into the application level, so it is not recommended to do this. Recommend serializable isolation in this case. 

## Serializable isolation
`Serializable isolation is the strongest isolation level that prevents all possible race conditions`. It guarantees that even though transactions may execute in parallel, the end result is the same as if they had executed one at a time, serially. 

There are 3 techniques to implement it:
- Literally executing transactions in a serial order, on a single thread. Avoids the coordination overhead, but throughput is limited to a single CPU core (can be resolved by partitioning, if you can make them independent of each other). Systems with single-threaded serial transaction processing don’t allow interactive multi-statement transactions, because humans and networks are slow; instead, the app use a stored procedure. Used by VoltDB/H-Store, Redis and Datomic. 
- `Two-phase locking (2PL)`. Details see below. 
- Use optimistic concurrency control such as `serializable snapshot isolation`. Details see below. 

### Two-phase locking (2PL)
Two-phase locking, several transactions are allowed to concurrently read the same object as long as nobody is writing to it. But as soon as anyone wants to write (modify or delete) an object, exclusive access is required:
- If transaction A has read an object and transaction B wants to write to that object, B must wait until A commits or aborts before it can continue. This ensures that B can’t change the object unexpectedly behind A’s back.
- If transaction A has written an object and transaction B wants to read that object, B must wait until A commits or aborts before it can continue. Reading an old version of the object is not acceptable under 2PL.

`In 2PL, writers block both other writers and other readers. Readers in a transaction block other writers.` 

2PL is used by the serializable isolation level in MySQL (InnoDB) and SQL Server, and the repeatable read isolation level in DB2. 

The blocking of readers and writers is implemented by a having a lock on each object in the database. The lock can either be in shared mode (shared lock for readers) or in exclusive mode. If a transaction wants to write to an object, it must first acquire the lock in exclusive mode. After a transaction has acquired the lock, it must continue to hold the lock until the end of the transaction (commit or abort). `This is where the name “two-phase” comes from: the first phase (while the transaction is executing) is when the locks are acquired, and the second phase (at the end of the transaction) is when all the locks are released.`

Transaction throughput and response times of queries are significantly worse under two-phase locking than under weak isolation. Because human input may be involved, databases running 2PL can have quite unstable latencies, and they can be very slow at high percentiles. 

A `predicate lock` restricts access as follows: if transaction A wants to read objects matching some condition, like in that SELECT query, it must acquire a shared-mode predicate lock on the conditions of the query. If another transaction B currently has an exclusive lock on any object matching those conditions, A must wait until B releases its lock before it is allowed to make its query. If transaction A wants to insert, update, or delete any object, it must first check whether either the old or the new value matches any existing predicate lock. If there is a matching predicate lock held by transaction B, then A must wait until B has committed or aborted before it can continue. The key idea here is that a predicate lock applies even to objects that do not yet exist in the database, but which might be added in the future (phantoms).

Most databases with 2PL implement `index-range locking` (next-key locking), which is a simplified approximation of predicate locking. 

### Serializable Snapshot Isolation (SSI)
It provides full serializability, but has only a small performance penalty compared to snapshot isolation.

There may be a causal dependency between the queries and the writes in the transaction.

Optimistic means that instead of blocking if something potentially dangerous happens, transactions continue anyway, hoping that everything will be fine. `When a transaction wants to commit, the database checks whether anything bad happened (i.e., whether isolation was violated); if so, the transaction is aborted and has to be retried. Only transactions that executed serializably are allowed to commit`.

Compared to two-phase locking, the big advantage of serializable snapshot isolation is that one transaction doesn’t need to block waiting for locks held by another transaction. Like under snapshot isolation, writers don’t block readers, and vice versa. This design principle makes query latency much more predictable and less variable. In particular, read-only queries can run on a consistent snapshot without requiring any locks, which is very appealing for read-heavy workloads.














