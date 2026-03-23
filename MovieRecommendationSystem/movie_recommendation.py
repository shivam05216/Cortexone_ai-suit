import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Load the datasets
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Create a user-item matrix (rows: users, columns: movies, values: ratings)
user_item_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating')
user_item_matrix.fillna(0, inplace=True)

# Compute the user-user cosine similarity matrix
user_similarity = cosine_similarity(user_item_matrix)

# Convert to a DataFrame for readability
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

# Function to recommend movies
def recommend_movies(user_id, num_recommendations=5):
    user_sim_scores = user_similarity_df[user_id]
    similar_users = user_sim_scores.sort_values(ascending=False).index
    similar_users_ratings = user_item_matrix.loc[similar_users]
    weighted_ratings = similar_users_ratings.T.dot(user_sim_scores.loc[similar_users])
    user_ratings = user_item_matrix.loc[user_id]
    recommended_movies = weighted_ratings[user_ratings == 0].sort_values(ascending=False).head(num_recommendations)
    recommended_movie_titles = movies[movies['movieId'].isin(recommended_movies.index)]['title']
    return recommended_movie_titles

# Streamlit Interface
def main():
    st.title("Movie Recommendation System")
    selected_user = st.selectbox("Select a User", user_item_matrix.index)
    num_recommendations = st.slider("Number of recommendations", min_value=1, max_value=10)
    if st.button("Recommend"):
        recommendations = recommend_movies(selected_user, num_recommendations)
        st.write("Recommended Movies:")
        for movie in recommendations:
            st.write(movie)

if __name__ == "__main__":
    main()