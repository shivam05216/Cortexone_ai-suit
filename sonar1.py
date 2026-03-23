# streamlit_app.py
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


# Load the dataset
@st.cache_data
def load_data():
    file_path = 'Copy of sonar data.csv'
    data = pd.read_csv(file_path)
    return data


# Function to train the model and make predictions
def train_model(model, X_train, y_train, X_test):
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    return predictions


# Load the data
data = load_data()

# Prepare the dataset
X = data.iloc[:, :-1]  # Features (all columns except the last)
y = data.iloc[:, -1]  # Target (the last column, which is 'R' or another label)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the models to choose from
models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Support Vector Machine": SVC(),
    "Gradient Boosting": GradientBoostingClassifier()
}

# Streamlit app interface
st.title("Sonar and Rock Prediction Model")

# Dropdown for model selection
model_choice = st.selectbox("Select a model", list(models.keys()))

# When the user clicks the button, train and test the model
if st.button("Run Model"):
    model = models[model_choice]
    predictions = train_model(model, X_train, y_train, X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, predictions)

    # Display results
    st.write(f"Model: {model_choice}")
    st.write(f"Accuracy: {accuracy * 100:.2f}%")

    # Show a comparison of actual vs predicted values
    results = pd.DataFrame({"Predicted": predictions, "Actual": y_test})
    st.write(results)

# Optionally allow users to upload their own CSV file for prediction
st.write("You can upload your own dataset for prediction:")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    user_data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:")
    st.write(user_data)
    # Make predictions on the new dataset
    user_predictions = model.predict(user_data)
    st.write("Predictions on uploaded data:")
    st.write(user_predictions)
