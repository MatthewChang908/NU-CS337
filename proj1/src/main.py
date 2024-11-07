import os
import pandas as pd

from host import getHost
from preprocessing import load_tweets, preprocess_tweets
from redcarpet import get_red_carpet_results
from process_awards import process
from nominees import get_nominees
from presenters import get_all_presenters
from awards import get_awards
from interactive_menu import show_menu
from winners import get_all_winners
import awards as a
import results as r
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

def get_tweets(year):
    """Get tweets for a given year"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tweets_file = f'data/gg{year}.json'
    input_path = os.path.join(current_dir, tweets_file)
    try:
        df = load_tweets(input_path)
        
        path = os.path.join(current_dir, f'data/gg{year}_processed.json')
        if os.path.exists(path):
            print(f"Processed tweets for {year} already exist. Skipping preprocessing.")
            df_processed = pd.read_json(path)
        else:
            df_processed = preprocess_tweets(df)
            
        print("Formatting tweets...")
        tweets = df_processed.to_dict('records')
        print("Done")
        return tweets
    except:
        print(f"Error loading tweets for {year}. Please check the file and try again.")
        return []

def main():
    while True:
        print("\nWelcome to our Golden Globes project! Which year would you like to analyze?")
        year = input("Please enter a year: ")
        if not year.isdigit():
            print("Invalid year. Please enter a valid year.")
            continue
        tweets = get_tweets(year)
        if not tweets:
            print("No tweets found for the specified year. Please try again.")
            continue
        tweet_texts = [get_bare_text(tweet) for tweet in tweets]
        awards = process()
        
        print("\nWelcome to our Golden Globes project! What would you like to do?")
        print("1. Show Host(s)")
        print("2. Show Award Categories")
        print("3. Show Presenters")
        print("4. Show Nominees")
        print("5. Show Winners")
        print("6. Show Red Carpet Analysis")
        print("7. Get All Results to File")
        print("8. Exit")
        
        choice = input("\nPlease enter a number (1-7): ")
        
        if choice == "1":
            getHost(tweet_texts)
        elif choice == "2":
            a.get_awards(tweet_texts)
        elif choice == "3":
            get_all_presenters(tweets, AWARDS_LIST)
        elif choice == "4":
            get_nominees(tweet_texts, awards)
        elif choice == "5":
            get_all_winners(tweet_texts, awards)
        elif choice == "6":
            print(get_red_carpet_results())
        elif choice == "7":
            print("\nGetting all results...")
            host = getHost(tweet_texts, print_results=False)
            pres = get_all_presenters(tweets, print_results=False)
            nominees = get_nominees(tweet_texts, awards, print_results=False)
            winners = get_all_winners(tweet_texts, awards, print_results=False)
            print("Results saved to results.json")
            # r.output_results(awards, host, presenters, nominees, winners)
        elif choice == "8":
            print("\nThank you for using our app!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
    
if __name__ == "__main__":
    
    main()
