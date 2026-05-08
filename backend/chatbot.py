import re

# Knowledge base - static responses
INTENTS = {
    "greeting": {
        "patterns": ["hi", "hello", "hey", "good morning", "good evening"],
        "response": "Hello! Welcome to the Travel Assistant. How can I help you today?"
    },
    "packages": {
        "patterns": ["packages", "offers", "deals", "tours", "what do you offer"],
        "response": "We offer 3 exciting packages: 1) Kandy Tour 2) Ella Adventure 3) Sigiriya Explorer. Which one interests you?"
    },
    "kandy": {
        "patterns": ["kandy", "tell me about kandy", "kandy package"],
        "response": "The Kandy package includes: Hotel stay (3 nights), Temple of the Tooth visit, Kandy Lake walk, and transport. Price: $150"
    },
    "ella": {
        "patterns": ["ella", "tell me about ella", "ella package"],
        "response": "The Ella package includes: Hotel stay (2 nights), Nine Arch Bridge visit, Little Adam's Peak hike, and transport. Price: $120"
    },
    "sigiriya": {
        "patterns": ["sigiriya", "tell me about sigiriya", "sigiriya package"],
        "response": "The Sigiriya package includes: Hotel stay (2 nights), Sigiriya Rock Fortress climb, Dambulla Cave Temple, and transport. Price: $130"
    },
    "price": {
        "patterns": ["price", "cost", "how much", "fee", "charge"],
        "response": "Our packages start from $120. Kandy: $150, Ella: $120, Sigiriya: $130. Would you like more details on any package?"
    },
    "booking": {
        "patterns": ["book", "reserve", "booking", "i want to go", "sign up"],
        "response": "Great choice! To book a package, please provide your name, email, and preferred travel date. Our team will contact you within 24 hours."
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you", "thanks", "thank you"],
        "response": "Thank you for visiting! Have a wonderful trip. Goodbye! 👋"
    }
}

def preprocess(text: str) -> str:
    return text.lower().strip()

def detect_intent(text: str) -> str:
    text = preprocess(text)
    for intent, data in INTENTS.items():
        for pattern in data["patterns"]:
            if pattern in text:
                return intent
    return "unknown"

def get_response(message: str) -> str:
    intent = detect_intent(message)
    if intent == "unknown":
        return "I'm sorry, I didn't understand that. You can ask me about our travel packages, prices, or bookings!"
    return INTENTS[intent]["response"]