from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import nltk
from models import User  # Import your models
from routes import setup_routes  # Import route setup function
from extensions import db
from config import DevelopmentConfig

login_manager = LoginManager()

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    # App configuration
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(DevelopmentConfig)

    # Initialize extensions with the app
    db.init_app(app)
    
    login_manager.init_app(app)

    # Configure LoginManager
    login_manager.login_view = 'login'
    
    # Set up routes
    setup_routes(app)

    # Set up the user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Fetch user from database

    # Ensure required NLTK resources
    ensure_nltk_resources()
    
    @app.route('/')
    def home():
        return "App Running!"
    
    return app

def ensure_nltk_resources():
    nltk.download('vader_lexicon', quiet=True)

if __name__ == "__main__":
    # Create the app
    app = create_app()

    # Use app context to create database tables
    with app.app_context():
        db.create_all()  # Ensure all tables are created
        print("Database tables created.")

    # Run the Flask app
    app.run(debug=True)

