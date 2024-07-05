import streamlit as st
from transformers import pipeline
import matplotlib.pyplot as plt
import numpy as np
import requests
from bs4 import BeautifulSoup
from langdetect import detect, LangDetectException
import pandas as pd

custom_headers = {
    "Accept-language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
}

class Analysis:
    def __init__(self):
        self.sentiment_pipeline = pipeline("sentiment-analysis")
        
    def analyze_reviews(self, reviews):
        if not reviews:
            return [], 0, 0

        results = self.sentiment_pipeline(reviews)

        positive_count = 0
        negative_count = 0

        review_data = []

        for review, result in zip(reviews, results):
            review_data.append({"Review": review, "Sentiment": result['label'], "Confidence": result['score']})
            if result['label'] == 'POSITIVE':
                positive_count += 1
            elif result['label'] == 'NEGATIVE':
                negative_count += 1

        return review_data, positive_count, negative_count

    def plot_pie_chart(self, positive_count, negative_count):
        if positive_count + negative_count == 0:
            st.write("No reviews available for analysis.")
            return

        labels = ['Positive', 'Negative']
        sizes = [positive_count, negative_count]
        colors = ['#4DB6AC', '#FF6F61']

        def autopct_generator(pct, allvalues):
            absolute = int(np.round(pct/100.*np.sum(allvalues)))
            label = labels[sizes.index(absolute)]
            return f"{label}\n{pct:.1f}%"

        fig, ax = plt.subplots(figsize=(8, 6), facecolor='none')
        wedges, texts, autotexts = ax.pie(sizes, colors=colors, autopct=lambda pct: autopct_generator(pct, sizes), startangle=140, textprops=dict(color="white"))
        ax.axis('equal')
        plt.setp(autotexts, size=12, weight="bold", color="black")
        plt.title('Product Sentiment', color='#708090')
        st.pyplot(fig)

def get_soup(url):
    try:
        response = requests.get(url, headers=custom_headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        return soup
    except requests.exceptions.RequestException as e:
        st.write(f"No available data")
        return None

def is_english(text):
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False

def get_reviews(soup):
    review_elements = soup.select("div.review")
    review_texts = []
    for review in review_elements:
        r_content_element = review.select_one("span.review-text")
        r_content = r_content_element.text if r_content_element else None
        if r_content and is_english(r_content):
            truncated_content = r_content.strip()[:705]
            review_texts.append(truncated_content)
    return review_texts

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Processor", "Brand", "Laptops", "Desktops", "Developer Stats"])
    
    analyzer = Analysis()
    
    if page == "Home":
        st.title("Sentiment Analysis Dashboard")
        st.markdown("### Choose a category to view the product review analysis")
        st.markdown("\n\n**Intel®** Product Sentiment Analysis based on online product reviews")
        st.markdown("#### Or paste an Amazon link to analyze reviews")
        amazon_link = st.text_input("Amazon Product Link")

        if amazon_link:
            soup = get_soup(amazon_link)
            if soup:
                reviews = get_reviews(soup)
                _, positive_count, negative_count = analyzer.analyze_reviews(reviews)
                analyzer.plot_pie_chart(positive_count, negative_count)
            else:
                st.error("Failed to retrieve data from the provided link.")
    
    elif page == "Processor":
        st.title("Processor Reviews")
        choice = st.selectbox("Select Processor", ["Select", "Intel i9", "Intel i7", "Intel i5"])
        mapp = {"Intel i9": "i9", "Intel i7": "i7", "Intel i5": "i5"}
        if choice != "Select":
            file_path = f"data/{mapp[choice]}.txt"
            with open(file_path, "r", encoding="utf-8") as file:
                reviews = file.read().split("\n")
            reviews = [review.strip('"') for review in reviews if review.strip()]
            review_data, positive_count, negative_count = analyzer.analyze_reviews(reviews)
            analyzer.plot_pie_chart(positive_count, negative_count)
            st.table(review_data)
    
    elif page == "Brand":
        st.title("Brand Reviews")
        choice = st.selectbox("Select Brand", ["Select", "Acer", "Dell", "Hewlett Packard", "Lenovo"])
        if choice != "Select":
            if choice == "Hewlett Packard":
                choice = "hp"
            file_path = f"data/{choice.lower()}.txt"
            with open(file_path, "r", encoding="utf-8") as file:
                reviews = file.read().split("\n")
            reviews = [review.strip('"') for review in reviews if review.strip()]
            review_data, positive_count, negative_count = analyzer.analyze_reviews(reviews)
            analyzer.plot_pie_chart(positive_count, negative_count)
            st.table(review_data)
    
    elif page == "Laptops":
        st.title("Laptop Reviews")
        choice = st.selectbox("Select Laptop", ["Select", "Acer", "Dell", "Hewlett Packard"])
        if choice != "Select":
            if choice == "Hewlett Packard":
                choice = "hp"
            file_path = f"data/{choice.lower()}.txt"
            with open(file_path, "r", encoding="utf-8") as file:
                reviews = file.read().split("\n")
            reviews = [review.strip('"') for review in reviews if review.strip()]
            review_data, positive_count, negative_count = analyzer.analyze_reviews(reviews)
            analyzer.plot_pie_chart(positive_count, negative_count)
            st.table(review_data)
    
    elif page == "Desktops":
        st.title("Desktop Reviews")
        choice = st.selectbox("Select Desktop", ["Select", "Acer", "Dell", "Hewlett Packard", "Lenovo"])
        if choice != "Select":
            if choice == "Hewlett Packard":
                choice = "hp"
            file_path = f"data/{choice.lower()}.txt"
            with open(file_path, "r", encoding="utf-8") as file:
                reviews = file.read().split("\n")
            reviews = [review.strip('"') for review in reviews if review.strip()]
            review_data, positive_count, negative_count = analyzer.analyze_reviews(reviews)
            analyzer.plot_pie_chart(positive_count, negative_count)
            st.table(review_data)
    
    elif page == "Developer Stats":
        st.title("Developer Statistics")
        st.write("Product sentiment analysis of Intel products\n")
        st.image("accuracy.png", caption="Model accuracy", use_column_width=True)
        st.markdown("""
        - **Accuracy of Analysis**: 90%-95%
        - **Model Type**: Pretrained Transformer Model
        - **Architecture**: DistilBERT (Bidirectional Encoder Representations from Transformers
        - **Model**: distilbert-base-uncased-finetuned-sst-2-english
        - **Layers**: 6 transformer layers
        - **Batch Size**: NA (inference mode)
        - **Pipeline**: sentiment-analysis
        """)
        st.write("\nMade by team 'Airborne'")

if __name__ == "__main__":
    main()
