import os
from dotenv import load_dotenv
from flask import Flask
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

load_dotenv(".env")
db = SQLAlchemy()
app = Flask(__name__)
swagger = Swagger(app)
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

from routes import user_routes
from routes import course_routes
from routes import order_routes


@app.route("/")
def hello_world():
    return {"message": "Hello World from itversity"}
