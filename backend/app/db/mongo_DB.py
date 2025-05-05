from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from app.core.config import settings

# MongoDB client instance
client = None

# Database and collections
db = None
users_collection = None

def connect_to_mongo():
    """Initialize MongoDB connection"""
    global client, db, users_collection
    
    # Create MongoDB client
    client = MongoClient(settings.MONGODB_URL)
    
    # Get database
    db_name = settings.MONGODB_URL.split("/")[-1].split("?")[0]
    db = client[db_name]
    
    # Access collections
    users_collection = db.users
    
    # Create indexes for faster queries
    users_collection.create_index("username", unique=True)
    users_collection.create_index("email", unique=True)
    
    return db

def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()

def get_users_collection() -> Collection:
    """Get users collection"""
    global users_collection
    return users_collection

def get_database() -> Database:
    """Get database instance"""
    global db
    return db