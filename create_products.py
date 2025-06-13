# seed.py

from app import app
from extensions import db
from models import User, Product

def seed_data():
    with app.app_context():
        # Create tables
        db.create_all()

        # Seed user if not exists
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", password="admin123")  # NOTE: Plaintext in dev only
            db.session.add(admin)
            print("✅ Admin user created.")

        # Optional: seed products
        if not Product.query.first():
            products = [
                Product(name="Laptop", description="A powerful machine", price=1200.00),
                Product(name="Headphones", description="Noise-cancelling", price=250.00),
                Product(name="Mouse", description="Wireless optical mouse", price=45.50)
            ]
            db.session.add_all(products)
            print("✅ Sample products added.")

        db.session.commit()
        print("🎉 Database seeding complete.")

if __name__ == "__main__":
    seed_data()

