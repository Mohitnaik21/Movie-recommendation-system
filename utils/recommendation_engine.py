import requests
from config import Config

def get_similar_movies(movie_details, current_movie_id):
    """
    Fetch similar movies based on genre, cast, and director, excluding the current movie.

    Args:
        movie_details (dict): Details of the current movie.
        current_movie_id (int): ID of the current movie.

    Returns:
        list: A list of recommended movies.
    """
    try:
        # Extract genres
        genres = [genre['id'] for genre in movie_details.get('genres', [])]
        print(f"Extracted genres: {genres}")

        # Extract director
        director = next(
            (crew['id'] for crew in movie_details.get('credits', {}).get('crew', [])
             if crew['job'] == 'Director'), None
        )
        print(f"Extracted director ID: {director}")

        # Extract top 5 cast members
        cast = [cast_member['id'] for cast_member in movie_details.get('credits', {}).get('cast', [])[:5]]
        print(f"Extracted cast IDs: {cast}")

        # Initialize an empty list for recommendations
        recommendations = []

        # Query 1: Movies by the same director
        if director:
            director_url = f"https://api.themoviedb.org/3/discover/movie?api_key={Config.TMDB_API_KEY}&language=en-US"
            director_params = {'with_people': str(director), 'sort_by': 'popularity.desc', 'page': 1}
            director_response = requests.get(director_url, params=director_params)
            if director_response.status_code == 200:
                director_movies = director_response.json().get('results', [])
                recommendations.extend(director_movies)
            print(f"Movies by the same director: {[movie['id'] for movie in director_movies]}")

        # Query 2: Movies with overlapping genres
        if genres:
            genre_url = f"https://api.themoviedb.org/3/discover/movie?api_key={Config.TMDB_API_KEY}&language=en-US"
            genre_params = {'with_genres': ','.join(map(str, genres)), 'sort_by': 'popularity.desc', 'page': 1}
            genre_response = requests.get(genre_url, params=genre_params)
            if genre_response.status_code == 200:
                genre_movies = genre_response.json().get('results', [])
                recommendations.extend(genre_movies)
            print(f"Movies with overlapping genres: {[movie['id'] for movie in genre_movies]}")

        # Query 3: Movies with overlapping cast members
        if cast:
            cast_url = f"https://api.themoviedb.org/3/discover/movie?api_key={Config.TMDB_API_KEY}&language=en-US"
            cast_params = {'with_people': ','.join(map(str, cast)), 'sort_by': 'popularity.desc', 'page': 1}
            cast_response = requests.get(cast_url, params=cast_params)
            if cast_response.status_code == 200:
                cast_movies = cast_response.json().get('results', [])
                recommendations.extend(cast_movies)
            print(f"Movies with overlapping cast: {[movie['id'] for movie in cast_movies]}")

        # Deduplicate recommendations and filter out the current movie
        filtered_recommendations = {movie['id']: movie for movie in recommendations if movie['id'] != current_movie_id}
        sorted_recommendations = sorted(filtered_recommendations.values(), key=lambda x: x['popularity'], reverse=True)

        print(f"Final filtered recommendations: {[movie['id'] for movie in sorted_recommendations]}")
        return sorted_recommendations

    except Exception as e:
        print(f"Error in get_similar_movies: {e}")
        return []
