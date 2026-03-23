"""import streamlit as st
import pandas as pd

# ========================== Load and Prepare Course Data ==========================
def load_course_data():
    try:
        # Load the dataset
        courses = pd.read_excel('education_recommendation/Udemy Courses.xlsx', engine='openpyxl')
        st.write("Data Loaded Successfully!")
        return courses
    except Exception as e:
        st.error(f"Error loading course data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def prepare_course_data(courses):
    # Ensure proper column names as per the dataset
    # Convert 'course_rating' to numeric, coerce errors to NaN
    courses['Course Rating'] = pd.to_numeric(courses['Course Rating'], errors='coerce')

    # Fill missing ratings with 0 after conversion
    courses['Course Rating'] = courses['Course Rating'].fillna(0)

    # Drop duplicates and rows with missing values in 'category' and 'course_rating'
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
    st.title("Education Recommendation System")

    # Load the course data to get categories and ratings
    courses = load_course_data()
    if courses.empty:
        st.stop()  # Stop if data is not loaded

    # Prepare the data
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
        if len(recommendations) > 0:
            st.write("Recommended Courses:")
            for _, row in recommendations.iterrows():
                st.write(f"{row['Course Name']} - Rating: {row['Course Rating']:.1f}")
        else:
            st.write("No recommendations found for the given input.")

# Run the app
if __name__ == "__main__":
    main()"""

import streamlit as st
import pandas as pd


# ========================== Load and Prepare Course Data ==========================
def load_course_data():
    try:
        # Load the dataset
        courses = pd.read_excel('education_recommendation/Udemy Courses.xlsx', engine='openpyxl')
        # Display some basic info for debugging
      #  st.write("Sample Data from Dataset:")
      #  st.write(courses.head())
        return courses
    except Exception as e:
        st.error(f"Error loading course data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


def prepare_course_data(courses):
    # Fill missing values in 'Course Rating' with 0 and convert it to numeric type
    courses['Course Rating'] = pd.to_numeric(courses['Course Rating'], errors='coerce').fillna(0)
    # Drop duplicates and rows with missing values in 'Category' and 'Course Rating'
    courses = courses.dropna(subset=['Category', 'Course Rating'])
    courses = courses.drop_duplicates()
    return courses


# Function to recommend courses
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
    st.title("Education Recommendation System")

    # Load the course data to get categories and ratings
    courses = load_course_data()
    if courses.empty:
        st.stop()  # Stop if data is not loaded

    # Prepare the data
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
        if not recommendations.empty:
            st.write("Recommended Courses:")
            for _, row in recommendations.iterrows():
                st.write(f"{row['Course Name']} - Rating: {row['Course Rating']:.1f}")
        else:
            st.write("No recommendations available for the given inputs.")


# Run the app
if __name__ == "__main__":
    main()
