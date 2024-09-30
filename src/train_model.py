import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import pickle
from preprocess import clean_text

# Step 1: Load the Dataset
print("Loading the dataset...")
data_path = "../data/phishing_emails.csv"  # Adjust this path based on your project structure
data = pd.read_csv(data_path)

# Ensure the dataset has the required columns
if 'email_text' not in data.columns or 'label' not in data.columns:
    raise ValueError("Dataset should have 'email_text' and 'label' columns.")

print(f"Dataset Loaded: {len(data)} samples")

# Step 2: Preprocess the Email Text
print("Cleaning and preprocessing text data...")
data['cleaned_text'] = data['email_text'].apply(clean_text)

# Step 3: Vectorize the Cleaned Text using TF-IDF
print("Vectorizing the text data using TF-IDF...")
vectorizer = TfidfVectorizer(max_features=3000)  # Limit features to the top 3000 terms
X = vectorizer.fit_transform(data['cleaned_text'])  # Text features
y = data['label']  # Labels

# Step 4: Split the Data into Training and Testing Sets
print("Splitting the data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 5: Train a Machine Learning Model
print("Training the model using Logistic Regression...")
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 6: Evaluate the Model
print("Evaluating the model...")
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Step 7: Save the Trained Model and Vectorizer
print("Saving the trained model and vectorizer...")
model_filename = "../models/phishing_model.pkl"
vectorizer_filename = "../models/vectorizer.pkl"

# Save the model
with open(model_filename, "wb") as model_file:
    pickle.dump(model, model_file)

# Save the vectorizer
with open(vectorizer_filename, "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

print(f"Model saved to {model_filename}")
print(f"Vectorizer saved to {vectorizer_filename}")
print("Training and saving process completed successfully!")
