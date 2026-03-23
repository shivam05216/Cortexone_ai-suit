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

# ========================== Education Recommendation Model (Updated) ==========================
def load_course_data():
    try:
        # Load the dataset
        courses = pd.read_excel('education_recommendation/Udemy Courses.xlsx', engine='openpyxl')
        # Display some basic info for debugging
        return courses
    except Exception as e:
        st.error(f"Error loading course data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def prepare_course_data(courses):
    # Ensure 'Course Rating' is numeric
    courses['Course Rating'] = pd.to_numeric(courses['Course Rating'], errors='coerce')
    # Fill missing values in the 'Course Rating' column with 0
    courses['Course Rating'] = courses['Course Rating'].fillna(0)
    # Drop duplicates and rows with missing values in 'Category' and 'Course Rating'
    courses = courses.dropna(subset=['Category', 'Course Rating'])
    courses = courses.drop_duplicates()
    return courses

def recommend_courses(category, min_rating, num_recommendations):
    courses = load_course_data()
    if courses.empty:
        return []

    # Prepare the data
    courses = prepare_course_data(courses)

    # Filter courses by the selected category and rating
    filtered_courses = courses[(courses['Category'] == category) & (courses['Course Rating'] >= min_rating)]

    if filtered_courses.empty:
        st.error("No courses found for the selected category and rating.")
        return []

    # Sort the courses by rating in descending order and get the top recommendations
    recommended_courses = filtered_courses.sort_values(by='Course Rating', ascending=False).head(num_recommendations)

    return recommended_courses[['Course Name', 'Course Rating']]

# ========================== Streamlit Interface ==========================
def main():
    # Adding CSS for background, font color, and icons
    st.markdown("""
    <style>
        .reportview-container {
            background: <img src= 'background.jpg');
            background-size: cover;
        }
        .instruction-title {
            color: #33FFCE;
            font-size: 20px;
            font-weight: bold;
        }
        .instruction-input {
            color: #FF5733;
            font-size: 18px;
            font-weight: bold;
        }
        .icon {
            width: 50px;
            height: 50px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Machine Learning Model Platform")

    # Adding icons for each model

    # Dropdown to select model
    model_option = st.selectbox("Select a model",
                                ["Text Classification", "Collaborative Movie Filtering", "Education Recommendation"])

    # Icons for the selected models
    if model_option == "Text Classification":
        st.markdown("""
        <img src='https://cdn0.iconfinder.com/data/icons/ai-nlp-mastery-icons/128/Icon_Sentiment_analysis_02-512.png' class='icon'>
        """, unsafe_allow_html=True)
    elif model_option == "Collaborative Movie Filtering":
        st.markdown("""
        <img src='https://static.vecteezy.com/system/resources/previews/000/400/187/original/vector-characters-of-people-holding-movie-icons-illustration.jpg' class='icon'>
        """, unsafe_allow_html=True)
    elif model_option == "Education Recommendation":
        st.markdown("""
        <img src='https://thumbs.dreamstime.com/b/career-planning-concept-man-thinks-his-planing-career-man-standing-front-waymark-street-career-planning-102286344.jpg' class='icon'>
        """, unsafe_allow_html=True)

    # Input for Text Classification
    if model_option == "Text Classification":
        st.markdown('<p class="instruction-title">Text Classification</p>', unsafe_allow_html=True)
        st.markdown('<p class="instruction-input">Enter text for analysis:</p>', unsafe_allow_html=True)
        input_text = st.text_input("Enter text for analysis")
        if st.button("Analyze"):
            result = analyze_sentiment(input_text)
            st.write(f"Sentiment: {result}")

    # Input for Movie Recommendation
    elif model_option == "Collaborative Movie Filtering":
        st.markdown('<p class="instruction-title">Collaborative Movie Filtering</p>', unsafe_allow_html=True)
        st.markdown('<p class="instruction-input">Select a User and Number of Recommendations:</p>', unsafe_allow_html=True)
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
        st.markdown('<p class="instruction-title">Education Recommendation</p>', unsafe_allow_html=True)
        st.markdown('<p class="instruction-input">Select a Category, Minimum Rating, and Number of Recommendations:</p>', unsafe_allow_html=True)
        courses = load_course_data()
        if courses.empty:
            st.stop()  # Stop if data is not loaded

        courses = prepare_course_data(courses)

        # Dropdown for category selection
        category = st.selectbox("Select a category", sorted(courses['Category'].unique()))

        # Slider for minimum course rating
        min_rating = st.slider("Select minimum course rating", min_value=0.0, max_value=5.0, step=0.1, value=0.0)

        # Slider for number of recommendations
        num_recommendations = st.slider("Number of recommendations", min_value=1, max_value=10)

        # Button to get recommendations
        if st.button("Recommend Courses"):
            recommendations = recommend_courses(category, min_rating, num_recommendations)
            if recommendations is not None and not recommendations.empty:
                st.write("Recommended Courses:")
                for _, row in recommendations.iterrows():
                    st.write(f"{row['Course Name']} - Rating: {row['Course Rating']:.1f}")

# Run the app
if __name__ == "__main__":
    main()

