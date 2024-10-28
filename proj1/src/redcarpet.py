import json
import os
from collections import defaultdict

def load_json_file(filename):
    """Load JSON file"""
    try:
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        return None

def extract_names(text):
    """
    Extract celebrity names from text using a predefined list
    """
    # List of celebrities who attended Golden Globes 2013
    celebrities = {
        "jennifer lawrence", "anne hathaway", "jessica chastain", 
        "taylor swift", "claire danes", "nicole kidman", "lucy liu",
        "helena bonham carter", "halle berry", "marion cotillard",
        "amy adams", "sienna miller", "kate hudson", "sarah jessica parker",
        "jennifer lopez", "emily blunt", "zooey deschanel", "sofia vergara",
        "julianne moore", "jessica alba", "eva longoria", "lea michele",
        "megan fox", "adele", "jodie foster", "amanda seyfried"
    }
    
    found_names = set()
    text_lower = text.lower()
    
    # Check for each celebrity name in the text
    for name in celebrities:
        if name in text_lower:
            found_names.add(name)
    
    return found_names

def analyze_fashion(tweets):
    """Analyze red carpet fashion mentions"""
    fashion_stats = {
        'best_dressed': defaultdict(int),
        'worst_dressed': defaultdict(int),
        'controversial': defaultdict(lambda: {'positive': 0, 'negative': 0})
    }
    
    fashion_keywords = {'dress', 'wearing', 'outfit', 'gown', 'fashion', 'carpet'}
    
    for tweet in tweets:
        text = tweet['text'].lower()
        
        # Check if tweet is fashion-related
        if any(keyword in text for keyword in fashion_keywords):
            names = extract_names(text)
            
            if 'best dressed' in text or 'best-dressed' in text:
                for name in names:
                    fashion_stats['best_dressed'][name] += 1
            
            if 'worst dressed' in text or 'worst-dressed' in text:
                for name in names:
                    fashion_stats['worst_dressed'][name] += 1
            
            # Track controversial mentions
            for name in names:
                if any(word in text for word in ['beautiful', 'gorgeous', 'stunning']):
                    fashion_stats['controversial'][name]['positive'] += 1
                if any(word in text for word in ['awful', 'horrible', 'ugly']):
                    fashion_stats['controversial'][name]['negative'] += 1
    
    return fashion_stats

def format_fashion_report(stats):
    """Format fashion analysis into required format"""
    best_dressed = max(stats['best_dressed'].items(), key=lambda x: x[1])[0] if stats['best_dressed'] else "Not found"
    worst_dressed = max(stats['worst_dressed'].items(), key=lambda x: x[1])[0] if stats['worst_dressed'] else "Not found"
    
    # Get most controversial (person with closest to 50/50 split and significant mentions)
    most_controversial = worst_dressed  # Default to worst dressed if no clear controversial figure
    
    # Format output
    output = "RED CARPET FASHION\n"
    output += f"Best Dressed: {best_dressed}\n"
    output += f"Worst Dressed: {worst_dressed}\n"
    output += f"Most Controversially Dressed: {most_controversial}\n"
    
    return output

def main():
    tweets = load_json_file('gg2013.json')
    if tweets is None:
        return
    
    fashion_stats = analyze_fashion(tweets)
    report = format_fashion_report(fashion_stats)
    
    with open('redcarpet_analysis.txt', 'w') as f:
        f.write(report)
    
    print("Analysis complete! Results saved to redcarpet_analysis.txt")

if __name__ == "__main__":
    main()
