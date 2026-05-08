import spacy

nlp = spacy.load("en_core_web_sm")

INTENTS = {
    "greeting": {
        "keywords": ["hi", "hello", "hey", "morning", "evening", "greet"],
        "response": "Hello! Welcome to the Travel Assistant. How can I help you today? 🌍"
    },
    "packages": {
        "keywords": ["package", "offer", "deal", "tour", "option", "available"],
        "response": "We offer 3 exciting packages:\n1) Kandy Tour - $150\n2) Ella Adventure - $120\n3) Sigiriya Explorer - $130\nWhich one interests you?"
    },
    "kandy": {
        "keywords": ["kandy", "tooth", "lake"],
        "response": "The Kandy package includes:\n- 3 nights hotel stay\n- Temple of the Tooth visit\n- Kandy Lake walk\n- Transport included\nPrice: $150 per person"
    },
    "ella": {
        "keywords": ["ella", "arch", "bridge", "adam", "peak", "hike"],
        "response": "The Ella package includes:\n- 2 nights hotel stay\n- Nine Arch Bridge visit\n- Little Adam's Peak hike\n- Transport included\nPrice: $120 per person"
    },
    "sigiriya": {
        "keywords": ["sigiriya", "rock", "fortress", "dambulla", "cave"],
        "response": "The Sigiriya package includes:\n- 2 nights hotel stay\n- Sigiriya Rock Fortress climb\n- Dambulla Cave Temple\n- Transport included\nPrice: $130 per person"
    },
    "price": {
        "keywords": ["price", "cost", "much", "fee", "charge", "expensive", "cheap", "afford"],
        "response": "Our packages start from $120:\n- Kandy: $150\n- Ella: $120\n- Sigiriya: $130\nAll prices include hotel and transport. Would you like to book one?"
    },
    "booking": {
        "keywords": ["book", "reserve", "booking", "sign", "register", "want", "go", "travel"],
        "response": "Great choice! To book a package, please provide:\n- Your full name\n- Email address\n- Preferred travel date\nOur team will contact you within 24 hours! ✈️"
    },
    "goodbye": {
        "keywords": ["bye", "goodbye", "see", "thanks", "thank", "appreciate"],
        "response": "Thank you for visiting! Have a wonderful trip. Goodbye! 👋"
    }
}

def preprocess(text: str):
    doc = nlp(text.lower())
    # Lemmatize and remove stopwords/punctuation
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return tokens

def detect_intent(text: str) -> str:
    tokens = preprocess(text)
    scores = {}

    for intent, data in INTENTS.items():
        score = 0
        for token in tokens:
            if token in data["keywords"]:
                score += 1
        if score > 0:
            scores[intent] = score

    if not scores:
        return "unknown"

    # Return intent with highest score
    return max(scores, key=scores.get)

def get_response(message: str) -> str:
    intent = detect_intent(message)
    if intent == "unknown":
        return "I'm sorry, I didn't understand that. You can ask me about our travel packages, prices, or bookings! 😊"
    return INTENTS[intent]["response"]