import spacy
import re
from sqlalchemy.orm import Session

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
    "keywords": ["faq", "faqs", "show", "question", "cancel", "cancellation", "discount", "group", "include", "policy"],
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
    "booking": "Great choice! Please provide the following details:\n- Your full name\n- Email address\n- Preferred travel date\n- Package of choice (Kandy, Ella, or Sigiriya)\n\nOnce submitted, we will review your details and contact you within 24 hours to confirm your booking! ✈️",
}

AUTO_LEARN_THRESHOLD = 3

def preprocess(text: str):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return tokens

def detect_intent(text: str) -> str:
    tokens = preprocess(text)
    scores = {}
    for intent, data in INTENTS.items():
        score = sum(1 for token in tokens if token in data["keywords"])
        if score > 0:
            scores[intent] = score
    return max(scores, key=scores.get) if scores else "unknown"

def find_similar_faq(message: str, db: Session):
    from models import FAQ
    doc1 = nlp(message.lower())
    faqs = db.query(FAQ).all()
    best_match = None
    best_score = 0.0
    for faq in faqs:
        doc2 = nlp(faq.question.lower())
        if doc1.has_vector and doc2.has_vector:
            score = doc1.similarity(doc2)
            if score > best_score:
                best_score = score
                best_match = faq
    if best_score > 0.6 and best_match:
        return best_match.answer
    return None

def auto_generate_response(user_input: str) -> str:
    tokens = preprocess(user_input)
    if any(t in tokens for t in ["hotel", "stay", "accommodation"]):
        return "All our packages include comfortable hotel accommodations. Prices vary by package and duration."
    if any(t in tokens for t in ["food", "meal", "eat", "restaurant"]):
        return "Sri Lanka offers amazing local cuisine! Most tour packages include breakfast. Local restaurants are available for other meals."
    if any(t in tokens for t in ["weather", "climate", "rain", "season"]):
        return "Sri Lanka has a tropical climate. Best time to visit is December-March for the west coast and May-September for the east coast."
    if any(t in tokens for t in ["visa", "passport", "entry"]):
        return "Most nationalities can obtain a Sri Lanka e-visa online before arrival. Visit www.eta.gov.lk for details."
    if any(t in tokens for t in ["transport", "bus", "train", "flight"]):
        return "All our packages include transport between destinations. Domestic flights and trains are also available."
    return None

def handle_unknown(message: str, db: Session) -> str:
    from models import UnknownQuery, FAQ

    existing = db.query(UnknownQuery).filter(
        UnknownQuery.user_input.ilike(f"%{message[:30]}%"),
        UnknownQuery.resolved == 0
    ).first()

    if existing:
        existing.frequency += 1
        if existing.frequency >= AUTO_LEARN_THRESHOLD:
            auto_answer = auto_generate_response(message)
            if auto_answer:
                new_faq = FAQ(
                    question=existing.user_input,
                    answer=auto_answer
                )
                db.add(new_faq)
                existing.resolved = 1
                existing.suggested_answer = auto_answer
                db.commit()
                return auto_answer
    else:
        new_unknown = UnknownQuery(user_input=message)
        db.add(new_unknown)

    db.commit()
    return "I'm sorry, I didn't understand that. Your question has been saved and I'll learn from it! 😊"

def get_response(message: str, db: Session) -> str:
    intent = detect_intent(message)

    # 1. Static responses first
    if intent in STATIC_RESPONSES:
        return STATIC_RESPONSES[intent]

    # 2. Check if message looks like booking details
    has_email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', message)
    has_date = re.search(r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}', message)
    line_count = len([l for l in message.strip().split('\n') if l.strip()])
    if has_email or has_date or line_count >= 3:
        return "Thank you! We have received your booking details successfully. Our team will contact you within 24 hours to confirm your reservation. We look forward to making your Sri Lanka trip memorable! 🌴✈️"

    # 3. Handle casual follow-up responses
    if message.lower().strip() in ["okay", "ok", "sure", "alright", "great", "noted", "fine", "got it"]:
        return "You're welcome! Feel free to ask if you have any more questions. We look forward to your visit! 😊"

    # 4. Dynamic DB responses
    if intent == "packages":
        from models import Package
        packages = db.query(Package).all()
        if packages:
            pkg_list = "\n".join([f"- {p.name}: LKR {p.price} ({p.location})" for p in packages])
            return f"We offer the following packages:\n{pkg_list}\n\nWhich one interests you?"

    if intent in ["kandy", "ella", "sigiriya"]:
        from models import Package
        package = db.query(Package).filter(
            Package.location.ilike(f"%{intent}%")
        ).first()
        if package:
            return f"{package.name}\n{package.description}\nPrice: LKR {package.price} per person"

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

    # 5. Search FAQs using spaCy similarity
    faq_match = find_similar_faq(message, db)
    if faq_match:
        return faq_match

    # 6. Handle unknown - save and auto-learn
    return handle_unknown(message, db)