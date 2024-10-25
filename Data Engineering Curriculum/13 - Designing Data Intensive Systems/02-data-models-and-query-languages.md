# Data Models and Query Languages
Data models are one of the most important part of developing software, because they not only affect how the software is written, but also affect how we think about the problem that we are solving. 

Most applications are built by layering one data model on top of another. Each layer hides the complexity of the layers below it by providing a clean data model.

Since the data model has such a profound effect on what the software above it can and can't do, it's important to choose one that is appropriate to the application.

## Relational Model Versus Document Model
Much of what you see on the web today is still powered by relational databases, be it online publishing, discussion, social networking, e-commerce, games, software-as-a-service productivity applications, or much more.

There are several driving forces behind the adoption of NoSQL databases, including:
- A need for greater scalability, including very large datasets or very high write throughput
- Preference for free and open source software over commercial ones
- Specialized query that are not well supported by the relational model
- A desire for a more dynamic and expressive data model

## The Object-Relational Mismatch
Most application development today is done in object-oriented programming languages, but if data is stored in relational tables, an awkward translation layer is required between them. The disconnect between the models is sometimes called an `impedance mismatch`.

For a data structure with `one to many` relationships like a resume (one person with many occupations, education history, etc), which is mostly a self-contained document, a JSON representation can be quite appropriate. JSON has the appeal of being much simpler than XML. Document-oriented databases like MongoDB, RethinkDB, CouchDB, and Espresso support this data model.

## Many-to-One and Many-to-Many Relationships
Anything that is meaningful to humans may need to change sometime in the future - and if that information is duplicated, all the redundant copies need to be updated. Removing such duplication is the key idea behind normalization in databases. As a rule of thumb, `if you're duplicating values that could be stored in just one place, the schema is not normalized`.

Example: many people live in one city - normalizing this data requires many-to-one relationships, which don't fit nicely into the document model (where support for joins are weak).

If the database itself does not support joins, you have to emulate a join in application code by making multiple queries to the database (the work of making the join is shifted from the database to the application code). Moreover, even if the initial version of an application fits well in a join-free document model, as features are added to applications, data has a tendency of becoming more interconnected, with many-to-many relationships. 

## Relational Versus Document Databases
If the data in your application has a document-like structure (i.e., a tree of one-to-many relationships, where typically the entire tree is loaded at once), then it's probably a good idea to use a document model. However, if your application use many-to-many relationships, using a document model can lead to significantly more complex application code and worse performance. For highly interconnected data, the document model is awkward, the relational model is acceptable, and graph models are the most natural.

Most document databases, and the JSON support in relational databases, do not enforce any schema on the data in documents (schema-on-read).

## Data locality for queries
A document is usually stored as a single continuous string, there is a performance advantage to this storage locality.

## Query Languages for Data
SQL is a declarative query language. It is up to the database system's query optimizer to decide which indexes and which join methods to use, and in which order to execute various parts of the query. Also, declarative languages often lend themselves to parallel execution.

## MapReduce Querying
MapReduce is a programming model for processing large amounts of data in bulk across many machines. MapReduce is neither a declarative query language nor a fully imperative query API, but somewhere in between: the logic of the query is expressed with snippets of code, which are called repeatedly by the processing framework. It is based on the map (also known as collect) and reduce (also known as fold or inject) functions that exist in many functional programming languages.

## Graph-like data models
A graph consists of two kinds of objects: vertices (also known as nodes or entities) and edges (also known as relationships or arcs). Many kinds of data can be modeled as a graph. Graphs are not limited to homogeneous data: an equally powerful use of graphs is to provide a consistent way of storing completely different types of objects in a single datastore.

Some important aspects of this model are:
1. Any vertex can have an edge connecting it with any other vertex. There is no schema that restricts which kinds of things can or cannot be associated.
2. Given any vertex, you can efficiently find both its incoming and its outgoing edges, and thus traverse the graph.
3. By using different labels for different kinds of relationships, you can store several different kinds of information in a single graph, while still maintaining a clean data model.

Those features give graphs a great deal of flexibility for data modeling. Graphs are good for evolvability: as you add features to your application, a graph can easily be extended to accommodate changes in your application's data structures.

Cypher is a declarative query language for property graphs. 

Since SQL:1999, the idea of variable-length traversal paths in a query can be expressed using recursive common table expressions (CTEs) (the WITH RECURSIVE syntax).

### Triple-Stores and SPARQL
In a triple-store, all information is stored in the form of very simple three-part statements: (subject, predicate, object). For example, in the triple (Jim, likes, bananas). 

SPARQL is a query language for triple-stores using the RDF data model. SPARQL is a nice query language, it can be a powerful tool for applications to use internally.

