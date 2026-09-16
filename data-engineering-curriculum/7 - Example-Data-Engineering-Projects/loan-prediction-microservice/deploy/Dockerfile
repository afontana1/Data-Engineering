FROM python:3.8-slim-buster

RUN apt-get update
RUN apt-get install -y -qq redis

COPY ./deploy/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install redis==4.4.0

