import requests
from config import Config

def get_similar_movies(movie_details, current_movie_id):
    """
    Fetch similar movies based on genre, cast, and director.

    Args:
        movie_details (dict): Details of the current movie.
        current_movie_id (int): ID of the current movie.

    Returns:
        list: A list of recommended movies.
    """
    try:
        genres = [genre['id'] for genre in movie_details.get('genres', [])]
        director = next((crew['id'] for crew in movie_details.get('credits', {}).get('crew', [])
                         if crew['job'] == 'Director'), None)
        cast = [cast_member['id'] for cast_member in movie_details.get('credits', {}).get('cast', [])[:5]]

        recommendations = []

        if director:
            recommendations += fetch_movies_by_criteria({'with_people': str(director)})

        if genres:
            recommendations += fetch_movies_by_criteria({'with_genres': ','.join(map(str, genres))})

        if cast:
            recommendations += fetch_movies_by_criteria({'with_people': ','.join(map(str, cast))})

        # Deduplicate and filter out the current movie
        filtered_recommendations = {movie['id']: movie for movie in recommendations if movie['id'] != current_movie_id}
        return list(filtered_recommendations.values())
    except Exception as e:
        print(f"Error in get_similar_movies: {e}")
        return []

def fetch_movies_by_criteria(criteria):
    """
    Fetch movies from TMDb API based on specific criteria.

    Args:
        criteria (dict): Dictionary of criteria for the API call.

    Returns:
        list: A list of movies.
    """
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={Config.TMDB_API_KEY}&language=en-US"
    response = requests.get(url, params={**criteria, 'sort_by': 'popularity.desc', 'page': 1})
    if response.status_code == 200:
        return response.json().get('results', [])
    return []
