import streamlit as st
from textblob import TextBlob
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# ========================== Text Classification Model ==========================
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    if sentiment > 0:
        return "Positive 😊"
    elif sentiment == 0:
        return "Neutral 😐"
    else:
        return "Negative 😔"


# ========================== Collaborative Movie Recommendation Model ==========================
def load_movie_data():
    movies = pd.read_csv('MovieRecommendationSystem/movies.csv')
    ratings = pd.read_csv('MovieRecommendationSystem/ratings.csv')

    user_item_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating')
    user_item_matrix.fillna(0, inplace=True)

    user_similarity = cosine_similarity(user_item_matrix)
    user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

    return movies, ratings, user_item_matrix, user_similarity_df


def recommend_movies(user_id, num_recommendations=5):
    movies, _, user_item_matrix, user_similarity_df = load_movie_data()
    user_sim_scores = user_similarity_df[user_id]
    similar_users = user_sim_scores.sort_values(ascending=False).index
    similar_users_ratings = user_item_matrix.loc[similar_users]
    weighted_ratings = similar_users_ratings.T.dot(user_sim_scores.loc[similar_users])
    user_ratings = user_item_matrix.loc[user_id]
    recommended_movies = weighted_ratings[user_ratings == 0].sort_values(ascending=False).head(num_recommendations)
    recommended_movie_titles = movies[movies['movieId'].isin(recommended_movies.index)]['title']
    return recommended_movie_titles


# ========================== Education Recommendation Model ==========================
def load_course_data():
    # Use on_bad_lines='skip' to skip problematic lines
    courses = pd.read_excel('EducationRecommendationSystem/udemy_courses.xlsx' )
    courses.dropna(inplace=True)
    courses.drop_duplicates(inplace=True)
    return courses


def recommend_courses(course_name, num_recommendations=5):
    courses = load_course_data()
    course_features = courses[['course_level', 'course_duration', 'course_rating', 'no_of_lectures']]
    course_matrix = pd.get_dummies(courses[['Category']]).join(course_features)
    similarity_matrix = cosine_similarity(course_matrix)
    similarity_df = pd.DataFrame(similarity_matrix, index=courses['course_name'], columns=courses['course_name'])
    similar_courses = similarity_df[course_name].sort_values(ascending=False).head(num_recommendations + 1).index
    return courses[courses['course_name'].isin(similar_courses)]['course_name']


# ========================== Streamlit Interface ==========================
def main():
    st.title("Machine Learning Model Platform")

    # Dropdown to select model
    model_option = st.selectbox("Select a model",
                                ["Text Classification", "Collaborative Movie Filtering", "Education Recommendation"])

    # Input for Text Classification
    if model_option == "Text Classification":
        input_text = st.text_input("Enter text for analysis")
        if st.button("Analyze"):
            result = analyze_sentiment(input_text)
            st.write(f"Sentiment: {result}")

    # Input for Movie Recommendation
    elif model_option == "Collaborative Movie Filtering":
        movies, ratings, user_item_matrix, _ = load_movie_data()
        selected_user = st.selectbox("Select a User", user_item_matrix.index)
        num_recommendations = st.slider("Number of recommendations", min_value=1, max_value=10)
        if st.button("Recommend Movies"):
            recommendations = recommend_movies(selected_user, num_recommendations)
            st.write("Recommended Movies:")
            for movie in recommendations:
                st.write(movie)

    # Input for Education Recommendation
    elif model_option == "Education Recommendation":
        courses = load_course_data()
        selected_course = st.selectbox("Select a Course", courses['course_name'].unique())
        num_recommendations = st.slider("Number of recommendations", min_value=1, max_value=10)
        if st.button("Recommend Courses"):
            recommendations = recommend_courses(selected_course, num_recommendations)
            st.write("Recommended Courses:")
            for course in recommendations:
                st.write(course)


# Run the app
if __name__ == "__main__":
    main()

