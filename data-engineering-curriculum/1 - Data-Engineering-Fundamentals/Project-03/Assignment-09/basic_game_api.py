#!/usr/bin/env python
from flask import Flask

app = Flask(__name__)
# Basic game API without sending messages to Kafka


@app.route("/")
def default_response():
    return "This is the default response! \n"


@app.route("/purchase_a_sword")
def purchase_sword():
    # business logic to purchase sword
    return "Sword Purchased! \n"


@app.route("/join_a_guild")
def join_guild():
    # business logic to join a guild
    return "Guild joined! \n"


@app.route("/get_coins")
def get_coins():
    # business logic to get coins
    return "Get coins! \n"
