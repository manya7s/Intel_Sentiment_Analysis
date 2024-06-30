import requests
from bs4 import BeautifulSoup
import pandas as pd
from langdetect import detect, LangDetectException

custom_headers = {
    "Accept-language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
}

def get_soup(url):
    response = requests.get(url, headers=custom_headers)

    if response.status_code != 200:
        print("Error in getting webpage")
        exit(-1)

    soup = BeautifulSoup(response.text, "lxml")
    return soup

def is_english(text):
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False

def get_reviews(soup):
    review_elements = soup.select("div.review")

    scraped_reviews = []
    review_texts = []

    for review in review_elements:
        r_author_element = review.select_one("span.a-profile-name")
        r_author = r_author_element.text if r_author_element else None

        r_rating_element = review.select_one("i.review-rating")
        r_rating = r_rating_element.text.replace("out of 5 stars", "") if r_rating_element else None

        r_title_element = review.select_one("a.review-title")
        r_title_span_element = r_title_element.select_one("span:not([class])") if r_title_element else None
        r_title = r_title_span_element.text if r_title_span_element else None

        r_content_element = review.select_one("span.review-text")
        r_content = r_content_element.text if r_content_element else None

        r_date_element = review.select_one("span.review-date")
        r_date = r_date_element.text if r_date_element else None

        r_verified_element = review.select_one("span.a-size-mini")
        r_verified = r_verified_element.text if r_verified_element else None

        if r_content and is_english(r_content):  #review in english
            truncated_content = r_content.strip()[:705]  #705 characters
            review_texts.append(truncated_content)

            r = {
                "author": r_author,
                "rating": r_rating,
                "title": r_title,
                "content": truncated_content, 
                "location_and_date": r_date,
                "verified": r_verified
            }

            scraped_reviews.append(r)

    #write to scraped.txt
    with open("scraped.txt", "w", encoding="utf-8") as file:
        for text in review_texts:
            file.write(text.replace("\nRead more", "") + "\n")

    return scraped_reviews

def main():
    search_url = "https://amzn.in/d/dnUPZWg"
    soup = get_soup(search_url)
    data = get_reviews(soup)
    df = pd.DataFrame(data=data)

    df.to_csv("amz.csv", index=False)

if __name__ == '__main__':
    main()
