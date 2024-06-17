import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import os

# Ensure TensorFlow Hub caches the model to avoid repeated downloads
os.environ['TFHUB_CACHE_DIR'] = './tfhub_cache'

# Load the pre-trained model from TensorFlow Hub
model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
print("Loading model...")
model = hub.load(model_url)
print("Model loaded successfully.")


def classify_review(review):
    #preprocess
    embeddings = model([review])
    positive_words = ["good", "great", "excellent", "amazing", "love", "fantastic"]
    negative_words = ["bad", "terrible", "awful", "hate", "worst", "poor"]

    #check for the presence of positive or negative words
    review_lower = review.lower()
    if any(word in review_lower for word in positive_words):
        return "Good"
    elif any(word in review_lower for word in negative_words):
        return "Bad"
    else:
        return "Neutral"



review = input("Enter review: ")
result = classify_review(review)
print(f"The review is: {result}")
