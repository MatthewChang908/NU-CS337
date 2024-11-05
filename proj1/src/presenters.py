from collections import defaultdict
import re
import json
import os

def get_presenters(tweets, award):
    """Get presenters for a specific award"""
    # 1. Load celebrity names
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "recent_celebrity_names.json")
    
    with open(json_path, "r") as f:
        data = json.load(f)
        celebrity_names_set = {name.lower() for name in data["recent_celebrity_names"]}

    presenters = defaultdict(int)
    
    # 2. Prepare keywords for matching
    award_words = set(award.lower().split())
    presenter_words = ['present', 'presents', 'presenting', 'announce', 'announces', 'announcing']
    
    # 3. Find relevant tweets
    relevant_tweets = []
    for tweet in tweets:
        text = tweet['text'].lower()
        # Relaxed condition: only need to match some award keywords
        award_match = sum(1 for word in award_words if word in text)
        if award_match >= 2 and any(p in text for p in presenter_words):
            relevant_tweets.append(tweet['text'])
    
    # 4. Extract names from relevant tweets
    name_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)'
    
    for tweet in relevant_tweets:
        # Find all possible names
        names = re.findall(name_pattern, tweet)
        
        for name in names:
            name = name.lower().strip()
            if name in celebrity_names_set:
                # Check name context
                context = tweet.lower()[max(0, tweet.lower().find(name)-30):
                                      min(len(tweet), tweet.lower().find(name)+30)]
                
                # Make sure this is a presenter not a winner
                if any(p in context for p in presenter_words) and \
                   not any(w in context for w in ['won', 'winner', 'wins']):
                    # Increase weight based on context quality
                    weight = 1
                    if 'present' in context and any(w in context for w in award_words):
                        weight = 2
                    presenters[name] += weight
    
    # 5. Select presenters
    sorted_presenters = sorted(presenters.items(), key=lambda x: (-x[1], x[0]))
    
    # Debug info
    print(f"\nFound {len(relevant_tweets)} relevant tweets for {award}")
    if presenters:
        print("Top presenter candidates:")
        for p, c in sorted_presenters[:5]:
            print(f"- {p}: {c} points")
    
    # 6. Return results
    if "cecil" in award.lower():
        # Cecil award usually has only one presenter
        return [p for p, c in sorted_presenters[:1] if c >= 2]
    else:
        # Other awards may have 1-2 presenters
        result = []
        for p, c in sorted_presenters[:2]:
            if c >= 2:  # Need at least 2 points
                result.append(p)
        return result

if __name__ == "__main__":
    # Load tweets
    with open(os.path.join(os.path.dirname(__file__), "gg2013.json"), "r") as f:
        tweets = json.load(f)
    
    test_awards = [
        "Best Motion Picture - Drama",
        "Best Director - Motion Picture",
        "Best Screenplay - Motion Picture",
        "Best Foreign Language Film",
        "Cecil B. DeMille Award"
    ]
    
    print("\nTesting presenter detection...")
    for award in test_awards:
        presenters = get_presenters(tweets, award)
        print(f"\nAward: {award}")
        print(f"Presenters: {presenters}")
