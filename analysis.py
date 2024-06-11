import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Load and preprocess data
def load_data(good_file, bad_file):
    texts = []
    labels = []
    
    # Load good reviews
    with open(good_file, 'r', encoding='utf-8') as file:
        for line in file:
            texts.append(line.strip())
            labels.append(1)  # 1 for good
            
    # Load bad reviews
    with open(bad_file, 'r', encoding='utf-8') as file:
        for line in file:
            texts.append(line.strip())
            labels.append(0)  # 0 for bad
            
    return texts, labels

# Load data
texts, labels = load_data('/home/manya/codes/intel/good.txt', '/home/manya/codes/intel/bad.txt')

# Split data into training and validation sets
x_train, x_val, y_train, y_val = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Create a pipeline with count vectorizer, tfidf transformer, and naive bayes classifier
text_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB()),
])

# Train the model
text_clf.fit(x_train, y_train)

# Evaluate the model
accuracy = text_clf.score(x_val, y_val)
print('Validation Accuracy:', accuracy)

# Function to predict sentiment of new reviews
def predict_sentiment(review):
    prediction = text_clf.predict([review])
    return 'Positive' if prediction[0] == 1 else 'Negative'

# Example usage
new_review = "Intel's products are amazing"
print(predict_sentiment(new_review))
