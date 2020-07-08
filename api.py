import os
from flask import (
    Flask,
    url_for,
    redirect,
    request,
)
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from helpers import generate_slug

app = Flask(__name__)

# load configuration for .env file
APP_ROOT = os.path.dirname(__file__)
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)

# Check for db environment variable
if not os.getenv("DATABASE_URI"):
    raise RuntimeError("DATABASE_URI is not set")


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Set up databasee
engine = create_engine(os.getenv("DATABASE_URI"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return redirect(url_for("api"))


@app.route("/shortlinks", methods=["POST", "GET"])
def api():
    if request.method == "POST":
        return f"post request: {request.json}"

    if request.method == "GET":
        return "get request"

    return "Test", 200
