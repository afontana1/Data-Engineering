# 4. Encoding and Evolution
Old and new versions of the code, and old and new data formats, may coexist in the system at the same time. For the system to continue running smoothly, we need to maintain compatibility in both directions:
- `Backward compatibility`: Newer code can read old data. Easy to achieve, because you know the old data format
- `Forward compatibility`: Older code can read new data. Harder to achieve, because you need to ignore future additions in data format

The translation from the in-memory representation to a byte sequence is called `encoding` (serialization/marshalling), and the reverse is called `decoding` (parsing/ deserialization/unmarshalling).

Language-specific formats for encoding: convenient, but lock you to a particular programming language; be a security issue; back forward/backward compatibility; bad performance. => it’s usually not recommended to use your language’s built-in encoding. 

JSON, XML, and Binary Variants: JSON, XML, and CSV are textual formats, and thus human-readable. Problems: Ambiguity: Without external schema, XML & CSV cannot distinguish a num and a digit-only string; JSON cannot specify a precision, and cannot distinguish integers and floats. JSON and XML do not support binary strings, so people use base64 encoding. 

Binary encoding: space saving is not significant, but loses human readability. 

Apache Thrift and Protocol Buffers: require a schema, then field names are replaced by field tags (numbers) in the encoded data. Handles schema evolution: forward compatibility by ignore unknown field tags, backward compatibility by making newly added fields optional, or have a default val. You can remove an optional field, and never reuse its tag number. 

Apache Avro: uses a schema to specify the structure of the data being encoded. If you want to allow a field to be null, you have to use a union type. Schema doesn’t contain any tag numbers. Friendly to dynamically generated schemas.

For dataflow through database: `Schema evolution` allows the entire database to appear as if it was encoded with a single schema, even though the underlying storage may contain records encoded with various historical versions of the schema.

For dataflow through services: REST APIs and RPC 

Message-passing dataflow: Async message brokers such as Apache Kafka. 





































