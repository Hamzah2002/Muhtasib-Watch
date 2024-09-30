import re
import nltk

# Download stopwords if not already present
nltk.download('stopwords')
from nltk.corpus import stopwords

# Set of English stopwords
STOPWORDS = set(stopwords.words('english'))


def clean_text(text):
    """
    Clean and preprocess email text by removing unwanted characters.

    Args:
        text (str): Raw email text to be cleaned.

    Returns:
        str: Cleaned and normalized email text.
    """
    # Convert text to lowercase
    text = text.lower()

    # Replace URLs with a placeholder
    text = re.sub(r'http\S+', '<URL>', text)  # Replace http:// or https:// links with <URL>

    # Replace email addresses with a placeholder
    text = re.sub(r'\S+@\S+', '<EMAIL>', text)  # Replace any word@domain.com with <EMAIL>

    # Remove special characters, punctuation, and digits
    text = re.sub(r'[^a-z\s<URL><EMAIL>]', '', text)  # Keep only letters, spaces, and placeholders

    # Optionally, remove stopwords (optional for phishing detection)
    # Uncomment the next line if you want to remove common stopwords like "the", "is", etc.
    # text = ' '.join([word for word in text.split() if word not in STOPWORDS])

    return text


def tokenize_text(text):
    """
    Tokenize the email text into individual words.

    Args:
        text (str): Cleaned email text.

    Returns:
        list: List of tokens (words) in the email.
    """
    # Split the text into individual words
    return text.split()


def remove_stopwords(tokens):
    """
    Remove stopwords from a list of tokens.

    Args:
        tokens (list): List of words/tokens from the email text.

    Returns:
        list: List of tokens with stopwords removed.
    """
    return [token for token in tokens if token not in STOPWORDS]


def preprocess_email(text):
    """
    Full preprocessing pipeline: clean, tokenize, and remove stopwords.

    Args:
        text (str): Raw email text.

    Returns:
        list: Preprocessed tokens from the email text.
    """
    # Step 1: Clean the text
    cleaned_text = clean_text(text)

    # Step 2: Tokenize the text
    tokens = tokenize_text(cleaned_text)

    # Step 3: Remove stopwords (optional)
    processed_tokens = remove_stopwords(tokens)

    return processed_tokens
