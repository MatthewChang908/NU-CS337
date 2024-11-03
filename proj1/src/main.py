import json
import os
import pandas as pd

from awards import get_awards
from preprocessing import load_tweets, preprocess_tweets
from redcarpet import get_red_carpet
from process_awards import process
from nominees import get_nominees
from presenters import get_presenters
from winners import get_all_winners

def process_tweet_text(tweet):
    """Convert tweet dictionary to text for analysis"""
    text = tweet.get('cleaned_text', '')
    retweet = tweet.get('retweet_text', '')
    # Combine cleaned text and retweet text if available
    return f"{text} {retweet}".strip() if retweet else text
def get_bare_text(tweet):
    """Extract the 'bare' text from a tweet dictionary"""
    return tweet.get('bare', '')
def main():
    # Part 0: Preprocess all tweets
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tweets_file = 'gg2013.json'
    input_path = os.path.join(current_dir, tweets_file)

    print("Loading tweets...")
    df = load_tweets(input_path)
    print(f"Loaded {len(df)} tweets")

    # check if gg2013_processed.json exists
    if os.path.exists(os.path.join(current_dir, 'gg2013_processed.json')):
        print("Processed tweets already exist. Skipping preprocessing.")
        df_processed = pd.read_json('gg2013_processed.json')
    else:
        df_processed = preprocess_tweets(df)
    # Convert processed tweets to list of dictionaries for analysis
    tweets = df_processed.to_dict('records')
    
    # Load configuration
    config = None
    config_path = os.path.join(current_dir, 'config.json')
    with open(config_path, 'r') as file:
        config = json.load(file)

    tweet_texts = [get_bare_text(tweet) for tweet in tweets]
    awards_names = get_awards(tweet_texts)
    print("Awards:", awards_names)
    
        
    # Get presenteres
    awards = process()
    # presenters = get_presenters(tweet_texts, awards)

    # PART 2: Get nominees and presenters
    # Get nominees
    nominees = get_nominees(tweet_texts, awards)

    # PART 1: Get winners
    # TODO: Replace with results from Part 2
    results = get_all_winners(tweet_texts, awards)
    # redcarpet analysis
    print("\nAnalyzing Red Carpet Fashion...")
    get_red_carpet()  # Call the function directly

if __name__ == "__main__":
    main()
