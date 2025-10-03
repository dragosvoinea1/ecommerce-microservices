import os
import json
from typing import List, Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, db

# --- Config & Setup ---
models.Base.metadata.create_all(bind=db.engine)
app = FastAPI(title="Notifications Service")

# --- WebSocket Connection Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_email: str):
        await websocket.accept()
        self.active_connections[user_email] = websocket

    def disconnect(self, user_email: str):
        if user_email in self.active_connections:
            del self.active_connections[user_email]

    async def send_personal_message(self, message: str, user_email: str):
        if user_email in self.active_connections:
            await self.active_connections[user_email].send_text(message)

manager = ConnectionManager()

def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()

# --- API Endpoints ---

# Endpoint la care se va conecta frontend-ul
@app.websocket("/ws/{user_email}")
async def websocket_endpoint(websocket: WebSocket, user_email: str):
    await manager.connect(websocket, user_email)
    try:
        while True:
            await websocket.receive_text() # Păstrăm conexiunea deschisă
    except WebSocketDisconnect:
        manager.disconnect(user_email)

# Endpoint intern, apelat de alte servicii
@app.post("/send-notification/{user_email}")
async def send_notification(
    user_email: str,
    payload: dict,
    db: Session = Depends(get_db)
):
    message = payload.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    # 1. Salvăm notificarea în baza de date
    db_notification = models.DBNotification(user_email=user_email, message=message)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    # 2. Trimitem notificarea prin WebSocket dacă utilizatorul e online
    await manager.send_personal_message(json.dumps({"message": message}), user_email)

    return {"status": "Notification sent"}

# Endpoint pentru a prelua istoricul notificărilor
@app.get("/notifications/{user_email}", response_model=List[models.Notification])
def get_notifications(user_email: str, db: Session = Depends(get_db)):
    notifications = db.query(models.DBNotification).filter(models.DBNotification.user_email == user_email).order_by(models.DBNotification.created_at.desc()).all()
    return notifications