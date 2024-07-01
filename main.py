import streamlit as st
from transformers import pipeline
import matplotlib.pyplot as plt
import numpy as np

class Analysis:
    def __init__(self):
        self.sentiment_pipeline = pipeline("sentiment-analysis")
        
    def analyze_reviews(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            reviews = file.read().split("\n")
        reviews = [review.strip('"') for review in reviews if review.strip()]

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


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Processor", "Brand", "Laptops", "Desktops", "Developer Stats"])
    
    analyzer = Analysis()
    
    if page == "Home":
        st.title("Sentiment Analysis Dashboard")
        st.markdown("### Choose a category to view the product review analysis")
        st.markdown("\n\n**Intel®** Product Sentiment Analysis based on online product reviews")
    
    elif page == "Processor":
        st.title("Processor Reviews")
        choice = st.selectbox("Select Processor", ["Select", "Intel i9", "Intel i7", "Intel i5"])
        mapp = {"Intel i9": "i9", "Intel i7": "i7", "Intel i5": "i5"}
        if choice != "Select":
            file_path = f"data/{mapp[choice]}.txt"
            review_data, positive_count, negative_count = analyzer.analyze_reviews(file_path)
            analyzer.plot_pie_chart(positive_count, negative_count)
            st.table(review_data)
    
    elif page == "Brand":
        st.title("Brand Reviews")
        choice = st.selectbox("Select Brand", ["Select", "Acer", "Dell", "Hewlett Packard", "Lenovo"])
        if choice != "Select":
            if choice == "Hewlett Packard":
                choice = "hp"
            file_path = f"data/{choice.lower()}.txt"
            review_data, positive_count, negative_count = analyzer.analyze_reviews(file_path)
            analyzer.plot_pie_chart(positive_count, negative_count)
            st.table(review_data)
    
    elif page == "Laptops":
        st.title("Laptop Reviews")
        choice = st.selectbox("Select Laptop", ["Select", "Acer", "Dell", "Hewlett Packard"])
        if choice != "Select":
            if choice == "Hewlett Packard":
                choice = "hp"
            file_path = f"data/{choice.lower()}.txt"
            review_data, positive_count, negative_count = analyzer.analyze_reviews(file_path)
            analyzer.plot_pie_chart(positive_count, negative_count)
            st.table(review_data)
    
    elif page == "Desktops":
        st.title("Desktop Reviews")
        choice = st.selectbox("Select Desktop", ["Select", "Acer", "Dell", "Hewlett Packard", "Lenovo"])
        if choice != "Select":
            if choice == "Hewlett Packard":
                choice = "hp"
            file_path = f"data/{choice.lower()}.txt"
            review_data, positive_count, negative_count = analyzer.analyze_reviews(file_path)
            analyzer.plot_pie_chart(positive_count, negative_count)
            st.table(review_data)
    
    elif page == "Developer Stats":
        st.title("Developer Statistics")
        st.write("Product sentiment analysis of Intel products\n")
        st.image("accuracy.png", caption="Model accuracy", use_column_width=True)
        st.markdown("""
        - **Accuracy of Analysis**: 89%-92%
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