import os
from dotenv import load_dotenv

class Config:
    # General Configurations
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database Configurations
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db') 

    TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'default_tmdb_api_key') 

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory DB for testing
