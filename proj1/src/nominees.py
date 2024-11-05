from collections import defaultdict
import spacy
import json
nlp = spacy.load("en_core_web_sm")

# 'Safe Sound' is nominated for a GOLDEN GLOBE for Best Song! Thx HFPA HAPPY BDAY! 
# It makes me so happy when movies like Django Unchained get nominated for Best Picture
# Oh wow Argo wins best picture drama All films nominated were great 
# associate nominee names

# award names: [tweets]
# entities: [tweets]
# find overlap?
# tweets: [award name, entity]

# create a map of entities to tweets with the word nominate
# for each award, find the entities that are in the tweets
# count the number of times each entity appears
# return the top 5 entities

def get_nominees(tweets, awards):
    movies_set = set()
    with open("movie_names.json", "r") as json_file:
        movie_names = json.load(json_file)
        movies_set = set(movie_names)
    
    celebs_set = set()
    with open("recent_celebrity_names.json", "r") as json_file:
        celebs = json.load(json_file)
        celebs_set = set(celebs['recent_celebrity_names'])
    
    tweets = preprocess_tweets(tweets)
    
    # get films/celebs that were mentioned with being nominated for something
    things_nominated = []
    for tweet in tweets:
        # TODO
        break
    
    nominees = {}
    for award in awards:
        nominees[award] = get_nominees_counts(tweets, awards[award], movies_set, celebs_set)
        
    print("\nNominees:")
    # for award, noms in nominees.items():
    #     print(f"{award}: {noms}")
    
def get_nominees_counts(tweets, award, movies_set, celebs_set):
    alternatives = award['formatted']
    nominees = defaultdict(int)
    for tweet in tweets:
        for alt in alternatives:
            if alt in tweet:
                doc = nlp(tweet)
                for ent in doc.ents:
                    nominees[ent.text] += 1
    # return a list of the top 5 nominees
    sorted_nominees = sorted(nominees.items(), key=lambda x: x[1], reverse=True)
    category = award['category']
    if category == 'Movie':
        return [nominee for nominee, count in sorted_nominees[:5] if nominee in movies_set]
    elif category == 'Person':
        return [nominee for nominee, count in sorted_nominees[:5] if nominee in celebs_set]
    return [nominee for nominee, count in sorted_nominees[:5]]

def preprocess_tweets(tweets):
    nominee_prediction_phrases = [
        "should have been",
        "should've been",
    ]
    
    negative_phrases = [
        "oscars",
        "oscar",
        "academy",
        "not nominated"
    ]

    phrases_to_exclude = nominee_prediction_phrases + negative_phrases
    
    tweets = [tweet for tweet in tweets if not any(phrase in tweet.lower() for phrase in phrases_to_exclude)]
        
    # nominat as the prefix for nominate, nominated, nomination, etc
    tweets = [tweet for tweet in tweets if "nominat" in tweet or "nominee" in tweet]
    print(f"Number of tweets: {len(tweets)}")
    
    return tweets