import pickle
from .preprocess import clean_text  # Import the cleaning function from preprocess.py

class PhishingAnalyzer:
    """
    Core class for the phishing detection system.
    Responsible for loading the model, vectorizer, and running predictions.
    """

    def __init__(self, model_path, vectorizer_path):
        """
        Initialize the analyzer with paths to the model and vectorizer.
        """
        # Load the trained model
        with open(model_path, 'rb') as model_file:
            self.model = pickle.load(model_file)

        # Load the trained vectorizer
        with open(vectorizer_path, 'rb') as vectorizer_file:
            self.vectorizer = pickle.load(vectorizer_file)

    def predict(self, email_text):
        """
        Predict if the given email text is phishing or not.
        :param email_text: Raw text of the email
        :return: 'Phishing' or 'Not Phishing'
        """
        # Clean the input email text
        cleaned_text = clean_text(email_text)

        # Transform the cleaned text using the loaded vectorizer
        text_vector = self.vectorizer.transform([cleaned_text])

        # Make a prediction using the loaded model
        prediction = self.model.predict(text_vector)

        # Return human-readable result
        return "Phishing" if prediction[0] == 1 else "Not Phishing"

    def analyze_keywords(self, email_text):
        """
        Analyze the email for suspicious keywords and phrases.
        :param email_text: Raw text of the email
        :return: List of suspicious keywords found in the email
        """
        # Define common phishing keywords to look for
        phishing_keywords = [
            "urgent", "verify", "password", "account suspended", "click here",
            "login", "security alert", "update account", "confirm identity",
            "unusual activity", "limited time", "risk", "threat", "locked",
            "restricted", "identity theft", "transfer", "credentials"
        ]

        # Find keywords in the email text (case insensitive)
        matches = [word for word in phishing_keywords if word.lower() in email_text.lower()]

        # Return the matches or indicate that no suspicious keywords were found
        return f"Suspicious Keywords Found: {', '.join(matches)}" if matches else "No suspicious keywords found."

    def get_prediction_with_details(self, email_text):
        """
        Combined method to get a detailed prediction report.
        :param email_text: Raw text of the email
        :return: Dictionary with prediction, keywords, and cleaned text
        """
        # Get the main prediction
        prediction = self.predict(email_text)

        # Analyze keywords in the email
        keyword_analysis = self.analyze_keywords(email_text)

        # Cleaned version of the email text
        cleaned_text = clean_text(email_text)

        # Return a structured report
        return {
            "prediction": prediction,
            "suspicious_keywords": keyword_analysis,
            "cleaned_text": cleaned_text
        }

# Example usage for testing
if __name__ == "__main__":
    # Assuming that the models are saved in 'models/' directory
    analyzer = PhishingAnalyzer("models/phishing_model.pkl", "models/vectorizer.pkl")

    # Example email to test
    test_email = """
    Dear user,

    We have detected unusual activity on your account. Please verify your identity immediately by clicking the link below.
    If you do not take action, your account will be suspended.

    Click here to verify: http://example.com/verify

    Thank you,
    Security Team
    """

    # Run predictions and keyword analysis
    print(f"Prediction: {analyzer.predict(test_email)}")
    print(f"Keyword Analysis: {analyzer.analyze_keywords(test_email)}")
    print(f"Detailed Report: {analyzer.get_prediction_with_details(test_email)}")
