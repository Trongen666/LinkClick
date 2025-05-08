"""
Main FastAPI application.
"""
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users
from app.utils.db import init_db

from app.routers import db_test


# Create FastAPI application
app = FastAPI(
    title="Authentication System",
    description="Authentication system with face recognition and OTP",
    version="1.0.0"
)

app.include_router(db_test.router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You should restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)

@app.on_event("startup")
async def startup_event():
    """
    Initialize database on startup
    """
    print("\n--- All registered routes ---")
    for route in app.routes:
        print(route.path, route.name)
#    await init_db()

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Authentication System API",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)