import pandas as pd

# Load dataset
file_path = "books_recommendation_model/startup_books_dataset.xlsx"
df = pd.read_excel(file_path)


# Function to recommend books
def recommend_books(startup_stage, num_books):
    # Filter dataset based on startup stage
    filtered_books = df[df["Startup_Stage"].str.lower() == startup_stage.lower()]

    # Check if books are available for that stage
    if filtered_books.empty:
        return ["No books found for this startup stage."]

    # Select the required number of books
    recommended_books = filtered_books.sample(n=min(num_books, len(filtered_books)))

    return recommended_books["Book_Title"].tolist()


# Test the function
if __name__ == "__main__":
    stage = input("Enter your startup stage (Idea, Implemented, Revenue, Scaling): ")
    num = int(input("Enter the number of books to recommend: "))

    recommendations = recommend_books(stage, num)

    print("\nRecommended Books:")
    for book in recommendations:
        print("-", book)
