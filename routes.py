from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db 
from forms import RegisterForm, LoginForm
import requests
from config import Config
from utils.recommendation_engine import recommend_movies, create_user_item_matrix, calculate_similarity
from utils.sentiment_analysis import analyze_sentiments, highlight_positive_reviews

def setup_routes(app):
    # TMDb API Utilities
    def fetch_popular_movies():
        """Fetch popular movies from TMDb API."""
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={Config.TMDB_API_KEY}&language=en-US&page=1"
        response = requests.get(url)
        return response.json().get('results', [])

    def fetch_movie_details(movie_id):
        """Fetch detailed movie information, including trailers and reviews."""
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={Config.TMDB_API_KEY}&append_to_response=videos,credits,reviews"
        response = requests.get(url)
        return response.json()

    def fetch_reviews(movie_id):
        """Fetch movie reviews dynamically."""
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={Config.TMDB_API_KEY}"
        response = requests.get(url)
        return response.json().get('results', [])

    @app.route('/')
    def index():
        """Render the home page with popular movies."""
        movies = fetch_popular_movies()
        return render_template('index.html', movies=movies)

    @app.route('/search', methods=['GET'])
    def search():
        """Search for movies based on user query."""
        query = request.args.get('query', '')
        if not query:
            flash('Please enter a search term!', 'warning')
            return redirect(url_for('index'))
        
        url = f"https://api.themoviedb.org/3/search/movie?api_key={Config.TMDB_API_KEY}&query={query}"
        response = requests.get(url).json()
        movies = response.get('results', [])
        return render_template('search_results.html', movies=movies, query=query)

    @app.route('/movie/<int:movie_id>')
    def movie_details(movie_id):
        """Display detailed information about a movie, recommendations, and reviews."""
        movie = fetch_movie_details(movie_id)

        # Fetch the first trailer
        trailer = None
        for video in movie.get('videos', {}).get('results', []):
            if video['type'] == "Trailer":
                trailer = video
                break

        # Recommendations based on content or user preferences
        recommendations = []
        if current_user.is_authenticated:
            try:
                user_item_matrix = create_user_item_matrix()
                similarity_matrix = calculate_similarity(user_item_matrix)
                recommendations = recommend_movies(current_user.id, user_item_matrix, similarity_matrix)
            except Exception as e:
                print(f"Recommendation error: {e}")
        else:
            recommendations = []  # No personalized recommendations for guests

        # Fallback: Provide similar content-based recommendations
        if not recommendations:
            recommendations = [{"title": "No recommendations available"}]  # Default fallback

        # Perform sentiment analysis on reviews
        reviews = fetch_reviews(movie_id)
        sentiments = analyze_sentiments(reviews) if reviews else []
        positive_reviews = highlight_positive_reviews(sentiments)

        return render_template(
            'movie_details.html',
            movie=movie,
            trailer=trailer,
            recommendations=recommendations,
            positive_reviews=positive_reviews
        )

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Handle user registration."""
        form = RegisterForm()
        if form.validate_on_submit():
                hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
                new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)

                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Registration successful. Please log in.', 'success')
                    return redirect(url_for('login'))
                except Exception as e:
                    db.session.rollback()  # Rollback in case of errors
                    print(f"Error during registration: {e}")
                    flash('An error occurred during registration. Please try again.', 'danger')

        return render_template('register.html', form=form)
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Handle user login."""
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()  # Fetch user by email
            # Corrected the comparison logic
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)  # Log the user in
                flash('Logged in successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        """Handle user logout."""
        logout_user()
        flash('Logged out successfully.', 'success')
        return redirect(url_for('index'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        """Render the user dashboard."""
        return render_template('dashboard.html', username=current_user.username)

    @app.route('/recommendations/<int:user_id>')
    @login_required
    def recommendations(user_id):
        """Generate personalized recommendations for the logged-in user."""
        user_item_matrix = create_user_item_matrix()
        similarity_matrix = calculate_similarity(user_item_matrix)
        recommended_movies = recommend_movies(user_id, user_item_matrix, similarity_matrix)

        movie_details = [
            fetch_movie_details(movie_id) for movie_id in recommended_movies.index
        ]

        return render_template('recommendations.html', recommendations=movie_details)
