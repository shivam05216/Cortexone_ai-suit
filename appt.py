import pandas as pd
import streamlit as st

# Load datasets
books_file = "books_recommendation_model/startup_books_dataset.xlsx"
journals_file = "Entrepreneurship_Journals.xlsx"  # Relative path
theories_file = "Startup_Theories_Case_Studies.xlsx"


@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)


books_df = load_data(books_file)
journals_df = load_data(journals_file)
theories_df = load_data(theories_file)

# Recommendation functions
def recommend_books(startup_stage, num_books):
    filtered_books = books_df[books_df["Startup_Stage"].str.lower() == startup_stage.lower()]
    if filtered_books.empty:
        return ["No books found for this startup stage."]
    return filtered_books.sample(n=min(num_books, len(filtered_books)))["Book_Title"].tolist()


def recommend_journals(startup_stage, num_journals):
    filtered_journals = journals_df[journals_df["Startup_Stage"].str.lower() == startup_stage.lower()]
    if filtered_journals.empty:
        return ["No journals found for this startup stage."]
    return filtered_journals.sample(n=min(num_journals, len(filtered_journals)))["Journal_Title"].tolist()


def recommend_theories(startup_stage, num_cases):
    filtered_theories = theories_df[theories_df["Startup_Stage"].str.lower() == startup_stage.lower()]
    if filtered_theories.empty:
        return ["No case studies or theories found for this startup stage."]
    return filtered_theories.sample(n=min(num_cases, len(filtered_theories)))["Theory_Case_Title"].tolist()


# Streamlit UI
st.title("VentureReads ")
st.write("Tailored reading recommendations for entrepreneurs, Choose a category and get relevant recommendations!")

# Model Selection
model_option = st.selectbox("Select Recommendation Type:", [
    "Startup Books Recommendation",
    "Entrepreneurship Journals Recommendation",
    "Startup Theories & Case Studies Recommendation"
])

# User Inputs
startup_stage = st.selectbox("Select your startup stage:", books_df["Startup_Stage"].unique())
num_recommendations = st.slider("Number of recommendations:", min_value=1, max_value=10, value=3)

if st.button("Get Recommendations"):
    st.subheader("Recommended:")
    if model_option == "Startup Books Recommendation":
        recommendations = recommend_books(startup_stage, num_recommendations)
    elif model_option == "Entrepreneurship Journals Recommendation":
        recommendations = recommend_journals(startup_stage, num_recommendations)
    else:
        recommendations = recommend_theories(startup_stage, num_recommendations)

    for item in recommendations:
        st.write(f"- {item}")