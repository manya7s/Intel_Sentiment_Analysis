import tensorflow as tf
import os

save_dir = './saved_model'
print("Loading model from saved directory...")
model = tf.saved_model.load(save_dir)
print("Model loaded successfully.")
#output key
signatures = model.signatures["serving_default"]

def classify_review(review):
    infer = model.signatures["serving_default"]
    embeddings = infer(tf.constant([review]))
    
    embedding_values = embeddings['output_0']

    positive_words = ["good", "great", "excellent", "amazing", "love", "fantastic"]
    negative_words = ["bad", "terrible", "awful", "hate", "not", "worst", "poor"]

    sentiment_score = tf.reduce_mean(embedding_values, axis=1).numpy()[0]

    if "not" in review.lower() and sentiment_score < 0.5:
        sentiment_score = 1 - sentiment_score

    if sentiment_score >= 0.6:
        return "Good"
    elif sentiment_score <= 0.4:
        return "Bad"
    else:
        return "Neutral"

review = input("Enter review: ")
result = classify_review(review)
print(f"The review is: {result}")
