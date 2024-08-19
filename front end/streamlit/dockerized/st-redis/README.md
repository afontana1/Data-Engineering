1. run 
```shell
docker-compose up
```

- A Redis container named ‘redisdb’, and expose port 6379.
- A Streamlit app making use of our code defined inside the ‘app.py’ file, and expose port 8501.
- A new Docker image named “microservice-website”, and link ports 8501 and 6379.

2. opening redis CLI
```shell
docker exec -it redisdb redis-cli

keys *
```