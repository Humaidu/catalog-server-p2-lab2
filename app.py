from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set up SQLAlchemy using the DATABASE_URL environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db = SQLAlchemy(app)

# Define the Product model representing the 'products' table
class Product(db.Model):
    __tablename__ = 'products' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)

# Default route for health check
@app.route("/")
def index():
    return "Welcome to the Catalog API"

# Endpoint to fetch all product records as JSON
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price
        } 
        for p in products
    ])

if __name__ == "__main__":
    # Ensure the database tables exist
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
