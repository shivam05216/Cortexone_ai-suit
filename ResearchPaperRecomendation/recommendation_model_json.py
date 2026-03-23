import pandas as pd
import json


# Load JSON data
def load_json_data(file_path):
    # Read the JSON file line by line
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))

    # Convert the list of dictionaries to a Pandas DataFrame
    return pd.DataFrame(data)


# Preprocess the data (e.g., remove NaNs, duplicates)
def preprocess_data(data):
    # Drop rows with missing titles or abstracts
    data = data.dropna(subset=['title', 'abstract'])

    # Keep only relevant columns
    return data[['title', 'abstract']]


# Path to your JSON file
file_path = 'arxiv-metadata-oai-snapshot.json'

# Load and preprocess the data
data = load_json_data(file_path)
data = preprocess_data(data)

# Display the first few rows to verify
print(data.head())

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Define the recommendation model
def recommend_papers(title, data, num_recommendations=5):
    # Initialize TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['abstract'])

    # Compute cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get the index of the paper that matches the title
    indices = pd.Series(data.index, index=data['title']).drop_duplicates()
    idx = indices[title]

    # Get similarity scores for the given paper
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the papers by similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the most similar papers
    sim_scores = sim_scores[1:num_recommendations+1]
    paper_indices = [i[0] for i in sim_scores]

    # Return the recommended papers
    return data['title'].iloc[paper_indices], data['abstract'].iloc[paper_indices]

import streamlit as st

def main():
    st.title("Test Streamlit App")
    st.write("If you see this message, Streamlit is working!")

if __name__ == "__main__":
    main()