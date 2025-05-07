from fastapi import FastAPI
from app.routes import notification_route

app = FastAPI()

app.include_router(notification_route.router)

@app.get("/")
def read_root():
    return {"message": "Senior Citizen Web Application - Backend Running"}