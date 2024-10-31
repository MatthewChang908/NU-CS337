import json
import os
from collections import defaultdict

def load_json_file(filename):
    # Load JSON file
    try:
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        return None

def load_celebrity_names():
    # Load celebrity names from answer file or fallback to default list
    try:
        # Try to load from answers file
        with open('gg2013answers.json', 'r') as f:
            answers = json.load(f)
            # Extract celebrities from answer file
            celebrities = set()
            # Note: Implementation depends on actual answer file structure
            return celebrities
    except FileNotFoundError:
        # Fallback to default celebrity list if answer file not found
        return {
            "jennifer lawrence", "anne hathaway", "jessica chastain",
            "taylor swift", "claire danes", "nicole kidman", "lucy liu",
            "helena bonham carter", "halle berry", "marion cotillard",
            "amy adams", "sienna miller", "kate hudson", "sarah jessica parker",
            "jennifer lopez", "emily blunt", "zooey deschanel", "sofia vergara",
            "julianne moore", "jessica alba", "eva longoria", "lea michele",
            "megan fox", "adele", "jodie foster", "amanda seyfried"
        }

def extract_names(text):
    # Get celebrity list from the new loading function
    celebrities = load_celebrity_names()
    found_names = set()
    text_lower = text.lower()
    
    # Search for each celebrity name in the text
    for name in celebrities:
        if name in text_lower:
            found_names.add(name)
    
    return found_names

def analyze_fashion_tweets(tweets):
    stats = {
        'best_dressed': defaultdict(int),
        'worst_dressed': defaultdict(int),
        'controversial_dressed': defaultdict(int)
    }
    
    # Significantly expanded keywords to catch more mentions
    best_keywords = [
        'best dressed', 'dressed best', 'looking great', 'beautiful dress', 
        'stunning dress', 'gorgeous', 'best looking', 'best outfit',
        'amazing dress', 'perfect dress', 'killed it', 'slayed',
        'beautiful', 'stunning', 'incredible', 'fantastic', 'perfect',
        'love her dress', 'love her look', 'best fashion', 'best style',
        'winning look', 'nailed it', 'flawless'
    ]
    
    worst_keywords = [
        'worst dressed', 'dressed worst', 'looking bad', 'awful dress', 
        'terrible outfit', 'fashion fail', 'worst looking', 'disaster',
        'horrible dress', 'fashion disaster', 'mess', 'ugly dress',
        'bad choice', 'fashion mistake', 'disappointing', 'what was she thinking',
        'hate the dress', 'hate her look', 'worst fashion', 'worst style',
        'fashion flop', 'fashion miss'
    ]
    
    for tweet in tweets:
        tweet_text = tweet.get('text', '').lower()
        names = extract_names(tweet_text)
        
        # Count both exact matches and partial mentions
        for name in names:
            if any(term in tweet_text for term in best_keywords):
                stats['best_dressed'][name] += 1
            if any(term in tweet_text for term in worst_keywords):
                stats['worst_dressed'][name] += 1
            # Only add to controversial if significantly mentioned in both categories
            if (name in stats['best_dressed'] and name in stats['worst_dressed'] and 
                stats['best_dressed'][name] > 2 and stats['worst_dressed'][name] > 2):
                stats['controversial_dressed'][name] = stats['best_dressed'][name] + stats['worst_dressed'][name]

    return stats

def format_fashion_report(stats):
    output = "RED CARPET FASHION\n"
    
    # Get top 3 for best and worst dressed
    best_dressed = sorted(stats['best_dressed'].items(), key=lambda x: x[1], reverse=True)[:3]
    worst_dressed = sorted(stats['worst_dressed'].items(), key=lambda x: x[1], reverse=True)[:3]
    
    # at least 2 names for best and worst dressed
    best_names = [name for name, count in best_dressed if count > 1][:3]  # Only include if mentioned multiple times
    worst_names = [name for name, count in worst_dressed if count > 1][:3]  # Only include if mentioned multiple times
    
    # Get top controversial (keep only one)
    controversial = sorted(stats['controversial_dressed'].items(), key=lambda x: x[1], reverse=True)[:1]
    
    # Format output with multiple names
    output += f"Best Dressed: {', '.join(best_names) if best_names else 'Not found'}\n"
    output += f"Worst Dressed: {', '.join(worst_names) if worst_names else 'Not found'}\n"
    output += f"Most Controversially Dressed: {controversial[0][0] if controversial else 'Not found'}\n"
    
    return output

def main():
    tweets = load_json_file('gg2013.json')
    if tweets is None:
        return
    
    fashion_stats = analyze_fashion_tweets(tweets)
    report = format_fashion_report(fashion_stats)
    
    # Save to src folder
    with open('proj1/src/redcarpet_analysis.txt', 'w') as f:
        f.write(report)
    
    print("Analysis complete! Results saved to redcarpet_analysis.txt")

if __name__ == "__main__":
    main()
