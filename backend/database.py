import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["opsflowhub"]

users_collection = db["users"]
upload_registry = db["upload_registry"]
revenue_collection = db["uploads_revenue"]
op_collection = db["uploads_op"]
ip_collection = db["uploads_ip"]
