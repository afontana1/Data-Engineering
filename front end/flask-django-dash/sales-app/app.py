import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

load_dotenv(".env")
db = SQLAlchemy()
app = Flask(__name__)
app.logger.setLevel("INFO")
Bootstrap(app)
host = os.environ.get("SALES_DB_HOST")
port = os.environ.get("SALES_DB_PORT")
db_name = os.environ.get("SALES_DB_NAME")
user = os.environ.get("SALES_DB_USER")
password = os.environ.get("SALES_DB_PASS")
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
app.config["SQLALCHEMY_ECHO"] = eval(os.environ.get("LOG_SQL_QUERIES", "False"))
db.init_app(app)

from routes import users, courses
from models.user import User


@app.route("/")
def hello_world():
    # rec = db.get_or_404(User, 1)
    return redirect(url_for("users"))
