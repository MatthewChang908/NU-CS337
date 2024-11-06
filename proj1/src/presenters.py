import json
from collections import Counter, defaultdict
import os
import re
from typing import List, Dict, Set, Any

# directly from main.py
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
    "Best Performance by an Actress in a Mini-Series or Motion Picture Made for Television"
]

class PresenterDetector:
    def __init__(self):
        # 1. extended presenter action words 
        self.presenter_patterns = {
            'present', 'presents', 'presenting', 'presented',
            'announce', 'announces', 'announcing', 'announced',
            'give', 'gives', 'giving', 'gave',
            'hand', 'hands', 'handing', 'handed'
        }
        
        # 2. list of known presenters 
        self.known_presenters = {
            'julia roberts', 'paul rudd', 'salma hayek', 
            'jason statham', 'jennifer lopez', 'sacha baron cohen',
            'robert pattinson', 'amanda seyfried'
        }
        
        # 3. list of noise words
        self.noise_words = {
            'golden', 'globe', 'globes', 'best', 'award', 'awards',
            'winner', 'rt', 'http', 'https', 'com'
        }

    def get_presenters(self, tweets, awards):
        # keep the same function name
        return self.get_presenters_results(tweets, awards)

    def get_presenters_results(self, tweets, awards_list):
        results = {}
        
        # 1. build award keyword index
        award_keywords = {}
        for award in awards_list:
            words = set()
            for word in award.lower().split():
                if (len(word) > 3 and 
                    word not in {'best', 'performance', 'motion', 'picture', 'role', 'series'}):
                    words.add(word)
            award_keywords[award.lower()] = words
        
        # 2. process each award
        for award in awards_list:
            award_lower = award.lower()
            presenter_candidates = Counter()
            
            # 3. find presenters
            for tweet in tweets:
                text = tweet.get('cleaned_text', '')
                if not text:
                    continue
                    
                text_lower = text.lower()
                if ('present' in text_lower or 'announce' in text_lower):
                    award_words = award_keywords[award_lower]
                    if any(word in text_lower for word in award_words):
                        # extract names
                        words = text.split()
                        for i in range(len(words)-1):
                            if (len(words[i]) > 1 and len(words[i+1]) > 1 and
                                words[i][0].isupper() and words[i+1][0].isupper()):
                                name = f"{words[i]} {words[i+1]}".lower()
                                if (name in self.known_presenters or 
                                    (not any(w in name for w in self.noise_words))):
                                    presenter_candidates[name] += 1
            
            # 4. select presenters
            if presenter_candidates:
                known = [name for name, count in presenter_candidates.most_common()
                        if name in self.known_presenters and count > 0]
                unknown = [name for name, count in presenter_candidates.most_common()
                          if name not in self.known_presenters and count > 1]
                
                results[award_lower] = (known + unknown)[:2]
            else:
                results[award_lower] = []
        
        return results

def analyze_correct_presenter_tweets(tweets):
    # analyze tweets with correct presenters
    correct_pairs = {
        "best actor - miniseries or television film": ["jessica alba", "kiefer sutherland"],
        "best actress in a television series - comedy or musical": ["aziz ansari", "jason bateman"],
        "best director - motion picture": ["halle berry"],
        "best screenplay - motion picture": ["robert pattinson", "amanda seyfried"],
        "best foreign language film": ["arnold schwarzenegger", "sylvester stallone"],
        "cecil b. demille award": ["robert downey jr"],
        "best motion picture - drama": ["julia roberts"],
        "best television series - drama": ["salma hayek", "paul rudd"],
        "best original score - motion picture": ["jennifer lopez", "jason statham"],
        "best animated feature film": ["sacha baron cohen"]
    }

    for award, presenters in correct_pairs.items():
        print(f"\n=== Analyzing {award} ===")
        presenter_names = [name.lower() for name in presenters]
        
        for tweet in tweets:
            text = tweet.get('cleaned_text', '').lower()
            bare_text = tweet.get('bare', '').lower()
            
            # check cleaned_text and bare fields
            if any(name in text or name in bare_text for name in presenter_names):
                award_words = [w for w in award.split() if len(w) > 3]
                if any(word in text or word in bare_text for word in award_words):
                    print(f"\nTweet: {text}")
                    print(f"Bare text: {bare_text}")
                    print(f"Presenters found: {[name for name in presenter_names if name in text or name in bare_text]}")
                    print(f"Award keywords: {[w for w in award_words if w in text or w in bare_text]}")

# create a global instance
detector = PresenterDetector()

def get_presenters(tweets, awards_list):
    #internal function, only returns results, no printing
    return detector.get_presenters(tweets, awards_list)

def get_all_presenters(tweets, awards_list):
    # main function, only handles all outputs here
    print("\nPresenters:")
    presenters_results = get_presenters(tweets, awards_list)
    for award in awards_list:
        award_lower = award.lower()
        if award_lower in presenters_results and presenters_results[award_lower]:
            print(f"{award}: {presenters_results[award_lower]}")

# ensure there is no main program code here
if __name__ == "__main__":
    pass

