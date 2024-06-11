import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import re
import string

# Function to preprocess text
def preprocess_text(text):
    # Remove punctuation and numbers
    text = re.sub(f'[{string.punctuation}0-9]', ' ', text)
    # Lowercase text
    text = text.lower()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load and preprocess data
def load_data(good_file, bad_file):
    texts = []
    labels = []
    
    # Load good reviews
    with open(good_file, 'r', encoding='utf-8') as file:
        for line in file:
            texts.append(preprocess_text(line.strip()))
            labels.append(1)  # 1 for good
            
    # Load bad reviews
    with open(bad_file, 'r', encoding='utf-8') as file:
        for line in file:
            texts.append(preprocess_text(line.strip()))
            labels.append(0)  # 0 for bad
            
    return texts, labels

# Load data
texts, labels = load_data('/home/manya/codes/intel/good.txt', '/home/manya/codes/intel/bad.txt')

# Split data into training and validation sets
x_train, x_val, y_train, y_val = train_test_split(texts, labels, test_size=0.2, random_state=42, stratify=labels)

# Create a pipeline with count vectorizer, tfidf transformer, and naive bayes classifier
text_clf = Pipeline([
    ('vect', CountVectorizer(max_features=10000, ngram_range=(1, 2), stop_words='english')),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB()),
])

# Train the model
text_clf.fit(x_train, y_train)

# Evaluate the model
y_pred = text_clf.predict(x_val)
accuracy = np.mean(y_pred == y_val)
print('Validation Accuracy:', accuracy)

# Print detailed classification report
print(classification_report(y_val, y_pred))
print(confusion_matrix(y_val, y_pred))

# Function to predict sentiment of new reviews
def predict_sentiment(review):
    review = preprocess_text(review)
    prediction = text_clf.predict([review])
    return 'Positive' if prediction[0] == 1 else 'Negative'

# Example usage
new_review = "Intel's products are disgusting"
print(predict_sentiment(new_review))

# Additional debugging: Check predictions for some bad reviews
bad_reviews = [
    "Intel's products are disgusting",
    "I hate the performance of this Intel product",
    "This is the worst Intel processor I've ever used",
    "Terrible product, not recommended",
    "Extremely disappointed with the quality of Intel's service",
    "Bad performance and horrible experience",
    "Never buying Intel again",
    "This product does not meet expectations",
    "Very poor build quality",
    "Waste of money on Intel products"
]

for review in bad_reviews:
    print(f'Review: {review} -> Prediction: {predict_sentiment(review)}')
