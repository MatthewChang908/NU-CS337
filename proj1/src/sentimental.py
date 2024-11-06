import json
from textblob import TextBlob
import os
from main import AWARDS_LIST
from winners import get_winner
from presenters import get_presenters
from nominees import get_nominees

def load_json_file(filename):
    # Load JSON file using relative path
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
    # Analyze sentiment for a specific entity in tweets
    stats = {
        'positive': 0,
        'negative': 0,
        'neutral': 0,
        'total': 0
    }
    
    for tweet in tweets:
        text = tweet.get('text', '').lower()
        if entity_name.lower() in text:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                stats['positive'] += 1
            elif polarity < -0.1:
                stats['negative'] += 1
            else:
                stats['neutral'] += 1
            stats['total'] += 1
    
    return stats

def write_sentiment_results(sentiment_data, output_file='sentiment_analysis_results.txt'):
    # include all five categories results writing function
    with open(output_file, 'w') as f:
        # Hosts section
        f.write("HOSTS SENTIMENT\n")
        f.write("=================\n")
        for host, data in sentiment_data['hosts'].items():
            f.write(f"Host: {host}\n")
            f.write(f"Overall Reception: {data['reception']}\n\n")
        
        # Winners section
        f.write("WINNERS SENTIMENT\n")
        f.write("===================\n")
        for winner, data in sentiment_data['winners'].items():
            f.write(f"Winner: {winner}\n")
            f.write(f"Overall Reception: {data['reception']}\n\n")
        
        # Presenters section
        f.write("PRESENTERS SENTIMENT\n")
        f.write("=======================\n")
        for presenter, data in sentiment_data['presenters'].items():
            f.write(f"Presenter: {presenter}\n")
            f.write(f"Overall Reception: {data['reception']}\n\n")
        
        # Performances section
        f.write("PERFORMANCES SENTIMENT\n")
        f.write("=======================\n")
        for performer, data in sentiment_data['performances'].items():
            f.write(f"Performance by: {performer}\n")
            f.write(f"Overall Reception: {data['reception']}\n\n")
        
        # Nominees section
        f.write("NOMINEES SENTIMENT\n")
        f.write("===================\n")
        for nominee, data in sentiment_data['nominees'].items():
            f.write(f"Nominee: {nominee}\n")
            f.write(f"Overall Reception: {data['reception']}\n\n")

def determine_reception(pos_percent, neg_percent):
    if pos_percent - neg_percent > 30:
        return "Very Positive"
    elif pos_percent - neg_percent > 10:
        return "Moderately Positive"
    elif neg_percent - pos_percent > 30:
        return "Very Negative"
    elif neg_percent - pos_percent > 10:
        return "Moderately Negative"
    else:
        return "Neutral"

def main():
    tweets = load_json_file('gg2013.json')
    if tweets is None:
        return
    
    print(f"Successfully loaded {len(tweets)} tweets")
    
    # preprocessing: only extract text content
    tweet_texts = [tweet['text'] for tweet in tweets]  # pass text list to get_winner
    
    # initialize results
    formatted_results = {
        'hosts': {},
        'winners': {},
        'presenters': {},
        'performances': {},
        'nominees': {}
    }
    
    # Process hosts
    hosts = ["amy poehler", "tina fey"]
    for host in hosts:
        stats = analyze_sentiment_for_entity(tweets, host)  # use original tweets for sentiment analysis
        if stats and stats['total'] > 0:
            formatted_results['hosts'][host] = {
                'reception': determine_reception(
                    (stats['positive'] / stats['total'] * 100),
                    (stats['negative'] / stats['total'] * 100)
                )
            }
    
    # Process awards
    for award in AWARDS_LIST:
        # Winners - pass text list instead of dict list
        winner = get_winner(tweet_texts, award)  # here changed
        if winner:
            stats = analyze_sentiment_for_entity(tweets, winner)
            if stats and stats['total'] > 0:
                formatted_results['winners'][winner] = {
                    'reception': determine_reception(
                        (stats['positive'] / stats['total'] * 100),
                        (stats['negative'] / stats['total'] * 100)
                    )
                }
        
        # Presenters
        presenters = get_presenters(tweets, award)
        for presenter in presenters:
            stats = analyze_sentiment_for_entity(tweets, presenter)
            if stats and stats['total'] > 0:
                formatted_results['presenters'][presenter] = {
                    'reception': determine_reception(
                        (stats['positive'] / stats['total'] * 100),
                        (stats['negative'] / stats['total'] * 100)
                    )
                }
        
        # Nominees
        nominees = get_nominees(tweets, award)
        for nominee in nominees:
            stats = analyze_sentiment_for_entity(tweets, nominee)
            if stats and stats['total'] > 0:
                formatted_results['nominees'][nominee] = {
                    'reception': determine_reception(
                        (stats['positive'] / stats['total'] * 100),
                        (stats['negative'] / stats['total'] * 100)
                    )
                }
        
        # Performances (focus on performance category)
        if 'performance' in award.lower() or 'actor' in award.lower() or 'actress' in award.lower():
            if winner:
                perf_stats = analyze_sentiment_for_entity(tweets, winner, performance_context=True)
                if perf_stats and perf_stats['total'] > 0:
                    formatted_results['performances'][winner] = {
                        'reception': determine_reception(
                            (perf_stats['positive'] / perf_stats['total'] * 100),
                            (perf_stats['negative'] / perf_stats['total'] * 100)
                        )
                    }
    
    # Write results
    write_sentiment_results(formatted_results)
    print("Analysis complete! Results saved to sentiment_analysis_results.txt")
    return formatted_results

if __name__ == "__main__":
    main()
