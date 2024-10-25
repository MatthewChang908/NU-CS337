import os
import json
import re
import pandas as pd
import ftfy
import unicodedata
from langdetect import detect, LangDetectException
from unidecode import unidecode
import datetime

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
    
    # Extract hashtags and mentions before cleaning
    hashtags = re.findall(r'#(\w+)', text)
    mentions = re.findall(r'@(\w+)', text)
    
    # Remove URLs (including shortened ones like httptco)
    text_without_urls = re.sub(r'https?://\S+|www\.\S+|httptco\S+', '', text)
    
    # Remove hashtags and mentions for language detection
    text_for_lang_detect = re.sub(r'#\w+|@\w+', '', text_without_urls)
    
    # Detect language
    try:
        language = detect(text_for_lang_detect)
    except LangDetectException:
        language = 'unknown'
    
    # Clean the text
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s@#\']', '', text_without_urls)
    cleaned_text = ' '.join(cleaned_text.split())  # Remove extra whitespace
    
    return {
        'cleaned_text': cleaned_text,
        'hashtags': hashtags,
        'mentions': mentions,
        'retweet_text': text if is_retweet else None, #for sentimental analysis and aw
        'timestamp': datetime.datetime.fromtimestamp(int(timestamp_ms)/1000.0), # sentimental analysis
        'language': language
    }

def preprocess_tweets(df: pd.DataFrame) -> pd.DataFrame:
    # Preprocess tweets in the DataFrame, keeping only English tweets
    processed = df.apply(lambda row: preprocess_and_extract_features(row['text'], row['timestamp_ms']), axis=1)
    df_processed = pd.DataFrame(processed.tolist())
    
    # Keep only English tweets
    df_processed = df_processed[df_processed['language'] == 'en']
    
    # Drop the language column
    df_processed = df_processed.drop('language', axis=1)
    
    return df_processed

def main(input_file: str, output_file: str):
    # Main function: load tweets, preprocess, and save results
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Build the full path for the input file
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

    # Build the full path for the output file
    output_path = os.path.join(current_dir, output_file)
    print(f"Saving processed tweets to {output_path}")
    df_processed.to_json(output_path, orient='records', lines=True, force_ascii=False)
    print("Processing complete.")

if __name__ == "__main__":
    input_file = 'gg2013.json'
    output_file = 'gg2013_processed.json'
    main(input_file, output_file)  
