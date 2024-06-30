from transformers import pipeline
import os
import matplotlib.pyplot as plt

class Analysis:
    def __init__(self):
        self.sentiment_pipeline = pipeline("sentiment-analysis")
        
    def analyze_reviews(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            reviews = file.read().split("\n")
        reviews = [review.strip('"') for review in reviews if review.strip()]

        results = self.sentiment_pipeline(reviews)

        os.system("clear")  # os.system("cls") for windows

        positive_count = 0
        negative_count = 0

        for review, result in zip(reviews, results):
            print(f"Review: {review}\nSentiment: {result['label']}, Confidence: {result['score']:.2f}\n")
            if result['label'] == 'POSITIVE':
                positive_count += 1
            elif result['label'] == 'NEGATIVE':
                negative_count += 1

        labels = ['Positive', 'Negative']
        sizes = [positive_count, negative_count]
        colors = ['#A8D5BA', '#F7A1A1']

        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Product Sentiment')
        plt.show()

# Example usage:
if __name__ == "__main__":
    analyzer = Analysis()
    source = "i5.txt"
    analyzer.analyze_reviews(f"data/{source}")
