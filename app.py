from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, verify_jwt_in_request
from dotenv import load_dotenv
import os
from extensions import db, jwt

# Load Environment Vars
load_dotenv()

# Flask App Init
app = Flask(__name__)

# Config: SQLAlchemy + JWT via Cookies
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_COOKIE_HTTPONLY"] = True
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_COOKIE_SAMESITE"] = "Lax"

# Initialize Extensions
db.init_app(app)
jwt.init_app(app)

# Deferred Imports
from models import Product
from auth import auth_bp

# Register Blueprints
app.register_blueprint(auth_bp)

# Public API Route
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/logout")
def logout_page():
    response = redirect("/login")
    unset_jwt_cookies(response)
    return response

# Public API Route
@app.route("/products")
def get_products():
    products = Product.query.all()
    return render_template("products.html", products=products)


# Protected API Route
@app.route("/profile")
@jwt_required()
def profile():
    user = get_jwt_identity()
    return render_template("profile.html", user=user)


@app.context_processor
def inject_user():
    try:
        verify_jwt_in_request(optional=True)
        user = get_jwt_identity()
    except:
        user = None
    return {'user': user}

# Application Entrypoint
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False, host="0.0.0.0")

