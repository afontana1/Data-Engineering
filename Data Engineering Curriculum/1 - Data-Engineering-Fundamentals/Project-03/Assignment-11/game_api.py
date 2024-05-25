#!/usr/bin/env python
from kafka import KafkaProducer
from flask import Flask, request
from flask import json

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers="kafka:29092")


def log_to_kafka(topic, event):
    """
    This function will first add some metadata (such as: Host, User-Agent, etc) to our generated events and then encode it into binary and dump it into Kafka
    """
    event.update(request.headers)
    event.update({"remote_addr": request.remote_addr})
    producer.send(topic, json.dumps(event).encode())


@app.route("/")
def default_response():
    """
    We provide a GET and a POST API request form. The user can either use the default ("/") GET method or the POST method (where the user can add some JSON text. Both of those will be send to Kafka through the log_to_kafka function and will return a message to the user.
    """
    default_event = {"event_type": "default"}
    log_to_kafka("userItems", default_event)
    return "This is the default response!\n"


@app.route("/purchase_sword", methods=["GET", "POST"])
def purchase_sword():
    """
    We provide a GET and a POST API request form. The user can either use the purchase_a_sword GET method (and choose a sword color) or the POST method (where the user can add some JSON text. Both of those will be send to Kafka through the log_to_kafka function and will return a message to the user.
    """
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
    """
    We provide a GET and a POST API request form. The user can either use the join_a_guild GET method or the POST method (where the user can add some JSON text. Both of those will be send to Kafka through the log_to_kafka function and will return a message to the user.
    """
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
    """
    We provide a GET and a POST API request form. The user can either use the get_coins GET method (and choose a number of coins) or the POST method (where the user can add some JSON text. Both of those will be send to Kafka through the log_to_kafka function and will return a message to the user.
    """
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
            return "Get " + json.dumps(request.json)[9:-1] + " coins\n"
