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
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    reviews = []
    for review in soup.find_all('div', class_='review'):
        reviews.append(review.get_text().strip())
    return reviews

def main():
    url = input("Enter URL of the page containing reviews: ")
    reviews = scrape_reviews(url)
    
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
