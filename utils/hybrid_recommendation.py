from utils.content_based_filtering import get_similar_movies
from utils.collaborative_filtering import get_collaborative_recommendations

def get_hybrid_recommendations(user_id, similarity_matrix, movie_details, current_movie_id, top_n=10):
    """
    Combine collaborative and content-based recommendations.

    Args:
        user_id (int): User ID.
        similarity_matrix (pd.DataFrame): Collaborative similarity matrix.
        movie_details (dict): Details of the current movie.
        current_movie_id (int): Current movie ID.
        top_n (int): Number of recommendations to return.

    Returns:
        list: Hybrid recommendations.
    """
    collaborative_recs = get_collaborative_recommendations(similarity_matrix, user_id, top_n=top_n)
    content_recs = get_similar_movies(movie_details, current_movie_id)

    movie_ids = set()
    hybrid_recs = []

    for rec in collaborative_recs + content_recs:
        if rec['id'] not in movie_ids:
            hybrid_recs.append(rec)
            movie_ids.add(rec['id'])
        if len(hybrid_recs) >= top_n:
            break

    return hybrid_recs
