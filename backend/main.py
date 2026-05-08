from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Conversation
from schemas import MessageInput, MessageResponse
from chatbot import get_response
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Chatbot API is running"}

@app.post("/chat", response_model=MessageResponse)
def chat(input: MessageInput, db: Session = Depends(get_db)):
    user_message = input.message
    bot_response = get_response(user_message)

    # Save to database
    conversation = Conversation(
        user_input=user_message,
        bot_response=bot_response
    )
    db.add(conversation)
    db.commit()

    return MessageResponse(response=bot_response, timestamp=datetime.now())