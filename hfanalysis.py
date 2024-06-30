from transformers import pipeline
import os

# Load the pre-trained sentiment-analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

with open ("scraped.txt", "r") as file:
    reviews = file.read().split("\n")
reviews.pop()

# Classify each review
results = sentiment_pipeline(reviews)

# Display the results
os.system("clear") #os.system("cls") for windows
for review, result in zip(reviews, results):
    print(f"Review: {review}\nSentiment: {result['label']}, Confidence: {result['score']:.2f}\n")
