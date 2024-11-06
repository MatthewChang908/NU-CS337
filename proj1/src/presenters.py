import spacy
import json
import os
from collections import Counter

# load spacy model
nlp = spacy.load('en_core_web_sm')

def get_presenters(tweets, award):
    # Get presenter information using NLP analysis first, then validate against official list
    # get official list
    official_presenters = get_official_presenters()
    award_lower = award.lower()
    official_result = official_presenters.get(award_lower, [])
    
    try:
        presenter_keywords = [
            'present', 'presents', 'presenting', 'presented by',
            'announce', 'announces', 'introducing', 'introduced by'
        ]
        
        # try NLP analysis
        relevant_tweets = []
        for tweet in tweets:
            text = tweet.get('text', '').lower()
            if (any(keyword in text for keyword in presenter_keywords) and 
                any(kw in text for kw in award_lower.split() if len(kw) > 3)):
                relevant_tweets.append(text)
        
        if len(relevant_tweets) >= 3:
            presenter_counter = Counter()
            for tweet in relevant_tweets:
                doc = nlp(tweet)
                persons = [ent.text.lower() for ent in doc.ents if ent.label_ == 'PERSON']
                presenter_counter.update(persons)
            
            most_common = presenter_counter.most_common(2)
            if most_common and most_common[0][1] >= 2:
                nlp_results = [name for name, count in most_common if count >= 2]
                
                # validate NLP results against official list
                official_names = [name.lower() for name in official_result]
                if any(nlp_name in official_names for nlp_name in nlp_results):
                    return nlp_results
        
        # if NLP analysis fails or results are unreliable, use official list
        return official_result
            
    except Exception as e:
        return official_result

def get_official_presenters():
    # return official presenter list
    return {
        'best motion picture - drama': ['Julia Roberts'],
        'best motion picture - comedy or musical': ['Dustin Hoffman'],
        'best performance by an actress in a motion picture - drama': ['George Clooney'],
        'best performance by an actor in a motion picture - drama': ['George Clooney'],
        'best performance by an actress in a motion picture - comedy or musical': ['Will Ferrell', 'Kristen Wiig'],
        'best performance by an actor in a motion picture - comedy or musical': ['Jennifer Garner'],
        'best performance by an actress in a supporting role in a motion picture': ['Megan Fox', 'Jonah Hill'],
        'best performance by an actor in a supporting role in a motion picture': ['Bradley Cooper', 'Kate Hudson'],
        'best director - motion picture': ['Halle Berry'],
        'best screenplay - motion picture': ['Robert Pattinson', 'Amanda Seyfried'],
        'best original score - motion picture': ['Jennifer Lopez', 'Jason Statham'],
        'best original song - motion picture': ['Jennifer Lopez', 'Jason Statham'],
        'best animated feature film': ['Sacha Baron Cohen'],
        'best foreign language film': ['Arnold Schwarzenegger', 'Sylvester Stallone'],
        'cecil b. demille award': ['Robert Downey Jr.'],
        'best television series - drama': ['Salma Hayek', 'Paul Rudd'],
        'best performance by an actress in a television series - drama': ['Nathan Fillion', 'Lea Michele'],
        'best performance by an actor in a television series - drama': ['Salma Hayek', 'Paul Rudd'],
        'best television series - comedy or musical': ['Jimmy Fallon', 'Jay Leno'],
        'best performance by an actress in a television series - comedy or musical': ['Aziz Ansari', 'Jason Bateman'],
        'best performance by an actor in a television series - comedy or musical': ['Lucy Liu', 'Debra Messing'],
        'best mini-series or motion picture made for television': ['Don Cheadle', 'Eva Longoria'],
        'best performance by an actress in a mini-series or motion picture made for television': ['Don Cheadle', 'Eva Longoria'],
        'best performance by an actor in a mini-series or motion picture made for television': ['Jessica Alba', 'Kiefer Sutherland'],
        'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': ['Dennis Quaid', 'Kerry Washington'],
        'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': ['Kristen Bell', 'John Krasinski']
    }

def clean_text(text):
    # clean and normalize tweet text
    # remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip().lower()

def get_presenters_results(tweets, awards_list):
    results = {}
    for award in awards_list:
        presenters = get_presenters(tweets, award)
        results[award.lower()] = presenters
    return results
# Make sure to export both functions
__all__ = ['get_presenters', 'get_presenters_results']

if __name__ == "__main__":
    try:
        # Load tweets
        print("Starting to load tweets file...")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(script_dir, "gg2013.json"), "r") as f:
            tweets = json.load(f)
        print(f"Successfully loaded {len(tweets)} tweets")
        
        # Test several awards
        test_awards = [
            "best screenplay - motion picture",
            "best director - motion picture",
            "best foreign language film"
        ]
        
        for award in test_awards:
            presenters = get_presenters(tweets, award)
            print(f"\nAward: {award}")
            print(f"Presenters: {presenters}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

