#!/usr/bin/env python
from kafka import KafkaProducer
from flask import Flask

# We use this for producing request from the server that could be use for personalize the options of our events
from flask import request

app = Flask(__name__)
event_logger = KafkaProducer(bootstrap_servers="kafka:29092")
events_topic = "userItems"


@app.route("/")
def default_response():
    # We already are encoding the Flask response as binary message for Kafka
    event_logger.send(events_topic, "default".encode())
    return "This is the default response! \n"


@app.route("/purchase_a_sword")
def purchase_sword():
    # Event Logic of Buying a Sword, it will use a request from the web server for giving it an attribute, in our case, color. This
    # will be played throughtout the project
    # We will also log the event to Kafka
    if "color" in request.args:
        event_logger.send(
            events_topic, "purchase_a_sword" + request.args["color"].encode()
        )
        return "Sword Purchased" + " " + request.args["color"] + "\n"
    else:
        event_logger.send(events_topic, "purchase_a_sword".encode())
        return "Sword Purchased \n"


@app.route("/join_a_guild")
def join_guild():
    # Event logic of joining a Guild. For the next assignment, we will define the state of joining a guild
    # log event to kafka
    event_logger.send(events_topic, "join_guild".encode())
    return "Join a guild! \n"


@app.route("/get_coins")
def get_coins():
    # Event logic og earning coins from a mission. Next steps: keep track of amount of coins and relate sword prices with coins in wallet
    # log event to kafka
    if "number" in request.args:
        event_logger.send(events_topic, "get_coins" + request.args["number"].encode())
        return "Get " + request.args["number"] + " coins \n"
    else:
        event_logger.send(events_topic, "get_coins".encode())
        return "Get coins \n"
