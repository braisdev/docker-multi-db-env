import os
from pymongo import MongoClient

MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME", "root")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "rootpass")
MONGO_HOST = os.getenv("MONGO_HOST", "127.0.0.1")  # Adjusted for localhost
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DATABASE", "mydb")  # <--- Add this line!

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"

client = MongoClient(MONGO_URI)

def get_mongo_client():
    """FastAPI dependency that yields a MongoDB client."""
    return client
