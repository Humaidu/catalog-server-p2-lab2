from app import db, Product, app

# Use the Flask app context to allow database operations outside of a request
with app.app_context():
    # Create all tables defined in SQLAlchemy models (if not already created)
    db.create_all()  # Ensures the 'products' table exists in the database

    # Check if any products already exist in the database
    if not Product.query.first():
        # Define a list of sample Product instances to seed the database
        products = [
            Product(name="Laptop", description="Powerful laptop", price=1200.0),
            Product(name="Smartphone", description="Android phone", price=800.0),
            Product(name="Tablet", description="10-inch screen", price=400.0)
        ]

        # Add all product instances to the current database session
        db.session.add_all(products)

        # Commit the session to persist changes (insert products into the DB)
        db.session.commit()

        # Print a confirmation message to the console
        print("Sample products inserted.")
    else:
        # If products already exist, skip seeding and notify the user
        print("Products already exist. Skipping seeding.")

