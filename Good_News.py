import requests
import nltk
import time
from nltk.sentiment import SentimentIntensityAnalyzer

# Function to calculate the positivity rating of a headline
def positivity_rating(headline):
    sentiment_scores = sia.polarity_scores(headline)
    positive_score = sentiment_scores['pos']
    negative_score = sentiment_scores['neg']
    return (positive_score - negative_score) / (positive_score + negative_score + 1e-9)


# Initialize the SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# NewsAPI
api_key = "c8c3bddff4504b39971031e287042cbc"
page_size = 100  # Set the number of articles per request

# List of popular sources (feel free to add more)
sources = [
    "abc-news",
    "al-jazeera-english",
    "associated-press",
    "bbc-news",
    "cnn",
    "espn",
    "fox-news",
    "nbc-news",
    "the-guardian-uk",
    "the-new-york-times"
]

# Combine the source names to create a comma-separated string
source_string = ",".join(sources)

# Fetch the latest news articles from popular sources
response = requests.get(f"https://newsapi.org/v2/top-headlines?apiKey={api_key}&language=en&sources={source_string}&pageSize={page_size}")

# Check if the response was successful
if response.status_code == 200:
    data = response.json()

    # Check if the 'articles' key exists in the response
    if 'articles' in data:
        articles = data['articles']

        # Extract the headlines and filter out empty strings
        headlines = [(article['title'], article['url']) for article in articles if article['title']]

        # Print the number of headlines
        print(f"Number of headlines: {len(headlines)}")

        # Filter headlines based on the positivity rating
        filtered_headlines = [(headline[0], headline[1]) for headline in headlines if positivity_rating(headline[0]) >= 0.75]

        # Print the number of filtered headlines
        print(f"Number of filtered headlines: {len(filtered_headlines)}")

        # Print the filtered headlines with URLs
        for headline, url in filtered_headlines:
            print(f"{headline}\n{url}\n")

    else:
        print("Error: The 'articles' key is missing in the response.")

else:
    print("Error: Failed to fetch data from NewsAPI.")