from app import db, Product, app

with app.app_context():
    db.create_all()  # Ensures table exists
    if not Product.query.first():
        products = [
            Product(name="Laptop", description="Powerful laptop", price=1200.0),
            Product(name="Smartphone", description="Android phone", price=800.0),
            Product(name="Tablet", description="10-inch screen", price=400.0)
        ]
        db.session.add_all(products)
        db.session.commit()
        print("Sample products inserted.")
    else:
        print("Products already exist. Skipping seeding.")
