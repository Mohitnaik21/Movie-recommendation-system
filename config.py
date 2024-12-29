import os

class Config:
    # General Configurations
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')  # Replace with a secure key in production
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database Configurations
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db')  # Default to SQLite for local dev

    # API Keys (e.g., TMDb API)
    TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'bb7804f8f451595866609ee97b01261c')  

class DevelopmentConfig(Config):
    DEBUG = True

# class ProductionConfig(Config):
#     DEBUG = False
#     SECRET_KEY = os.getenv('SECRET_KEY', 'production_secret_key')  # Use a secure secret key in production

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory DB for testing
