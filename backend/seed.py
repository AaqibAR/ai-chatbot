from database import SessionLocal, engine, Base
from models import Package, FAQ, Conversation

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear existing data
db.query(Package).delete()
db.query(FAQ).delete()

# Seed packages
packages = [
    Package(name="Kandy Tour", description="Visit the Temple of the Tooth, Kandy Lake, and enjoy the cultural heart of Sri Lanka.", price=150.00, location="Kandy"),
    Package(name="Ella Adventure", description="Hike Little Adam's Peak, visit Nine Arch Bridge, and enjoy stunning mountain views.", price=120.00, location="Ella"),
    Package(name="Sigiriya Explorer", description="Climb the famous Sigiriya Rock Fortress and visit the Dambulla Cave Temple.", price=130.00, location="Sigiriya"),
]

# Seed FAQs
faqs = [
    FAQ(question="What is included in the packages?", answer="All packages include hotel stay, transport, and guided tours."),
    FAQ(question="How do I book a package?", answer="Provide your name, email and preferred date. Our team will contact you within 24 hours."),
    FAQ(question="What is the cheapest package?", answer="The Ella Adventure package is our most affordable at $120 per person."),
    FAQ(question="Do you offer group discounts?", answer="Yes! Groups of 5 or more receive a 10% discount on all packages."),
    FAQ(question="What is the cancellation policy?", answer="Free cancellation up to 7 days before travel. 50% refund within 3-7 days."),
]

db.add_all(packages)
db.add_all(faqs)
db.commit()
db.close()

print("✅ Database seeded successfully!")
print(f"   - {len(packages)} packages added")
print(f"   - {len(faqs)} FAQs added")