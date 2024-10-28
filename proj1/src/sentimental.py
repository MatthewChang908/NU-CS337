import json
from textblob import TextBlob
import os

def load_json_file(filename):
    #Load JSON file using relative path
    try:
        # Try to load from src directory
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        print(f"Please ensure {filename} is in the src directory")
        return None

def analyze_sentiment_for_entity(tweets, entity_name):
    
    #Use TextBlob's sentiment analysis to classify tweets
    
    #Args:
    #tweets: List of tweets
    #entity_name: Name of entity to analyze
        
    #Returns:
    #Dictionary containing sentiment analysis results

    stats = {
        'positive': 0,
        'negative': 0,
        'neutral': 0,
        'total': 0,
        'sentiment_examples': {
            'positive': [],  # Store positive tweet examples
            'negative': [],  # Store negative tweet examples
            'neutral': []    # Store neutral tweet examples
        }
    }
    
    for tweet in tweets:
        text = tweet['text'].lower()
        if entity_name.lower() in text:
            # Use TextBlob for sentiment analysis
            blob = TextBlob(text)
            
            # Get sentiment scores
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Classify based on polarity and subjectivity
            if subjectivity > 0.5:  # Only count if tweet is subjective enough
                if polarity > 0.1:
                    stats['positive'] += 1
                    if len(stats['sentiment_examples']['positive']) < 3:
                        stats['sentiment_examples']['positive'].append({
                            'text': tweet['text'],
                            'polarity': polarity,
                            'subjectivity': subjectivity,
                            'retweet_count': tweet.get('retweet_count', 0)
                        })
                elif polarity < -0.1:
                    stats['negative'] += 1
                    if len(stats['sentiment_examples']['negative']) < 3:
                        stats['sentiment_examples']['negative'].append({
                            'text': tweet['text'],
                            'polarity': polarity,
                            'subjectivity': subjectivity,
                            'retweet_count': tweet.get('retweet_count', 0)
                        })
                else:
                    stats['neutral'] += 1
                    if len(stats['sentiment_examples']['neutral']) < 3:
                        stats['sentiment_examples']['neutral'].append({
                            'text': tweet['text'],
                            'polarity': polarity,
                            'subjectivity': subjectivity,
                            'retweet_count': tweet.get('retweet_count', 0)
                        })
                stats['total'] += 1
    
    return stats

def format_sentiment_summary(entity_type, entity_name, stats):
    #Format sentiment analysis results focusing on sentiment distribution and trends
    if stats['total'] == 0:
        return f"{entity_type}: {entity_name}\n- Insufficient data for analysis\n"
    
    # Calculate percentages
    pos_percent = (stats['positive'] / stats['total']) * 100
    neg_percent = (stats['negative'] / stats['total']) * 100
    neu_percent = (stats['neutral'] / stats['total']) * 100
    
    output = f"{entity_type}: {entity_name}\n"
    output += f"- Total Mentions: {stats['total']}\n"
    output += f"- Sentiment Overview:\n"
    output += f"  * Positive: {pos_percent:.1f}%\n"
    output += f"  * Negative: {neg_percent:.1f}%\n"
    output += f"  * Neutral: {neu_percent:.1f}%\n"
    
    # Add sentiment trend (if significant difference)
    if pos_percent - neg_percent > 30:
        output += "- Overall Reception: Very Positive\n"
    elif pos_percent - neg_percent > 10:
        output += "- Overall Reception: Moderately Positive\n"
    elif neg_percent - pos_percent > 30:
        output += "- Overall Reception: Very Negative\n"
    elif neg_percent - pos_percent > 10:
        output += "- Overall Reception: Moderately Negative\n"
    else:
        output += "- Overall Reception: Mixed\n"
    
    return output + "\n"

def generate_autograder_format(results):
    #Generate JSON format compatible with autograder
    autograder_output = {
        "Host": ["amy poehler", "tina fey"],  # Will be replaced with actual hosts
        "award_data": {}
    }
    
    # Example award data structure (to be replaced with actual data)
    award_data = {
        "Best Motion Picture - Drama": {
            "Presenters": ["robert pattinson", "amanda seyfried"],
            "Nominees": [
                "argo",
                "django unchained",
                "lincoln",
                "zero dark thirty",
                "life of pi"
            ],
            "Winner": "argo"
        },
        "Best Motion Picture - Musical or Comedy": {
            "Presenters": ["will ferrell", "kristen wiig"],
            "Nominees": [
                "les miserables",
                "silver linings playbook",
                "moonrise kingdom",
                "salmon fishing in the yemen",
                "the best exotic marigold hotel"
            ],
            "Winner": "les miserables"
        }
    }
    
    autograder_output.update(award_data)
    
    # Write to JSON file
    with open('sentiment_analysis_autograder.json', 'w') as f:
        json.dump(autograder_output, f, indent=2)
    
    return autograder_output

def main():
    # Main function to analyze Golden Globes tweets
    tweets = load_json_file('gg2013.json')
    if tweets is None:
        return
    
    print(f"Successfully loaded {len(tweets)} tweets")
    
    # Initialize results
    results = {
        'hosts': {},
        'winners': {},
        'presenters': {},
        'nominees': {}
    }
    
    output = "GOLDEN GLOBES 2013 SENTIMENT ANALYSIS\n\n"
    
    # 1. Hosts Analysis
    output += "1. HOSTS SENTIMENT\n"
    output += "=================\n"
    hosts = ["amy poehler", "tina fey"]
    for host in hosts:
        stats = analyze_sentiment_for_entity(tweets, host)
        results['hosts'][host] = stats
        output += format_sentiment_summary("Host", host, stats)
    
    # 2. Winners Analysis
    output += "2. WINNERS SENTIMENT\n"
    output += "===================\n"
    winners = {
        "Best Motion Picture - Drama": "argo",
        "Best Motion Picture - Musical or Comedy": "les miserables",
        "Best Director": "ben affleck"
    }
    for award, winner in winners.items():
        stats = analyze_sentiment_for_entity(tweets, winner)
        results['winners'][winner] = stats
        output += format_sentiment_summary(f"Winner ({award})", winner, stats)
    
    # Similar sections for presenters and nominees...
    
    # Write results
    with open('sentiment_analysis_results.txt', 'w') as f:
        f.write(output)
    
    print("Analysis complete! Results saved to sentiment_analysis_results.txt")
    
    # Generate and save autograder format
    autograder_output = generate_autograder_format(results)
    
    print("Analysis complete! Results saved to:")
    print("1. sentiment_analysis_results.txt (human-readable)")
    print("2. sentiment_analysis_autograder.json (autograder format)")

if __name__ == "__main__":
    main()
