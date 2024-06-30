from transformers import pipeline
import os
import matplotlib.pyplot as plt

# Load the pre-trained sentiment-analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

with open("scraped.txt", "r", encoding="utf-8") as file:
    reviews = file.read().split("\n")
reviews = [review.strip('"') for review in reviews if review.strip()]

# Classify each review
results = sentiment_pipeline(reviews)

# Display the results
os.system("clear")  # os.system("cls") for windows

positive_count = 0
negative_count = 0

for review, result in zip(reviews, results):
    print(f"Review: {review}\nSentiment: {result['label']}, Confidence: {result['score']:.2f}\n")
    if result['label'] == 'POSITIVE':
        positive_count += 1
    elif result['label'] == 'NEGATIVE':
        negative_count += 1

# Generate a pie chart
labels = ['Positive', 'Negative']
sizes = [positive_count, negative_count]
colors = ['#66b3ff', '#ff9999']

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Distribution of Sentiments in Reviews')
plt.show()
