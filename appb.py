import pandas as pd
import streamlit as st

# Load dataset
file_path = "books_recommendation_model/startup_books_dataset.xlsx"


@st.cache_data
def load_data():
    return pd.read_excel(file_path)


df = load_data()


# Function to recommend books
def recommend_books(startup_stage, num_books):
    filtered_books = df[df["Startup_Stage"].str.lower() == startup_stage.lower()]

    if filtered_books.empty:
        return ["No books found for this startup stage."]

    recommended_books = filtered_books.sample(n=min(num_books, len(filtered_books)))

    return recommended_books["Book_Title"].tolist()


# Streamlit UI
st.title("📚 Startup Books Recommendation System")
st.write("Get book recommendations based on your startup stage.")

# User input
startup_stage = st.selectbox("Select your startup stage:", df["Startup_Stage"].unique())
num_books = st.slider("Number of books to recommend:", min_value=1, max_value=10, value=3)

# Button to generate recommendations
if st.button("Get Recommendations"):
    recommendations = recommend_books(startup_stage, num_books)

    # Display recommendations
    st.subheader("Recommended Books:")
    for book in recommendations:
        st.write(f"- {book}")
