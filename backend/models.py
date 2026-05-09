from sqlalchemy import Column, Integer, String, Text, DateTime, DECIMAL
from sqlalchemy.sql import func
from database import Base

class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    price = Column(DECIMAL)
    location = Column(String(100))

class FAQ(Base):
    __tablename__ = "faqs"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text)
    bot_response = Column(Text)
    timestamp = Column(DateTime, default=func.now())

class UnknownQuery(Base):
    __tablename__ = "unknown_queries"
    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text)
    suggested_answer = Column(Text, nullable=True)
    frequency = Column(Integer, default=1)
    resolved = Column(Integer, default=0)
    timestamp = Column(DateTime, default=func.now())