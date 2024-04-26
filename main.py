import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    return sentiment_scores['compound']

def scrape_reviews(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        
        reviews = []
        for review in soup.find_all('div', class_='review-text-content'):
            review_text = review.get_text(strip=True)
            reviews.append(review_text)
        return reviews
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return []

def main():
    url = input("Enter URL of the Amazon page containing reviews: ")
    reviews = scrape_reviews(url)
    
    if not reviews:
        print("No reviews found on this page.")
        return
    
    for review in reviews:
        sentiment_score = analyze_sentiment(review)
        
        if sentiment_score <= 0.2:
            print("Review:", review)
            print("Sentiment: Negative")
            print(f"Review score: {sentiment_score}")
            print("Sorry, this review seems negative.\n")
        else:
            print("Review:", review)
            print("Sentiment: Positive")
            print(f"Review score: {sentiment_score}")
            print("Thanks for this positive review!\n")

if __name__ == "__main__":
    main()
