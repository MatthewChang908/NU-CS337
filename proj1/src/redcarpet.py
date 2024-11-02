import spacy
import json
import os
from collections import defaultdict

# Fashion-related keywords for sentiment analysis
best_keywords = [
    # Strong positive indicators
    'best dressed', 'dressed best', 'looking great', 'beautiful dress', 
    'stunning dress', 'gorgeous', 'best looking', 'best outfit',
    'amazing dress', 'perfect dress', 'killed it', 'slayed',
    'beautiful', 'stunning', 'incredible', 'fantastic', 'perfect',
    'love her dress', 'love her look', 'best fashion', 'best style',
    'winning look', 'nailed it', 'flawless', 'show stopper',
    'red carpet queen', 'fashion moment', 'serving looks', 
    'understood the assignment', 'ate and left no crumbs',
    'iconic', 'masterpiece', 'perfection', 'absolutely stunning',
    'breathtaking', 'queen', 'style icon', 'fashion goals',
    'best look', 'magnificent', 'divine', 'elegant', 'radiant',
    'glowing', 'phenomenal', 'spectacular', 'outstanding'
]

worst_keywords = [
    # Strong negative indicators
    'worst dressed', 'dressed worst', 'looking bad', 'awful dress', 
    'terrible outfit', 'fashion fail', 'worst looking', 'disaster',
    'horrible dress', 'fashion disaster', 'mess', 'ugly dress',
    'bad choice', 'fashion mistake', 'disappointing', 
    'what was she thinking', 'hate the dress', 'hate her look', 
    'worst fashion', 'worst style', 'fashion flop', 'fashion miss',
    'ill-fitting', 'unflattering', 'missed the mark', 
    'wardrobe malfunction', 'choice was made', 'did her dirty',
    'stylist needs to be fired', 'tragic', 'terrible', 'wtf',
    'not it', 'fail', 'fashion crime', 'hideous', 'awful',
    'what is this', 'no no no', 'make it stop'
]

controversial_keywords = [
    'controversial', 'shocking', 'bold', 'risky', 'daring',
    'questionable', 'interesting choice', 'unusual', 'unique',
    'divided opinions', 'mixed reactions', 'debate', 'polarizing'
]

def extract_names(text, nominees):
    """Extract names from text based on nominees list"""
    found_names = set()
    text = text.lower()
    
    # Check for each nominee in the tweet
    for nominee in nominees:
        if nominee.lower() in text:
            found_names.add(nominee)
    
    return list(found_names)

def load_nominees():
    # Load nominees from config.json"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, 'config.json')
        
        with open(config_path, 'r') as f:
            config_data = json.load(f)
            nominees = set()
            
            # correct handling of nested JSON structure
            for award in config_data.get("Awards", []):
                if "nominees" in award:
                    nominees.update(award["nominees"])
            
            print(f"Loaded {len(nominees)} nominees from config.json")
            return list(nominees)
    except Exception as e:
        print(f"Error loading nominees: {e}")
        return []

def load_tweets():
    try:
        # use relative path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(script_dir, 'gg2013.json')
        
        print(f"Loading tweets from: {data_file}")
        
        with open(data_file, 'r') as f:
            tweets_data = json.load(f)
            print(f"Successfully loaded {len(tweets_data)} tweets")
            return tweets_data
            
    except Exception as e:
        print(f"Error loading tweets: {e}")
        return None

def get_top_three(counter):
    # Helper function to get top 3 names from a counter"""
    top = sorted(counter.items(), key=lambda x: x[1], reverse=True)[:3]
    return [name for name, _ in top] if top else ["Not found"]

def get_top_one(counter):
    # Helper function to get top 1 name from a counter"""
    top = sorted(counter.items(), key=lambda x: x[1], reverse=True)[:1]
    return top[0][0] if top else "Not found"

def get_red_carpet():
    tweets = load_tweets()
    if tweets is None:
        return
        
    # Initialize counters for fashion analysis
    best_dressed = defaultdict(int)
    worst_dressed = defaultdict(int)
    controversial = defaultdict(int)
    most_discussed = defaultdict(int)
    
    # Load spaCy model for name recognition
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading spaCy model...")
        os.system("python -m spacy download en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    
    # Words to exclude from name recognition
    exclude_words = {'golden', 'globes', 'globe', 'goldenglobes', 'rt', '@', 'http', 'https'}
    
    # Fashion-related keywords for tweet filtering
    fashion_keywords = [
        'dress', 'wearing', 'outfit', 'fashion', 'carpet', 'gown', 'style',
        'look', 'wore', 'dressed', 'attire', 'ensemble', 'couture', 
        'designer', 'fashion statement', 'red carpet look', 'stylist',
        'glamorous', 'fashion choice', 'wardrobe', 'clothing', 'wear',
        'fashion moment', 'fashion icon', 'fashion forward', 'runway',
        'fashion police', 'fashionista', 'fashion game', 'slay', 'serve'
    ]
    
    for tweet in tweets:
        text = tweet.get('text', '')
        text_lower = text.lower()
        
        # Check if tweet is fashion-related using expanded keywords
        if any(word in text_lower for word in fashion_keywords):
            # Use spaCy for name extraction
            doc = nlp(text)
            # Extract only valid person names
            names = [
                ent.text for ent in doc.ents 
                if (ent.label_ == "PERSON" and 
                    not any(exclude in ent.text.lower() for exclude in exclude_words) and
                    len(ent.text.split()) >= 2)  # Only accept full names
            ]
            
            for name in names:
                # Check for fashion context with expanded criteria
                if any(word in text_lower for word in [
                    'her', 'she', 'wearing', 'dress', 'outfit', 'wore',
                    'styled', 'looking', 'appeared', 'arrived', 'rocked',
                    'donned', 'chosen', 'picked', 'opted'
                ]):
                    most_discussed[name] += 1
                    
                    # Best dressed mentions
                    if any(keyword in text_lower for keyword in best_keywords):
                        best_dressed[name] += 1
                    
                    # Worst dressed mentions
                    if any(keyword in text_lower for keyword in worst_keywords):
                        worst_dressed[name] += 1
                    
                    # Controversial mentions
                    if any(keyword in text_lower for keyword in controversial_keywords):
                        controversial[name] += 1
    
    # Get results using helper functions
    best_three = get_top_three(best_dressed)
    worst_three = get_top_three(worst_dressed)
    controversial_one = get_top_one(controversial)
    most_discussed_one = get_top_one(most_discussed)
    
    # Save results to redcarpet_analysis.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'redcarpet_analysis.txt')
    
    with open(output_file, 'a') as f:
        f.write("\nRed Carpet Fashion:\n")
        f.write(f"Best Dressed: {', '.join(best_three)}\n")
        f.write(f"Worst Dressed: {', '.join(worst_three)}\n")
        f.write(f"Most Controversially Dressed: {controversial_one}\n")
        f.write(f"Most Discussed: {most_discussed_one}\n")

def main():
    """Main function for standalone execution"""
    print("\nAnalyzing Red Carpet Fashion...")
    get_red_carpet()
    print("Red carpet analysis completed. Results written to redcarpet_analysis.txt")

if __name__ == "__main__":
    main()
