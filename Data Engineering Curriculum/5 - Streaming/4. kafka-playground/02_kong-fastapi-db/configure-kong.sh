#!/bin/bash

# Create microservice1 service
# curl -i -X POST http://kong:8001/services/ \
#      --data "name=microservice1" \
#      --data "url=http://microservice1:9000"

# # Create microservice1 route
# curl -i -X POST http://kong:8001/services/microservice1/routes \
#      --data "name=ms1-route" \
#      --data "paths[]=/microservice1" \
#      --data "hosts[]=localhost" \
#      --data "strip_path=true"

# # Create auth-service service
# curl -i -X POST http://kong:8001/services/ \
#      --data "name=auth-service" \
#      --data "url=http://auth-service:9002"

# # Create auth-service route
# curl -i -X POST http://kong:8001/services/auth-service/routes \
#      --data "name=auth-service-route" \
#      --data "paths[]=/auth-service" \
#      --data "hosts[]=localhost" \
#      --data "strip_path=true"

# THESE COMMANDS ARE FOR LOCAL DEVELOPMENT
# Create microservice1 service
curl -i -X POST http://localhost:8001/services/ \
     --data "name=microservice1" \
     --data "url=http://microservice1:9000"

# Create microservice1 route
curl -i -X POST http://localhost:8001/services/microservice1/routes \
     --data "name=ms1-route" \
     --data "paths[]=/microservice1" \
     --data "hosts[]=localhost" \
     --data "strip_path=true"

# Create auth-service service
curl -i -X POST http://localhost:8001/services/ \
     --data "name=auth-service" \
     --data "url=http://auth-service:9002"

# Create auth-service route
curl -i -X POST http://localhost:8001/services/auth-service/routes \
     --data "name=auth-service-route" \
     --data "paths[]=/auth-service" \
     --data "hosts[]=localhost" \
     --data "strip_path=true"
