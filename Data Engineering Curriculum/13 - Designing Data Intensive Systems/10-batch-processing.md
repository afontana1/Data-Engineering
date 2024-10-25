# 10. Batch Processing
Applications commonly use a combination of several different datastores, indexes, caches, analytics systems, etc. and implement mechanisms for moving data from one store to another. In reality, integrating disparate systems is one of the most important things that needs to be done in a nontrivial application.

A `system of record`, also known as source of truth, holds the authoritative version of your data. `Data in a derived system` is the result of taking some existing data from another system and transforming or processing it in some way.

Technically speaking, derived data is redundant, in the sense that it duplicates existing information. However, it is often essential for getting good performance on read queries. It is commonly denormalized.

Three different types of systems:
- Services (online systems). A service waits for a request/instruction from a client. When one is received, it tries to handle it ASAP and sends a response back. Response time is usually the primary measure of performance of a service, and availability is often very important. 
- Batch processing systems (offline systems). Takes a large amount of input data, runs a job to process it, and produces some output data. Often scheduled to run periodically. The primary performance measure of a batch job is usually throughput. 
- Stream processing systems (near-real-time systems). A stream processor consumes inputs and produces outputs. 

The Unix philosophy: Automation, rapid prototyping, incremental iteration, being friendly to experimentation, and breaking down large projects into manageable chunks - sounds remarkably like the Agile and DevOps movements of today.

A Unix shell like bash lets us easily compose these small programs into surprisingly powerful data processing jobs.

If you expect the output of one program to become the input to another program, that means those programs must use the same data format - in other words, a compatible interface. In Unix, that interface is a file. 

Separating the input/output wiring from the program logic makes it easier to compose small tools into bigger systems. However, `the biggest limitation of Unix tools is that they run only on a single machine - and that's where tools like Hadoop come in`.

## MapReduce and distributed file systems
MapReduce is a bit like Unix tools, but distributed across potentially thousands of machines. `MapReduce is a programming framework with which you can write code to process large datasets in a distributed filesystem like HDFS.` A single MapReduce job is comparable to a single Unix process: it takes one or more inputs and produces one or more outputs. A MapReduce job normally does not modify the input and does not have any side effects other than producing the output.

While Unix tools use stdin and stdout as input and output, MapReduce jobs read and write files on a distributed filesystem. In Hadoop's implementation of MapReduce, that filesystem is called HDFS (Hadoop Distributed File System). HDFS is based on the shared-nothing principle, which requires no special hardware, only computers connected by a conventional datacenter network. In order to tolerate machine and disk failures, file blocks are replicated on multiple machines. 

To create a MapReduce job, you need to implement two callback functions, the mapper and reducer. 

The main difference from pipelines of Unix commands is that MapReduce can parallelize a computation across many machines, without you having to write code to explicitly handle the parallelism.

It is very common for MapReduce jobs to be chained together into workflows, such that the output of one job becomes the input to the next job, like a sequence of commands where each command's output is written to a temporary file, and the next command reads from the temporary file. To handle these dependencies between job executions, various workflow schedulers for Hadoop have been developed, including Oozie, Azkaban, Luigi, Airflow, and Pinball. 

In order to achieve good throughput in a batch process, the computation must be (as much as possible) local to one machine.

A workflow of MapReduce jobs is not the same as a SQL query used for analytic purposes. The output of a batch process is often not a report, but some other kind of structure.

Collecting data in its raw form, and worrying about schema design later, allows the data collection to be speeded up (known as a "data lake" or "enterprise data hub"). Thus, Hadoop has often been used for implementing ETL processes: data from transaction processing systems is dumped into the distributed filesystem in some raw form, and then MapReduce jobs are written to clean up that data, transform it into a relational form, and import it into an MPP data warehouse for analytic purposes. Data modeling still happens, but it is in a separate step, decoupled from the data collection. This decoupling is possible because a distributed filesystem supports data encoded in any format.

The MapReduce approach is more appropriate for larger jobs: jobs that process so much data and run for such a long time that they are likely to experience at least one task failure along the way. Overcommitting resources allows better utilization of machines and greater efficiency compared to systems that segregate production and nonproduction tasks. However, as MapReduce jobs run at low priority, they run the risk of being preempted at any time because a higher-priority process requires their resources.

The process of writing out intermediate state to files is called materialization.

To fix these problems with MapReduce, data flow engines for distributed batch computations were developed, such as Spark, Tez and Flink. They handle an entire workflow as one job, rather than breaking it up into independent subjobs.
