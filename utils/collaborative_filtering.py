import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from models import Review
import requests
from config import Config

def train_collaborative_filtering():
    reviews = Review.query.all()
    if not reviews:
        print("No reviews found in the database.")
        return pd.DataFrame()

    data = [(review.user_id, review.movie_id, review.rating or 0) for review in reviews]
    print(f"Review data: {data}")
    df = pd.DataFrame(data, columns=['user_id', 'movie_id', 'rating'])

    user_item_matrix = df.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)
    print(f"User-Item Matrix Shape: {user_item_matrix.shape}")
    print(user_item_matrix.head())

    if user_item_matrix.shape[1] < 2 or user_item_matrix.shape[0] < 2:
        print("Insufficient data for collaborative filtering.")
        return pd.DataFrame()

    similarity_matrix = pd.DataFrame(cosine_similarity(user_item_matrix),
                                     index=user_item_matrix.index,
                                     columns=user_item_matrix.index)
    print(f"Similarity Matrix Shape: {similarity_matrix.shape}")
    print(similarity_matrix.head())
    return similarity_matrix


def fetch_movie_details(movie_id):
    """Fetch movie details from TMDb API."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={Config.TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"Error fetching movie details for ID {movie_id}: {response.status_code}")
    return None



def get_collaborative_recommendations(similarity_matrix, user_id, top_n=10):
    if user_id not in similarity_matrix.index:
        print(f"User ID {user_id} not found in the similarity matrix.")
        return []

    user_similarities = similarity_matrix[user_id].sort_values(ascending=False)[1:]
    similar_users = user_similarities.index

    recommendations = []
    for similar_user in similar_users:
        print(f"Checking movies for similar user: {similar_user}")
        similar_user_movies = Review.query.filter_by(user_id=similar_user).all()
        for review in similar_user_movies:
            if review.movie_id not in [r['id'] for r in recommendations]:
                # Fetch movie details dynamically
                movie_details = fetch_movie_details(review.movie_id)
                if movie_details:
                    recommendations.append({
                        'id': movie_details['id'],
                        'title': movie_details['title'],
                        'poster_path': movie_details.get('poster_path'),
                        'overview': movie_details.get('overview'),
                    })
                if len(recommendations) >= top_n:
                    break
        if len(recommendations) >= top_n:
            break

    if not recommendations:
        print("No recommendations found. Returning fallback recommendations.")
        return []

    print(f"Collaborative Recommendations: {recommendations}")
    return recommendations

