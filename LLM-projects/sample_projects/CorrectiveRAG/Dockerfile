FROM python:3.11-slim-bookworm AS builder
RUN mkdir /main
WORKDIR /main
ADD . .
RUN apt-get update --fix-missing && apt-get install -y --fix-missing \
    build-essential \
    gcc \
    g++ \
    cmake \
    autoconf && \
    rm -rf /var/lib/apt/lists/* 
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]