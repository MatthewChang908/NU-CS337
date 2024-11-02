import os
import json
import re
import pandas as pd
import ftfy
import unicodedata
from unidecode import unidecode
import datetime
import concurrent.futures
from langid import classify

def detect_language(text):
    language, _ = classify(text)
    return language

def load_tweets(file_path: str, limit: int = None) -> pd.DataFrame:
    # Load tweets from a JSON file into a pandas DataFrame, with an optional limit on the number of tweets.
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return pd.DataFrame(data[:limit] if limit else data)

def preprocess_and_extract_features(text: str, timestamp_ms: int) -> dict:
    # Basic cleaning
    text = ftfy.fix_text(text)
    text = unicodedata.normalize('NFKD', text)
    
    # Check if it's a retweet
    is_retweet = text.startswith('RT @')
    bare_text = text
    # remove retweet text
    if is_retweet:
        print("old", bare_text)
        bare_text = " ".join(text.split()[2:])
        print("new", bare_text)

    # Extract hashtags and mentions before cleaning
    hashtags = re.findall(r'#(\w+)', text)
    # remove hashtags
    bare_text = re.sub(r'#\w+', '', bare_text)

    mentions = re.findall(r'@(\w+)', text)
    # remove mentions
    bare_text = re.sub(r'@\w+', '', bare_text)
    
    # Remove URLs (including shortened ones like httptco)
    text_without_urls = re.sub(r'https?://\S+|www\.\S+|httptco\S+', '', text)
    bare_text = re.sub(r'https?://\S+|www\.\S+|httptco\S+', '', bare_text)

    # Remove hashtags and mentions for language detection
    text_for_lang_detect = re.sub(r'#\w+|@\w+', '', text_without_urls)
    language = detect_language(text_for_lang_detect)

    
    # Clean the text
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s@#\']', '', text_without_urls)
    bare_text = re.sub(r'[^a-zA-Z0-9\s@#\']', '', bare_text)
    cleaned_text = cleaned_text.strip()  # Remove extra whitespace
    bare_text = bare_text.strip()
    return {
        'cleaned_text': cleaned_text,
        'hashtags': hashtags,
        'mentions': mentions,
        'retweet_text': text if is_retweet else None, #for sentimental analysis and aw
        'timestamp': datetime.datetime.fromtimestamp(int(timestamp_ms)/1000.0), # sentimental analysis
        'language': language,
        'bare': bare_text
    }

def preprocess_tweets(df: pd.DataFrame) -> pd.DataFrame:
    # Preprocess tweets in the DataFrame, keeping only English tweets
    processed = df.apply(lambda row: preprocess_and_extract_features(row['text'], row['timestamp_ms']), axis=1)
    df_processed = pd.DataFrame(processed.tolist())
    
    # Keep only English tweets
    df_processed = df_processed[df_processed['language'] == 'en']
    
    # Drop the language column
    df_processed = df_processed.drop('language', axis=1)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = 'gg2013_processed.json'
    output_path = os.path.join(current_dir, output_file)
    print(f"Saving processed tweets to {output_path}")
    df_processed.to_json(output_path, orient='records', force_ascii=False, indent=4)
    print("Processing complete.")
    print(f"After processing, {len(df_processed)} English tweets remain")
    return df_processed

def main(input_file: str, output_file: str):
    # Main function: load tweets, preprocess, and save results
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, input_file)
    
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found")
        return

    print("Loading tweets...")
    df = load_tweets(input_path)
    print(f"Loaded {len(df)} tweets")

    print("Preprocessing tweets...")
    df_processed = preprocess_tweets(df)
    print(f"After processing, {len(df_processed)} English tweets remain")

    # Modified output format: removed lines=True to generate standard JSON array with orient='records'
    output_path = os.path.join(current_dir, output_file)
    print(f"Saving processed tweets to {output_path}")
    df_processed.to_json(output_path, orient='records', force_ascii=False, indent=4)
    print("Processing complete.")

if __name__ == "__main__":
    input_file = 'gg2013.json'
    output_file = 'gg2013_processed.json'
    main(input_file, output_file)  