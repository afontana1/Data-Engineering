FROM python:3.8-slim-buster AS ApiImage

LABEL org.opencontainers.image.source https://github.com/RedisVentures/loan-prediction-microservice

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/
COPY ./backend/requirements.txt /app/requirements.txt


RUN python3 -m pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]