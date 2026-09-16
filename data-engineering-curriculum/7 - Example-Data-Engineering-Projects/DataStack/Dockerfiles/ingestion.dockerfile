FROM python:3.9.1

RUN pip3 install pandas sqlalchemy psycopg2 python-dotenv pymysql cryptography pyarrow fastparquet

WORKDIR /app
COPY ./scripts/ingest_data.py ingest_data.py 
COPY ./data data

ENTRYPOINT ["python"]
CMD ["ingest_data.py"]