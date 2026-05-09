import spacy

nlp = spacy.load("en_core_web_sm")

INTENTS = {
    "greeting": {
        "keywords": ["hi", "hello", "hey", "morning", "evening", "greet"],
        "response": None
    },
    "packages": {
        "keywords": ["package", "offer", "deal", "tour", "option", "available"],
        "response": None
    },
    "kandy": {
        "keywords": ["kandy", "tooth", "lake"],
        "response": None
    },
    "ella": {
        "keywords": ["ella", "arch", "bridge", "adam", "peak", "hike"],
        "response": None
    },
    "sigiriya": {
        "keywords": ["sigiriya", "rock", "fortress", "dambulla", "cave"],
        "response": None
    },
    "price": {
        "keywords": ["price", "cost", "much", "fee", "charge", "expensive", "cheap", "afford"],
        "response": None
    },
    "booking": {
        "keywords": ["book", "reserve", "booking", "sign", "register", "want", "go", "travel"],
        "response": None
    },
    "faq": {
        "keywords": ["faq", "question", "cancel", "cancellation", "discount", "group", "include", "policy"],
        "response": None
    },
    "goodbye": {
        "keywords": ["bye", "goodbye", "see", "thanks", "thank", "appreciate"],
        "response": None
    }
}

STATIC_RESPONSES = {
    "greeting": "Hello! Welcome to the Travel Assistant. How can I help you today? 🌍",
    "goodbye": "Thank you for visiting! Have a wonderful trip. Goodbye! 👋",
    "booking": "Great choice! To book a package, please provide:\n- Your full name\n- Email address\n- Preferred travel date\nOur team will contact you within 24 hours! ✈️",
}

def preprocess(text: str):
    doc = nlp(text.lower())
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

    return max(scores, key=scores.get)

def get_response(message: str, db) -> str:
    intent = detect_intent(message)

    # Static responses
    if intent in STATIC_RESPONSES:
        return STATIC_RESPONSES[intent]

    # Dynamic responses from database
    if intent == "packages":
        packages = db.query(__import__('models').Package).all()
        if packages:
            pkg_list = "\n".join([f"- {p.name}: LKR {p.price} ({p.location})" for p in packages])
            return f"We offer the following packages:\n{pkg_list}\n\nWhich one interests you?"

    if intent in ["kandy", "ella", "sigiriya"]:
        from models import Package
        package = db.query(Package).filter(
            Package.location.ilike(f"%{intent}%")
        ).first()
        if package:
            return f"**{package.name}**\n{package.description}\nPrice: LKR {package.price} per person"

    if intent == "price":
        from models import Package
        packages = db.query(Package).all()
        if packages:
            price_list = "\n".join([f"- {p.name}: LKR {p.price}" for p in packages])
            return f"Our package prices:\n{price_list}\n\nAll prices include hotel and transport!"

    if intent == "faq":
        from models import FAQ
        faqs = db.query(FAQ).limit(3).all()
        if faqs:
            faq_list = "\n\n".join([f"Q: {f.question}\nA: {f.answer}" for f in faqs])
            return f"Here are some frequently asked questions:\n\n{faq_list}"

    # Search FAQs in database for any match
    from models import FAQ
    all_faqs = db.query(FAQ).all()
    for faq in all_faqs:
        faq_tokens = preprocess(faq.question)
        for token in tokens:
            if token in faq_tokens:
                return faq.answer

    # Save unknown query for learning
    unknown = __import__('models').UnknownQuery(user_input=message)
    db.add(unknown)
    db.commit()

    return "I'm sorry, I didn't understand that. Your question has been saved and we'll improve our responses! 😊"