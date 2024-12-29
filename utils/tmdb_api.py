import requests
from config import Config
import pandas as pd

def fetch_popular_movies():
    """Fetch popular movies from TMDb API."""
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={Config.TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url).json()
    return response['results']

def fetch_movie_details(movie_id):
    """Fetch detailed information about a movie."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={Config.TMDB_API_KEY}&append_to_response=credits"
    response = requests.get(url).json()
    return response

def fetch_reviews(movie_id):
    """Fetch reviews for a movie."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={Config.TMDB_API_KEY}"
    response = requests.get(url).json()
    return response.get('results', [])

def save_movies_to_file():
    """Fetch movies and save to a CSV file."""
    movies = fetch_popular_movies()
    movies_data = [
        {
            'movie_id': movie['id'],
            'title': movie['title'],
            'genres': '|'.join([genre['name'] for genre in movie.get('genres', [])]),
            'cast': '',  # Add cast later from detailed data
            'director': ''  # Add director later from detailed data
        }
        for movie in movies
    ]
    df = pd.DataFrame(movies_data)
    df.to_csv('movies.csv', index=False)
