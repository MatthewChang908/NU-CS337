import json
import os
import pandas as pd

from host import getHost
from preprocessing import load_tweets, preprocess_tweets
from redcarpet import get_red_carpet_results
from process_awards import process
from nominees import get_nominees
from presenters import get_presenters
from awards import get_awards
from interactive_menu import show_menu
from winners import get_all_winners
import awards as a

AWARDS_LIST = [
    "Best Motion Picture - Drama",
    "Best Motion Picture - Musical or Comedy",
    "Best Performance by an Actor in a Motion Picture - Drama",
    "Best Performance by an Actress in a Motion Picture - Drama",
    "Best Performance by an Actor in a Motion Picture - Musical or Comedy",
    "Best Performance by an Actress in a Motion Picture - Musical or Comedy",
    "Best Performance by an Actor in a Supporting Role in any Motion Picture",
    "Best Performance by an Actress in a Supporting Role in any Motion Picture",
    "Best Director - Motion Picture",
    "Best Screenplay - Motion Picture",
    "Best Original Score - Motion Picture",
    "Best Original Song - Motion Picture",
    "Best Animated Feature Film",
    "Best Foreign Language Film",
    "Best Television Series - Drama",
    "Best Television Series - Musical or Comedy",
    "Best Performance by an Actor in a Television Series - Drama",
    "Best Performance by an Actress in a Television Series - Drama",
    "Best Performance by an Actor in a Television Series - Musical or Comedy",
    "Best Performance by an Actress in a Television Series - Musical or Comedy",
    "Best Performance by an Actor in a Supporting Role in a Series, Miniseries or Motion Picture Made for Television",
    "Best Performance by an Actress in a Supporting Role in a Series, Miniseries or Motion Picture Made for Television",
    "Best Mini-Series or Motion Picture Made for Television",
    "Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television",
    "Best Performance by an Actress in a Mini-Series or Motion Picture Made for Television",
]

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
    tweets_file = 'data/gg2013.json'
    input_path = os.path.join(current_dir, tweets_file)

    print("Loading tweets...")
    df = load_tweets(input_path)
    print(f"Loaded {len(df)} tweets")

    # check if gg2013_processed.json exists
    path = os.path.join(current_dir, 'data/gg2013_processed.json')
    if os.path.exists(path):
        print("Processed tweets already exist. Skipping preprocessing.")
        df_processed = pd.read_json(path)
    else:
        df_processed = preprocess_tweets(df)
    # Convert processed tweets to list of dictionaries for analysis
    tweets = df_processed.to_dict('records')
    
    # Load configuration
    config = None
    config_path = os.path.join(current_dir, 'data/config.json')
    with open(config_path, 'r') as file:
        config = json.load(file)

    tweet_texts = [get_bare_text(tweet) for tweet in tweets]
    
    # HOSTS
    # host = getHost(tweet_texts)
    
    # AWARDS

    # a.get_awards(tweet_texts)
    
    # NOMINEES
    awards = process()
    # get_nominees(tweet_texts, awards)

    get_all_winners(tweet_texts, awards)

    # Get presenters for all awards
    presenters_dict = {}
    print("\nPresenters:")
    for award in AWARDS_LIST:
        award_lower = award.lower()
        presenters = get_presenters(tweets, award_lower)
        if presenters:  # print the awards with presenters
            print(f"{award}: {presenters}")  # print the awards and presenters
        presenters_dict[award_lower] = presenters
    
    # Print red carpet results
    print(get_red_carpet_results())  
    
    # call the interactive menu
    show_menu(
        tweets=tweets,
        awards_list=AWARDS_LIST,
        presenters_dict=presenters_dict
    )


    
if __name__ == "__main__":
    
    main()
