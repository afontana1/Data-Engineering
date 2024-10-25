#!/bin/bash

curl -X PUT -H "Content-Type: application/vnd.schemaregistry.v1+json" \
     --data '{"compatibility": "FULL"}' \
     http://localhost:8081/config/todo-value
