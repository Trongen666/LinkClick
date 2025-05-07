"""
MongoDB connection and initialization.
"""
import logging
from datetime import datetime
import motor.motor_asyncio
from pymongo import IndexModel, ASCENDING, TEXT, DESCENDING
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# MongoDB connection
try:
    client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.MONGODB_URI,
        serverSelectionTimeoutMS=5000  # 5 second timeout for initial connection
    )
    # Force a connection to verify it works
    client.admin.command('ping')
    logger.info("Connected to MongoDB successfully")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

database = client[settings.DATABASE_NAME]

# Collections
users_collection = database.users
otp_collection = database.otp
login_attempts_collection = database.login_attempts
sessions_collection = database.sessions

async def create_indexes():
    """Create all necessary database indexes"""
    try:
        # Users collection indexes
        await users_collection.create_indexes([
            IndexModel([("username", ASCENDING)], unique=True),
            IndexModel([("phone_number", ASCENDING)]),
            IndexModel([("is_active", ASCENDING)]),
            IndexModel([("is_admin", ASCENDING)])
        ])
        
        # OTP collection indexes
        await otp_collection.create_indexes([
            IndexModel([("username", ASCENDING)], unique=True),
            IndexModel([("expires_at", ASCENDING)], expireAfterSeconds=0)  # TTL index
        ])
        
        # Login attempts collection indexes
        await login_attempts_collection.create_indexes([
            IndexModel([("username", ASCENDING)]),
            IndexModel([("ip_address", ASCENDING)]),
            IndexModel([("timestamp", DESCENDING)]),
            IndexModel([("timestamp", ASCENDING)], expireAfterSeconds=7*24*60*60)  # Auto-expire after 7 days
        ])
        
        # Sessions collection indexes
        await sessions_collection.create_indexes([
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("token", ASCENDING)], unique=True),
            IndexModel([("expires_at", ASCENDING)], expireAfterSeconds=0)  # TTL index
        ])
        
        logger.info("All database indexes created successfully")
    except Exception as e:
        logger.error(f"Error creating database indexes: {str(e)}")
        raise

async def create_admin_user():
    """Create admin user if it doesn't exist"""
    admin_exists = await users_collection.find_one({"username": "admin", "is_admin": True})
    if not admin_exists:
        try:
            await users_collection.insert_one({
                "username": "admin",
                "phone_number": settings.ADMIN_PHONE_NUMBER,
                "is_active": True,
                "is_admin": True,
                "face_embedding": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            logger.info("Admin user created successfully")
        except Exception as e:
            logger.error(f"Error creating admin user: {str(e)}")
            raise

async def init_db():
    """Initialize database with indexes and default data"""
    try:
        logger.info("Initializing database...")
        await create_indexes()
        await create_admin_user()
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise