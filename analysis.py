import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import os

os.environ['TFHUB_CACHE_DIR'] = './tfhub_cache'

model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
print("Loading model...")
model = hub.load(model_url)
print("Model loaded successfully.")


def classify_review(review):

    embeddings = model([review])

    positive_words = ["good", "great", "excellent", "amazing", "love", "fantastic"]
    negative_words = ["bad", "terrible", "awful", "hate", "not", "worst", "poor"]

    sentiment_score = tf.reduce_mean(embeddings, axis=1).numpy()[0]

    if "not" in review.lower() and sentiment_score < 0.5:
        sentiment_score = 1 - sentiment_score

    if sentiment_score >= 0.6:
        return "Good"
    elif sentiment_score <= 0.4:
        return "Bad"
    else:
        return "Neutral"

#taking review
review = input("Enter review: ")
result = classify_review(review)
print(f"The review is: {result}")
