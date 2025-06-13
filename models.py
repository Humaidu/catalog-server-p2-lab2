from extensions import db

# Product model for catalog items
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        # Serialize object to dictionary
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
        }

# Simple User model for demonstration
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # Plaintext here; hash in prod

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
        }

