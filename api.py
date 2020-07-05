import os
from flask import (
    Flask,
    url_for,
    redirect,
)
from models import db

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Set up databasee
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    return redirect(url_for("api"))


@app.route("/shortlinks")
def api():
    return "api"


def main():
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        main()
