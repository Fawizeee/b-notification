from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for notifications
notifications = []

class NotificationRequest(BaseModel):
    message: str
@app.get("/")
async def home():
    return {"success":"yes"}
@app.post("/notify")
async def notify(request: NotificationRequest):
    logger.info(f"Received notification request: {request.message}")
    # Store the notification
    notification = {
        "message": request.message,
        "timestamp": datetime.utcnow().isoformat()
    }
    notifications.append(notification)
    return {"status": "notified", "message": request.message}

@app.get("/notifications")
async def get_notifications():
    return {"notifications": notifications}
