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

# Copy the current directory contents into the container at /code
COPY . /code

# Make register.sh executable
RUN chmod +x /code/register.sh

# Run the register.sh script
CMD ["/code/register.sh"]
