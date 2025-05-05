from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from app.core.config import settings
from app.api import auth
from app.db.mongo_DB import connect_to_mongo, close_mongo_connection
from app.core.middleware import AuthMiddleware

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.middleware("http")(AuthMiddleware())

# Include API routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

# Connect to MongoDB on startup
@app.on_event("startup")
async def startup_db_client():
    connect_to_mongo()

# Close MongoDB connection on shutdown
@app.on_event("shutdown")
async def shutdown_db_client():
    close_mongo_connection()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Futuristic Auth System API",
        "version": "1.0.0",
        "docs_url": f"{settings.API_V1_STR}/docs"
    }

# Run the application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )