import os
import warnings
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    warnings.warn("SECRET_KEY environment variable is not set; using insecure default.", stacklevel=1)
    secret_key = "dev-secret-key"
app.config["SECRET_KEY"] = secret_key

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
db = client.get_database("formation_ia")


@app.route("/")
def index():
    return {"status": "ok"}


@app.route("/health")
def health():
    try:
        client.admin.command("ping")
        return {"status": "healthy", "db": "connected"}
    except Exception:
        return {"status": "unhealthy", "db": "disconnected"}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
