# 8. The trouble with distributed systems
For a software on a single computer, when the hardware is working correctly, the same operation always produces the same result (deterministic). If there is a hardware problem, the consequence is usually a total system failure. An individual computer with good software is usually either fully functional or entirely broken, but not something in between.

In a distributed system, there may be some parts of the system that are broken in some unpredictable way, even though other parts of the system are working fine - Partial failure. Partial failures are nondeterministic, which makes distributed systems hard to work with. 

Different types of `large scale computing systems`:
- `High performance computing (HPC)`. Super computers with thousands of CPUs. Usually for scientific computing. A super computer is more like a single-node computer than a distributed system. It escalates partial failure to total failure. 
- `Cloud computing`. Multi-tenant data centers, commodity computers connected via internet, elastic resource allocation, metered billing
- `Traditional enterprise datacenters` lie somewhere between the both

Cloud computing:
- need to serve users with low latency at any time
- nodes are built from commodity machines - low cost, but higher failure rates
- often based on internet
- bigger system with thousands of nodes always have something broken. need to tolerate failed nodes and still keep working
- internet an be slow and unreliable for geo-distributed system

Therefore, we need to build a reliable system from unreliable components. 

## Unreliable Networks
`shared-nothing systems`: i.e., a bunch of machines connected by a network.

Shared-nothing has become the dominant approach for building internet services, because it is cheap, can use cloud computing services, and can achieve high availability through redundancy across multiple geo distributed datacenters. 

The internet and most internal networks in datacenters are async packet networks. One node can send a message (packet) to another node, but the network can not guarantee when/whether it will arrive. If you send a request and expect a response, many things could go wrong. If you send a request to another node and don’t receive a response, it is impossible to tell why. The usual way of handling this issue is a timeout. 

You need to know how your software reacts to network problems and ensure that the system can recover from them.

Many systems need to automatically detect faulty nodes.

In public clouds and multi-tenant datacenters, resources are shared among many customers: the network links and switches, and even each machine’s network interface and CPUs (when running on virtual machines), are shared. Batch workloads such as MapReduce can easily saturate network links. As you have no control over or insight into other customers’ usage of the shared resources, network delays can be highly variable if someone near you (a noisy neighbor) is using a lot of resources. 

Variable delays in networks are not a law of nature, but simply the result of a cost/ benefit trade-off. Currently deployed technology does not allow us to make any guarantees about delays or reliability of the network: we have to assume that network congestion, queueing, and unbounded delays will happen. Consequently, there’s no “correct” value for timeouts—they need to be determined experimentally.

## Unreliable Clocks
The time when a message is received is always later than the time when it is sent, but due to variable delays in the network, we don’t know how much later.

Each machine on the network has its own clock, which is an actual hardware device: usually a quartz crystal oscillator. These devices are not perfectly accurate. 

It is possible to synchronize clocks to some degree: the most commonly used mechanism is the Network Time Protocol (NTP), which allows the computer clock to be adjusted according to the time reported by a group of servers. 

Modern computers have at least two different kinds of clocks: a `time-of-day clock` and a `monotonic clock`.

If the local clock is too far ahead of the NTP server, it may be forcibly reset and appear to jump back to a previous point in time. These jumps, as well as the fact that they often ignore leap seconds, make time-of-day clocks unsuitable for measuring elapsed time. 

`A monotonic clock is suitable for measuring time intervals`, such as a timeout or a service’s response time. The name comes from the fact that they are guaranteed to always move forward (whereas a time-of-day clock may jump back in time).

Logical clocks are based on incrementing counters rather than an oscillating quartz crystal, so they are a safer alternative for ordering events. Logical clocks do not measure the time of day or the number of seconds elapsed, only the relative ordering of events. 

`Time-of-day and monotonic clocks`, which measure actual elapsed time, are also known as `physical clocks`.

Google’s TrueTime API in Spanner explicitly reports the confidence interval on the local clock. When you ask it for the current time, you get back two values: [earliest, latest], which are the earliest possible and the latest possible timestamp.

Developing real-time systems is very expensive, and they are most commonly used in safety-critical embedded devices.

`Fencing tokens` can be used to protect access to some resource, in case a node claims itself as the leader while in fact it is not. 

Distributed systems problems become much harder if there is a risk that nodes may “lie” (send arbitrary faulty or corrupted responses)— eg, if a node may claim to have received a particular message when in fact it didn’t. Such behavior is known as a `Byzantine fault`. 

## System Model and Reality
For modeling real systems, the partially synchronous model with crash-recovery faults is generally the most useful model.

Safety is often informally defined as nothing bad happens, and liveness as something good eventually happens.
