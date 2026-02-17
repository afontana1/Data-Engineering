# splitter/Dockerfile
FROM python:3.12-slim

# Install qpdf (and minimal deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
    qpdf \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 10001 appuser
WORKDIR /app

# Install python deps
COPY splitter/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy code
COPY splitter/splitter.py /app/splitter.py

USER 10001

# Entrypoint
CMD ["python", "/app/splitter.py"]