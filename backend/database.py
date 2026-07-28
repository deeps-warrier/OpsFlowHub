from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["opsflowhub"]

users_collection = db["users"]
upload_registry = db["upload_registry"]
revenue_collection = db["uploads_revenue"]
op_collection = db["uploads_op"]
ip_collection = db["uploads_ip"]
