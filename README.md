# AI Travel Chatbot 🌍✈️

An AI-powered travel assistant chatbot built with React, FastAPI, and PostgreSQL.

## Tech Stack

- **Frontend:** React + Vite + CSS
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL + SQLAlchemy
- **NLP:** spaCy (lemmatization + intent detection)

## System Architecture

This project follows a 3-tier architecture:

1. **Natural Language Interface** — React chat UI
2. **Inference Engine** — spaCy NLP intent detection
3. **Knowledge Base** — PostgreSQL database

## Features

- Natural language understanding using spaCy
- Intent detection with lemmatization and keyword scoring
- Travel package information (Kandy, Ella, Sigiriya)
- Conversation logging to PostgreSQL
- Typing indicator and smooth chat UI
- RESTful API with FastAPI

## Prerequisites

- Node.js 18+
- Python 3.10+
- PostgreSQL 16+

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/AaqibAR/ai-chatbot.git
cd ai-chatbot
```

### 2. Backend setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn spacy scikit-learn psycopg2-binary sqlalchemy python-dotenv
python -m spacy download en_core_web_sm
```

### 3. Configure environment
Copy `.env.example` to `.env` and update with your PostgreSQL credentials:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=chatbot_db
DB_USER=your_username
DB_PASSWORD=your_password

### 4. Create database and seed data
```bash
psql postgres -c "CREATE DATABASE chatbot_db;"
python seed.py
```

### 5. Run the backend
```bash
uvicorn main:app --reload
```

### 6. Frontend setup
```bash
cd ../frontend
npm install
npm run dev
```

### 7. Open the app
Visit `http://localhost:5173`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/chat` | Send a message and get a response |

## Example Conversations

| User Input | Bot Response |
|------------|-------------|
| "Hello" | Greeting response |
| "Show me packages" | Lists all 3 packages |
| "Tell me about Kandy" | Kandy package details |
| "How much does it cost?" | Price list |
| "I want to book" | Booking instructions |

## Database Schema

- **packages** — Travel package details
- **faqs** — Frequently asked questions
- **conversations** — Logs all user interactions

## Project Structure

ai-chatbot/
├── backend/
│   ├── main.py         # FastAPI app and routes
│   ├── chatbot.py      # NLP inference engine
│   ├── database.py     # PostgreSQL connection
│   ├── models.py       # Database models
│   ├── schemas.py      # Request/response schemas
│   └── seed.py         # Database seeder
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── components/
│           ├── ChatWindow.jsx
│           └── ChatInput.jsx
└── README.md