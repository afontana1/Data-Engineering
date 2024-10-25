# 02_kafka_messaging

https://github.com/aio-libs/aiokafka

```

docker compose up --build

cd kafka_schema

chmod +x register.sh  

./register.sh

```

Now View a few Confluent Schema Endpoints in browser

http://localhost:8081/config/

http://localhost:8081/schemas/types

http://localhost:8081/subjects

http://localhost:8081/schemas/ids/1

http://localhost:8081/schemas/ids/2

http://localhost:8081/subjects/todo-value/versions

http://localhost:8081/subjects/todo-value/versions/1



https://docs.confluent.io/platform/7.6/schema-registry/develop/using.html

https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/protobuf_producer.py

https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/protobuf_consumer.py

https://docs.confluent.io/platform/current/schema-registry/index.html

https://docs.confluent.io/platform/7.6/schema-registry/fundamentals/serdes-develop/serdes-protobuf.html#protobuf-schema-compatibility-rules

https://www.confluent.io/blog/schemas-contracts-compatibility/?utm_source=stackoverflow&utm_medium=rmoff&utm_campaign=ty.community.con.rmoff_stackoverflow_2020-06-16&utm_term=rmoff-devx

https://github.com/confluentinc/schema-registry