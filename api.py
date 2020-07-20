import os
from flask import (
    Flask,
    url_for,
    redirect,
    request,
    jsonify,
)
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from helpers import generate_slug, valid_schema, save_url

app = Flask(__name__)

# load configuration from .env file
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

        try:
            ios_primary = request.json["ios"]["primary"]
            ios_fallback = request.json["ios"]["fallback"]
            android_primary = request.json["android"]["primary"]
            android_fallback = request.json["android"]["fallback"]
            web = request.json["web"]
            slug = request.json["slug"] or ""

            # if any of the urls is invalid
            if not valid_schema(
                ios_primary=ios_primary,
                ios_fallback=ios_fallback,
                android_primary=android_primary,
                android_fallback=android_fallback,
                web=web,
            ):
                return jsonify({"bad request": 400}), 400

            # if slug was not specified, generate it
            if not slug:
                slug = generate_slug(6)

            # saves the valid url in db
            save_url(
                slug=slug,
                ios_primary=ios_primary,
                ios_fallback=ios_fallback,
                android_primary=android_primary,
                android_fallback=android_fallback,
                web=web,
                db=db,
            )

            return jsonify("url created successfully"), 200

        except KeyError as e:
            # if the slug key wasn't provided, generate it
            if str(e.args[0]) == "slug":
                slug = generate_slug(6)
                save_url(
                    slug=slug,
                    ios_primary=ios_primary,
                    ios_fallback=ios_fallback,
                    android_primary=android_primary,
                    android_fallback=android_fallback,
                    web=web,
                    db=db,
                )
                return (
                    jsonify(
                        {
                            "success": True,
                            "message": "url and its slug created successfully",
                        }
                    ),
                    200,
                )
            else:
                return (
                    jsonify({"success": False, "message": "bad request"}),
                    400,
                )

    if request.method == "GET":

        urls = db.execute(
            "SELECT slug, \
                            ios_primary_url, \
                            ios_fallback_url, \
                            android_primary_url, \
                            android_fallback_url, \
                            web_url \
                            FROM urls"
        ).fetchall()
        print(type(urls))
        print(urls)
        return jsonify({"urls": [dict(url) for url in urls]})
