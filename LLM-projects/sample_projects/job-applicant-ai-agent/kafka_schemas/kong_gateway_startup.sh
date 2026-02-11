#!/bin/sh

KONG_ADMIN_URL="http://host.docker.internal:8001"

# Wait for Kong to be ready
until $(curl --output /dev/null --silent --head --fail $KONG_ADMIN_URL); do
  printf '.'
  sleep 5
  echo "Waiting for Kong Gateway to be ready..."
done

#####################
####### AUTH #######
#####################

# Register GATEWAY
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=auth-server" \
  --data "url=http://host.docker.internal:9000"

# Register BASE ROUTE
curl -i -X POST $KONG_ADMIN_URL/services/auth-server/routes \
  --data "paths[]=/auth-server" \
  --data "strip_path=true"

#####################
####### TO DO #######
#####################

# Register todo
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=todo-service" \
  --data "url=http://host.docker.internal:9002"

# Register todo-service route
curl -i -X POST $KONG_ADMIN_URL/services/todo-service/routes \
  --data "paths[]=/todo-service" \
  --data "strip_path=true"

#####################
#### AI REC. ENG. ####
#####################

# Register merged spec service
curl -i -X POST $KONG_ADMIN_URL/services/ \
  --data "name=ai-eng" \
  --data "url=http://host.docker.internal:9001"

# Register merged spec route
curl -i -X POST $KONG_ADMIN_URL/services/ai-eng/routes \
  --data "paths[]=/ai-eng" \
  --data "strip_path=true"

echo "Kong Gateway setup completed!"
