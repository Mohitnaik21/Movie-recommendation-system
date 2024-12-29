import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def create_user_item_matrix():
    ratings = pd.read_csv('ratings.csv')
    return ratings.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)

def calculate_similarity(user_item_matrix):
    similarity = cosine_similarity(user_item_matrix)
    return pd.DataFrame(similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

def recommend_movies(user_id, user_item_matrix, similarity_matrix, top_n=5):
    similar_users = similarity_matrix[user_id].sort_values(ascending=False).index[1:]
    similar_users_ratings = user_item_matrix.loc[similar_users].mean().sort_values(ascending=False)
    user_rated_movies = user_item_matrix.loc[user_id]
    recommendations = similar_users_ratings[user_rated_movies[user_rated_movies > 0].index].dropna()
    return recommendations.head(top_n)
