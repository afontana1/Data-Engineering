#!/usr/bin/env python
from kafka import KafkaProducer
from flask import Flask, request
from flask import json

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers="kafka:29092")


def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())


@app.route("/")
def default_response():
    default_event = {"event_type": "default"}
    log_to_kafka("userItems", default_event)
    return "This is the default response!\n"


@app.route("/purchase_a_sword", methods=["GET", "POST"])
def purchase_sword():
    if request.method == "GET":
        sword_event = {"event_type": "purchase_a_sword"}
        log_to_kafka("userItems", sword_event)
        return "Sword Purchased\n"
    else:
        if request.headers["Content-Type"] == "application/json":
            sword_event = {
                "event_type": "purchase_a_sword:" + " " + json.dumps(request.json)
            }
            log_to_kafka("userItems", sword_event)
            return "Sword Purchased: " + json.dumps(request.json) + "\n"


@app.route("/join_a_guild", methods=["GET", "POST"])
def join_guild():
    if request.method == "GET":
        join_guild_event = {"event_type": "join_guild"}
        log_to_kafka("userItems", join_guild_event)
        return "Join a Guild!\n"
    else:
        if request.headers["Content-Type"] == "application/json":
            join_guild_event = {
                "event_type": "join_guild" + " " + json.dumps(request.json)
            }
            log_to_kafka("userItems", join_guild_event)
            return "Join a guild!" + json.dumps(request.json) + "\n"


@app.route("/get_coins", methods=["GET", "POST"])
def get_coins():
    if request.method == "GET":
        get_coins_event = {"event_type": "get_coins"}
        log_to_kafka("userItems", get_coins_event)
        return "Get Coins\n"
    else:
        if request.headers["Content-Type"] == "application/json":
            get_coins_event = {
                "event_type": "get_coins" + " " + json.dumps(request.json)
            }
            log_to_kafka("userItems", get_coins_event)
            return "Get " + json.dumps(request.json)["coins"] + "coins\n"
