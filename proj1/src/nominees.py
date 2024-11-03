from collections import defaultdict
import spacy
import json
nlp = spacy.load("en_core_web_sm")

def get_nominees(tweets, awards):
    movies_set = set()
    with open("movie_names.json", "r") as json_file:
        movie_names = json.load(json_file)
        movies_set = set(movie_names)
    
    celebs_set = set()
    with open("recent_celebrity_names.json", "r") as json_file:
        celebs = json.load(json_file)
        celebs_set = set(celebs['recent_celebrity_names'])
    
    print("Getting Nominees")
    nominee_prediction_phrases = [
        "should have been",
        "should've been",
    ]
    
    for phrase in nominee_prediction_phrases:
        tweets = [tweet for tweet in tweets if phrase not in tweet]    
    tweets = [tweet for tweet in tweets if "nominated" in tweet or "nominee" in tweet]
    nominees = {}
    for award in awards:
        nominees[award] = get_nominees_counts(tweets, awards[award], movies_set, celebs_set)
    return nominees
    
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