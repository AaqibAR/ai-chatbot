from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Conversation, Package, FAQ
from schemas import MessageInput, MessageResponse, PackageSchema, FAQSchema
from chatbot import get_response
from datetime import datetime
from typing import List

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
    bot_response = get_response(user_message, db)

    conversation = Conversation(
        user_input=user_message,
        bot_response=bot_response
    )
    db.add(conversation)
    db.commit()

    return MessageResponse(response=bot_response, timestamp=datetime.now())

@app.get("/packages", response_model=List[PackageSchema])
def get_packages(db: Session = Depends(get_db)):
    return db.query(Package).all()

@app.get("/faqs", response_model=List[FAQSchema])
def get_faqs(db: Session = Depends(get_db)):
    return db.query(FAQ).all()

@app.get("/conversations")
def get_conversations(db: Session = Depends(get_db)):
    conversations = db.query(Conversation).order_by(Conversation.timestamp.desc()).limit(50).all()
    return conversations

from models import UnknownQuery

@app.get("/unknown-queries")
def get_unknown_queries(db: Session = Depends(get_db)):
    return db.query(UnknownQuery).filter(UnknownQuery.resolved == 0).all()

@app.post("/learn")
def learn(data: dict, db: Session = Depends(get_db)):
    query_id = data.get("id")
    answer = data.get("answer")
    question = data.get("question")

    # Save as new FAQ so bot learns it
    new_faq = FAQ(question=question, answer=answer)
    db.add(new_faq)

    # Mark unknown query as resolved
    unknown = db.query(UnknownQuery).filter(UnknownQuery.id == query_id).first()
    if unknown:
        unknown.resolved = 1
        unknown.suggested_answer = answer

    db.commit()
    return {"message": "Bot has learned a new response!"}

@app.get("/unknown-queries")
def get_unknown_queries(db: Session = Depends(get_db)):
    return db.query(UnknownQuery).filter(UnknownQuery.resolved == 0).all()

@app.get("/auto-learned")
def get_auto_learned(db: Session = Depends(get_db)):
    return db.query(UnknownQuery).filter(UnknownQuery.resolved == 1).all()