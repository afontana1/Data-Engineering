# 1. Reliable, Scalable, and Maintainable Applications
Many applications today are `data-intensive` - their limiting factor: `amount/complexity/speed-of-change of data`. When building an application, we need to figure out `which tools and which approaches are the most appropriate` for the task. And it can be hard to `combine tools` when you need to do something that a single tool cannot do alone.

Why put data storage tools all under `data systems`?
- The `boundaries` between the traditional categories are becoming blurred. (Redis for message queues, Kafka for db-like durability guarantees, etc)
- Apps now have diverging requirements, so a single tool is no longer sufficient. Need to `break down into tasks` that can be performed with `a single tool`, then `stitch` different tools together using app code. (create `special-purpose data systems` from `smaller, general-purpose components`)

Many factors influence the design of a data system, depend on the situation:
- the skills and experience of the people
- legacy system dependencies
- the timescale for delivery
- your org’s tolerance of different kinds of risk
- regulatory constraints
- ...

There are 3 concerns that are important in most software systems: 
1. **Reliable** - continue to work correctly even when things go wrong (hardware/software faults, and human error).
2. **Scalable** - as the system grows (in data/traffic volume, or complexity), there should be ways to deal with it.
3. **Maintainable** - Over time, many different people will work on the system (engineering and ops, both maintaining current behavior and adapting the system to new use cases), and they should all be able to work on it productively.

## Reliability
Bugs in business applications cause lost productivity, and legal risks if numbers are reported incorrectly; outages of e-commerce sites can have huge costs in lost revenue and damage to reputation.

A `fault` is one component of the system not working; a `failure` is when the whole system stops working.

For `hardware faults`, we can add `redundancy` to the individual hardware components to reduce the failure rate of the system. It makes total failure of `a single machine` fairly rare (but needs planned downtime). But more applications have begun using `larger numbers of machines`, which proportionally increases the rate of hardware faults - Hence there is a move toward systems that can `tolerate the loss of entire machines`, by using software fault-tolerance techniques, or in addition to hardware redundancy (allows for rolling upgrade).

For `software errors`, the bugs often hide for a long time until they are triggered by an unusual set of circumstances. There is no quick solution to it. Small things can help: carefully thinking about assumptions and interactions in the system; thorough testing; process isolation; allowing processes to crash and restart; measuring, monitoring, and analyzing system behavior in production.

For `human errors`, we could Design systems in a way that minimizes opportunities for error; use sandbox environments; test thoroughly; Allow quick and easy recovery; set up detailed and clear monitoring; implement good management practices and training; etc. 

## Scalability
`Scalability` describes a system’s ability to `cope with increased load`. E.g.: “If the system grows in a particular way, what are our options for coping with the growth?” and “How can we add computing resources to handle the additional load?” 

`Load` can be described with a few load parameters. The best choice of parameters (requests per sec, ratio of reads to writes, num of concurrent active users, ...) depends on the architecture of your system. 

An example: Implementing Twitter. Twitter’s scaling challenge is due to fan-out (each user follows/followed-by many people). There are two ways of doing this:
- Posting a tweet inserts the new tweet into a global tweets collection. When a user requests their home timeline, look up all the people they follow, find all the tweets for each of those users, and merge them,  sorted by time. Do more work at read time and less at write time. (v1 of twitter)
- Maintain a pre-computed cache for each user’s home timeline. When a user posts a tweet, look up all the people who follow that user, and insert the new tweet into each of their home timeline caches. Do more work at write time and less at read time. (v2 of twitter, switched from v1, because home-page refresh happens much more frequent than posting a tweet)

However, for v2, celebrities have millions of followers makes updating cache time-consuming. So they use hybrid v1 (for celebrities) and v2 (for regular users) approach. 

Describing the performance of a system: In online systems, service’s `response time` is important (the time between request sent and response received). Response time is a distribution of values (better in percentiles). `High percentiles` of response times  (tail latencies) are important because they directly affect users’ experience of the service. Queueing delays often takes a large part of the response time at high percentiles.

The `response time` is what the `client sees` - it includes network delays and queueing delays. `Latency` is the duration that a request is waiting to be handled (awaiting service), is the delay. 

A system that can run on a single machine is often simpler, but high-end machines can be very expensive, so very intensive workloads often `can’t avoid scaling out`. In reality, good architectures usually involve a  `mixture of approaches`.

An architecture that scales well for a particular application is built around assumptions of which operations will be common and which will be rare (the load parameters). If those assumptions turn out to be wrong, the engineering effort for scaling is wasted or counterproductive. In an early-stage startup or an unproven product it’s usually more important to be able to `iterate quickly on product features` than it is to `scale to some hypothetical future load`.

## Maintainability
The majority of the cost of software is not in its initial development, but in its ongoing maintenance. 

For maintainability, there are three design principles for software systems:
- Operability - Make it easy for operations teams to keep the system running smoothly.
- Simplicity - Make it easy for new engineers to understand the system (rmv complexity).
- Evolvability - Make it easy for engineers to make changes to the system in the future, adapting it for unanticipated use cases as requirements change (such as using agile working patterns).
