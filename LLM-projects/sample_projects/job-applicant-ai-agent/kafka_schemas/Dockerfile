# Use an official Python runtime as a parent image
FROM python:3.12

LABEL maintainer="ameen-alam"

# Set the working directory in the container
WORKDIR /code

# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

# Install aiokafka package
RUN pip install aiokafka

# Copy the current directory contents into the container at /code
COPY . /code

# Make the scripts executable
RUN chmod +x /code/create_kafka_topics.py /code/register_schemas.sh /code/kong_gateway_startup.sh

# Verify the file permissions (for debugging purposes)
RUN ls -l /code/

# Run the create_kafka_topics.py script and then the register_schemas.sh script
CMD ["/bin/bash", "-c", "python /code/create_kafka_topics.py && /bin/bash /code/kong_gateway_startup.sh  && /code/register_schemas.sh "]
