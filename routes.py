from flask import render_template, redirect, url_for, flash, request,jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Review, Favorite
from extensions import db 
from forms import RegisterForm, LoginForm
import requests
from config import Config
from utils.recommendation_engine import get_similar_movies
from utils.sentiment_analysis import analyze_sentiments
from utils.content_based_filtering import get_similar_movies
from utils.collaborative_filtering import train_collaborative_filtering, get_collaborative_recommendations
from utils.hybrid_recommendation import get_hybrid_recommendations

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
        # Fetch movie details
        movie = fetch_movie_details(movie_id)

        # Fetch the first trailer
        trailer = None
        for video in movie.get('videos', {}).get('results', []):
            if video['type'] == "Trailer":
                trailer = video
                break

        # Fetch TMDb reviews
        tmdb_reviews = fetch_reviews(movie_id)

        # Pagination for TMDb reviews
        page = request.args.get('page', 1, type=int)
        per_page = 5
        total_pages = -(-len(tmdb_reviews) // per_page)  # Ceiling division
        paginated_tmdb_reviews = tmdb_reviews[(page - 1) * per_page : page * per_page]

        # Fetch user-added reviews from the database
        user_reviews = Review.query.filter_by(movie_id=movie_id).all()

        # Combine TMDb and user reviews
        combined_reviews = paginated_tmdb_reviews + [
            {'author': review.user.username, 'content': review.content, 'rating': review.rating or "No rating"}
            for review in user_reviews
        ]

        # Perform sentiment analysis on all reviews
        sentiments = analyze_sentiments(combined_reviews)
        # Check if the movie is a favorite for the current user
        is_favorite = False
        if current_user.is_authenticated:
            is_favorite = Favorite.query.filter_by(user_id=current_user.id, movie_id=movie_id).first() is not None

        # Fetch recommendations
        recommendations = get_similar_movies(movie,movie_id)
        
        # Render the movie details page
        return render_template(
            'movie_details.html',
            movie=movie,
            trailer=trailer,
            recommendations=recommendations,
            sentiments=sentiments,
            is_favorite=is_favorite,
            total_pages=total_pages,
            current_page=page
        )


    @app.route('/add_review/<int:movie_id>', methods=['POST'])
    @login_required
    def add_review(movie_id):
        """Add a user review for a movie."""
        review_content = request.form.get('review_content')
        review_rating = request.form.get('review_rating')  # Fetch rating input

        if not review_content:
            flash('Review content cannot be empty!', 'danger')
            return redirect(url_for('movie_details', movie_id=movie_id))

        try:
            review = Review(
                user_id=current_user.id,
                movie_id=movie_id,
                content=review_content,
                rating=int(review_rating) if review_rating else None
            )
            db.session.add(review)
            db.session.commit()
            flash('Review added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Error saving review: {e}")
            flash('An error occurred while adding the review. Please try again.', 'danger')

        return redirect(url_for('movie_details', movie_id=movie_id))
    
    @app.route('/add_favorite/<int:movie_id>', methods=['POST'])
    @login_required
    def add_favorite(movie_id):
        """Mark or unmark a movie as a favorite."""
        favorite = Favorite.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()

        if favorite:
            # If already a favorite, remove it
            db.session.delete(favorite)
            db.session.commit()
            flash('Movie removed from favorites.', 'success')
        else:
            # Add to favorites
            new_favorite = Favorite(user_id=current_user.id, movie_id=movie_id)
            db.session.add(new_favorite)
            db.session.commit()
            flash('Movie added to favorites!', 'success')

        return redirect(url_for('movie_details', movie_id=movie_id))

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



    def fetch_recommendations(favorite_movies):
        """Generate recommendations based on user's favorite movies."""
        if favorite_movies:
            # Content-based recommendations based on favorited movies
            recommendations = []
            for movie in favorite_movies:
                movie_id = movie['id']
                movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={Config.TMDB_API_KEY}&append_to_response=similar"
                response = requests.get(movie_details_url).json()
                recommendations.extend(response.get('similar', {}).get('results', []))
            # Remove duplicates and return unique recommendations
            return {rec['id']: rec for rec in recommendations}.values()
        else:
            # Default to popular movies for new users
            return fetch_popular_movies()
    

       
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """
        Render the user dashboard with personalized recommendations and favorites.
        """
        # Fetch user favorites
        favorite_movies = Favorite.query.filter_by(user_id=current_user.id).all()

        # Fetch details for each favorite movie
        favorites_details = []
        for favorite in favorite_movies:
            try:
                movie_details = fetch_movie_details(favorite.movie_id)  # Use the TMDb API to fetch details
                favorites_details.append({
                    'title': movie_details['title'],
                    'poster_path': movie_details.get('poster_path'),
                    'overview': movie_details.get('overview'),
                    'movie_id': movie_details.get('id'),
                })
            except Exception as e:
                print(f"Error fetching details for movie_id {favorite.movie_id}: {e}")

        # Personalized recommendations based on favorite movies
        recommendations = []
        if favorites_details:
            # Use the first favorite movie for recommendations
            reference_movie = favorites_details[0]
            recommended_movies = get_similar_movies(fetch_movie_details(reference_movie['movie_id']),
                                                    reference_movie['movie_id'])

            recommendations = [
                {
                    'title': rec.get('title'),
                    'poster_path': rec.get('poster_path'),
                    'overview': rec.get('overview'),
                    'movie_id': rec.get('id'),
                }
                for rec in recommended_movies
            ]
        # Fetch popular movies (always shown on dashboard)
        popular_movies = fetch_popular_movies()

        # Render dashboard with favorites and recommendations
        return render_template(
            'dashboard.html',
            favorites=favorites_details,
            recommendations=recommendations,
            movies=popular_movies,
            has_favorites=bool(favorites_details)  # Pass flag if favorites exist
        )


    @app.route('/recommendations')
    @login_required
    def recommendations():
        collaborative_recs = []
        content_recs = []
        hybrid_recs = []

        # Train the collaborative filtering model
        cf_model = train_collaborative_filtering()

        # Collaborative recommendations
        if cf_model is not None and not cf_model.empty:  # Check if cf_model is valid and not empty
            collaborative_recs = get_collaborative_recommendations(cf_model, current_user.id)

        # Content-based recommendations
        favorite = Favorite.query.filter_by(user_id=current_user.id).first()
        if favorite:
            movie_details = fetch_movie_details(favorite.movie_id)
            content_recs = get_similar_movies(movie_details, favorite.movie_id)

            # Hybrid recommendations
            hybrid_recs = get_hybrid_recommendations(current_user.id, cf_model, movie_details, favorite.movie_id)

        return render_template('recommendations.html', collaborative_recs=collaborative_recs,
                            content_recs=content_recs, hybrid_recs=hybrid_recs)