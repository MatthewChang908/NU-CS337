import spacy
from collections import Counter
import re
import json
import os

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
    "Best Performance by an Actress in a Mini-Series or Motion Picture Made for Television",
]

def get_all_presenters(tweets, awards_list):
    detector = PresenterDetector()
    presenters = detector.get_presenters('2013')  # hardcoded year as 2013
    
    # Print results for each award
    for award in awards_list:
        if award in presenters and presenters[award]:
            print(f"{award}: {presenters[award]}")
        else:
            print(f"{award}: []")
    
    return presenters

class PresenterDetector:
    # Class to detect award presenters from tweets
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.awards = [award.lower() for award in AWARDS_LIST]
        
        # Patterns to match presenter pairs and awards
        self.presenter_patterns = [
            r"(\w+\s+\w+)\s+and\s+(\w+\s+\w+)\s+present(?:ing|ed)?\s+(?:the\s+)?(?:nominees\s+for\s+)?(?:award\s+for\s+)?(best\s+.+?)(?:\sto|\.|\#|$)",
            r"(\w+\s+\w+)\s+&\s+(\w+\s+\w+)\s+present(?:ing|ed)?\s+(?:the\s+)?(?:nominees\s+for\s+)?(?:award\s+for\s+)?(best\s+.+?)(?:\sto|\.|\#|$)",
            r"presenters?\s+(\w+\s+\w+)\s+and\s+(\w+\s+\w+)\s+for\s+(best\s+.+?)(?:\sto|\.|\#|$)",
            r"(\w+\s+\w+)\s+(\w+\s+\w+)\s+take\s+the\s+stage\s+to\s+present\s+(best\s+.+?)(?:\sto|\.|\#|$)"
        ]
        self.patterns = [re.compile(p, re.IGNORECASE) for p in self.presenter_patterns]

    def get_presenters(self, year):
        # get the data
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, "data", f"gg{year}_processed.json")
        
        with open(data_path, 'r') as f:
            tweets = json.load(f)
        
        # initialize the presenter dictionary
        presenter_dict = {award: [] for award in AWARDS_LIST}
        
        # 1. find the confirmed presenter pairs
        findings = self.find_presenter_pairs(tweets)
        confirmed_pairs = set()  # record the used presenter pairs
        
        for finding in findings:
            award_name = self.match_to_official_award(finding['award'])
            if award_name:
                presenter_dict[award_name] = finding['presenters']
                confirmed_pairs.add(tuple(finding['presenters']))
        
        # 2. assign the potential presenter pairs to the other awards
        potential_presenters = self.find_potential_presenters(tweets)
        
        # remove the used presenter pairs
        potential_presenters = [pair for pair in potential_presenters 
                              if tuple(pair) not in confirmed_pairs]
        
        # assign the potential presenter pairs to the other awards
        for award in AWARDS_LIST:
            if not presenter_dict[award] and potential_presenters:
                presenter_dict[award] = potential_presenters.pop(0)
        
        return presenter_dict

    def find_presenter_pairs(self, tweets):
        # find the presenter pairs
        findings = []
        seen_pairs = set()
        
        for tweet in tweets:
            texts = []
            if isinstance(tweet, dict):
                if tweet.get('cleaned_text'): texts.append(tweet['cleaned_text'])
                if tweet.get('retweet_text'): texts.append(tweet['retweet_text'])
                if tweet.get('text'): texts.append(tweet['text'])
                if tweet.get('bare'): texts.append(tweet['bare'])
            
            for text in texts:
                text = text.lower()
                
                # only process the tweets containing the presenter words
                if 'present' in text:
                    for pattern in self.patterns:
                        matches = pattern.finditer(text)
                        for match in matches:
                            if len(match.groups()) >= 3:  # unsure to have two names and one award
                                name1, name2, award = match.groups()[:3]
                                if self.validate_name(name1) and self.validate_name(name2):
                                    name_pair = tuple(sorted([name1.lower(), name2.lower()]))
                                    if name_pair not in seen_pairs:
                                        findings.append({
                                            'presenters': [n.title() for n in name_pair],
                                            'award': award,
                                            'text': text
                                        })
                                        seen_pairs.add(name_pair)
        
        return findings

    def match_to_official_award(self, found_award):
        # match the found award to the official award list
        if not found_award:
            return None
            
        found_award = found_award.lower()
        
        # 1. direct match
        if found_award in self.awards:
            return AWARDS_LIST[self.awards.index(found_award)]
            
        # 2. keyword match
        max_match = 0
        best_match = None
        
        found_words = set(found_award.split())
        
        for i, official_award in enumerate(self.awards):
            official_words = set(official_award.split())
            matches = len(found_words & official_words)
            
            if ('actor' in found_words and 'actor' in official_words) or \
               ('actress' in found_words and 'actress' in official_words):
                matches += 2
            
            if matches > max_match:
                max_match = matches
                best_match = AWARDS_LIST[i]
        
        return best_match if max_match >= 3 else None

    def validate_name(self, name):
        # validate the name
        if not name:
            return False
        
        words = name.lower().split()
        if not (2 <= len(words) <= 3):
            return False
        
        noise_words = {'rt', '@', 'golden', 'globe', 'best'}
        if any(word in noise_words for word in words):
            return False
        
        if any(len(word) < 2 for word in words):
            return False
        
        return True

    def find_potential_presenters(self, tweets):
        # find the potential presenter pairs
        presenter_pairs = Counter()
        
        for tweet in tweets:
            texts = []
            if isinstance(tweet, dict):
                if tweet.get('cleaned_text'): texts.append(tweet['cleaned_text'])
                if tweet.get('retweet_text'): texts.append(tweet['retweet_text'])
                if tweet.get('text'): texts.append(tweet['text'])
                if tweet.get('bare'): texts.append(tweet['bare'])
            
            for text in texts:
                text = text.lower()
                
                # find the tweets containing the presenter words
                if any(word in text for word in ['present', 'announce', 'introducing']):
                    # use NLP to identify the names
                    doc = self.nlp(text)
                    person_ents = [ent.text for ent in doc.ents 
                                 if ent.label_ == 'PERSON' and self.validate_name(ent.text)]
                    
                    # if two names are found, they might be the presenter pairs
                    if len(person_ents) == 2:
                        pair = tuple(sorted([p.title() for p in person_ents]))
                        presenter_pairs[pair] += 1
        
        # return the presenter pairs with the highest frequency
        return [list(pair) for pair, count in presenter_pairs.most_common(30)]

if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, "data", "gg2013_processed.json")
        
        print(f"loading data from: {data_path}")
        with open(data_path, 'r') as f:
            tweets = json.load(f)
            print("data loaded successfully!")
        
        detector = PresenterDetector()
        presenters = detector.get_presenters('2013')
        
        print("\nPresenters:")
        for award, names in presenters.items():
            if names:  
                print(f"{award}: {names}")
            
    except Exception as e:
        print(f"error: {str(e)}")

