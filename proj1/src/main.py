import json
from collections import defaultdict
import os
import pandas as pd
from preprocessing import load_tweets, preprocess_tweets
from redcarpet import main as redcarpet_main  # 直接导入redcarpet的main函数

# STEP 1: Get the winner of the award given the award and the nominees
def get_winner(tweets, award, nominees):
    # Get all tweets
    # Populate Regex expressions and get tweets that follow Nominee wins Award
    regex_templates = [
        "NOMINEE has won award for AWARD",
        "NOMINEE has won the award for AWARD",
        "NOMINEE wins award for AWARD",
        "NOMINEE wins the award for AWARD",
        "NOMINEE wins AWARD",
        "AWARD award goes to NOMINEE",
        "NOMINEE wins the AWARD award",
        "AWARD goes to NOMINEE",
        "AWARD won by NOMINEE"
    ]
    regex = defaultdict(list)

    for nominee in nominees:
        for template in regex_templates:
            reg = template.replace("NOMINEE", nominee).replace("AWARD", award)
            regex[nominee].append(reg)

    result = defaultdict(int) # mapping nominee to frequency
    # Run the tweets through the regex expressions
    for tweet in tweets:
        found = False
        for nominee in regex:
            if found: 
                break # We can return if we already found a match
            templates = regex[nominee]
            for reg in templates:
                if reg in tweet:
                    result[nominee] += 1
                    found = True
                    break
            if not found:
                if nominee in tweet and award in tweet:
                    result[nominee] += 1
                    found = True
                    break
    
    # Get the winner from the tweets through max frequency
    if not result:
        return ""
    return max(result, key=result.get)

def get_all_winners(tweets, awards):
    results = {}
    for award in awards:
        nominees = award['nominees']
        award_name = award['name']
        winner = get_winner(tweets, award_name, nominees)
        results[award_name] = winner
    nominees = {}
    for award in awards:
        nominees[award['name']] = award['nominees']
    return [results, nominees]

def print_all_winners(results, nominees):
    for award in results:
        print("Award:", award)
        print("Presenters WIP")
        print("Nominees:", nominees[award])
        print("Winner:", results[award])
        print()

# Part 2: Given the award name, return the nominees and the presenter
def get_nominees(tweets, award):
    return 

def get_presenters(tweets, award):
    return

# Part 3: Extract the award names from the tweets
def get_awards(tweets):
    return

# Note: Part 0 (Preprocessing) has been moved to before Part 3
    # This ensures that the tweets are loaded and preprocessed before any analysis
    # The 'tweets' variable is now available for use in subsequent parts
    # revise if its not in the right place
def process_tweet_text(tweet):
    """Convert tweet dictionary to text for analysis"""
    text = tweet.get('cleaned_text', '')
    retweet = tweet.get('retweet_text', '')
    # Combine cleaned text and retweet text if available
    return f"{text} {retweet}".strip() if retweet else text

def main():
    # Part 0: Preprocess all tweets
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = 'gg2013.json'
    input_path = os.path.join(current_dir, input_file)

    print("Loading tweets...")
    df = load_tweets(input_path)
    print(f"Loaded {len(df)} tweets")

    print("Preprocessing tweets...")
    df_processed = preprocess_tweets(df)
    print(f"After processing, {len(df_processed)} English tweets remain")

    # Convert processed tweets to list of dictionaries for analysis
    tweets = df_processed.to_dict('records')
    
    # Load configuration
    config = None
    with open('config.json', 'r') as file:
        config = json.load(file)

    # PART 3: Extract awards
    # Convert tweets to text format for analysis
    tweet_texts = [process_tweet_text(tweet) for tweet in tweets]
    awards_names = get_awards(tweet_texts)

    # PART 2: Get nominees and presenters
    awards = {}
    for award in awards_names:
        obj = {}
        nominees = get_nominees(tweet_texts, award)
        presenters = get_presenters(tweet_texts, award)
        obj['name'] = award
        obj['nominees'] = nominees
        obj['presenters'] = presenters
        awards[award] = obj

    # PART 1: Get winners
    awards = config['Awards']  # TODO: Replace with results from Part 2
    results, nominees = get_all_winners(tweet_texts, awards)
    print_all_winners(results, nominees)

    # redcarpet analysis
    print("\nAnalyzing Red Carpet Fashion...")
    redcarpet_main()

if __name__ == "__main__":
    main()
