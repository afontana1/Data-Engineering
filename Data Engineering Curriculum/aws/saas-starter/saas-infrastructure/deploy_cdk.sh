# First make sure the Dockerfile is up to date.
(cd ./compute/base_layer && ./generate_base_layer.sh)

# Then deploy the CDK application.
cdk deploy