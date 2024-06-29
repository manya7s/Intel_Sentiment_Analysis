from transformers import pipeline
import os

# Load the pre-trained sentiment-analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Example user reviews
reviews = [
    "The product was excellent and exceeded my expectations!",
    "The product was terrible and didn't work at all.",
    "The product is okay, but nothing special."
]

# Classify each review
results = sentiment_pipeline(reviews)

# Display the results
os.system("clear") #os.system("cls") for windows
for review, result in zip(reviews, results):
    print(f"Review: {review}\nSentiment: {result['label']}, Confidence: {result['score']:.2f}\n")
