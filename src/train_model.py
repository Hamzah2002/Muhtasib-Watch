import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from imblearn.over_sampling import SMOTE  # To handle class imbalance
import pickle
from preprocess import clean_text

# Step 1: Load the Dataset
print("Loading the dataset...")
data_path = "../data/phishing_emails.csv"  # Adjust this path based on your project structure
data = pd.read_csv(data_path)

# Ensure the dataset has the required columns: 'email_text' and 'label'
if 'email_text' not in data.columns or 'label' not in data.columns:
    raise ValueError("Dataset should have 'email_text' and 'label' columns.")
print(f"Dataset Loaded: {len(data)} samples")

# Step 2: Preprocess the Email Text
print("Cleaning and preprocessing text data...")
data['cleaned_text'] = data['email_text'].apply(clean_text)

# Step 3: Check and Handle Class Imbalance Using SMOTE
# Display the distribution of phishing vs. non-phishing samples
print(f"Class Distribution Before Balancing:\n{data['label'].value_counts()}\n")

# If imbalance is detected, SMOTE will generate synthetic samples for the minority class
smote = SMOTE(random_state=42)

# Step 4: Vectorize the Cleaned Text using TF-IDF
print("Vectorizing the text data using TF-IDF...")
vectorizer = TfidfVectorizer(
    max_features=5000,  # Limit to the top 5000 terms to reduce dimensionality
    ngram_range=(1, 2),  # Use both unigrams and bigrams for richer features
    stop_words='english'  # Remove common English stop words
)
X = vectorizer.fit_transform(data['cleaned_text'])  # Extract text features using TF-IDF
y = data['label']  # Labels: 1 = Phishing, 0 = Legitimate

# Step 5: Split the Data into Training and Testing Sets
print("Splitting the data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 6: Apply SMOTE to Balance the Training Data
print("Applying SMOTE to balance the training data...")
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
print(f"Class Distribution After SMOTE:\n{np.bincount(y_train_balanced)}\n")

# Step 7: Hyperparameter Tuning with GridSearchCV
print("Tuning model hyperparameters using GridSearchCV...")
param_grid = {
    'C': [0.1, 1, 10],  # Regularization strength parameter
    'solver': ['liblinear', 'lbfgs']  # Different optimization algorithms
}
# Perform 5-fold cross-validation for hyperparameter tuning
grid_search = GridSearchCV(LogisticRegression(), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train_balanced, y_train_balanced)

# Get the best model from GridSearchCV
best_model = grid_search.best_estimator_
print(f"Best Model Parameters: {grid_search.best_params_}")

# Step 8: Evaluate the Model on the Test Set
print("Evaluating the model on the test set...")
y_pred = best_model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Step 9: Save the Trained Model and Vectorizer
print("Saving the trained model and vectorizer...")
model_filename = "../models/phishing_model.pkl"
vectorizer_filename = "../models/vectorizer.pkl"

# Save the best model to a file using pickle
with open(model_filename, "wb") as model_file:
    pickle.dump(best_model, model_file)

# Save the trained TF-IDF vectorizer
with open(vectorizer_filename, "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

print(f"Model saved to {model_filename}")
print(f"Vectorizer saved to {vectorizer_filename}")
print("Training and saving process completed successfully!")
