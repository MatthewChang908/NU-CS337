from collections import defaultdict
import spacy
import json
import re
nlp = spacy.load("en_core_web_sm")
import helpers as h

def get_nominees(tweets, awards):
    movies_set = set()
    with open("movie_names.json", "r") as json_file:
        movie_names = json.load(json_file)
        movies_set = set(movie_names)
    
    celebs_set = set()
    with open("recent_celebrity_names.json", "r") as json_file:
        celebs = json.load(json_file)
        celebs_set = set(celebs['recent_celebrity_names'])
    
    shows_set = set()
    with open("tv_shows.json", "r") as json_file:
        shows = json.load(json_file)
        shows_set = set(shows)
    
    tweets = preprocess_tweets(tweets)
    
    # get films/celebs that were mentioned with being nominated for something
    things = defaultdict(int)
    for tweet in tweets:
        
        
        movies = h.get_movie_from_set(tweet, movies_set)
        people = h.get_person_from_set(tweet, celebs_set)
        shows = h.get_tv_from_set(tweet, shows_set)
        
        for movie in movies:
            things[movie] += 1
            
        for person in people:
            things[person] += 1
        
        for show in shows:
            things[show] += 1
    # print(len(things))
    
    nominees = {}
    for award in awards:
        nominees[award] = get_nominees_counts(tweets, awards[award], things)
    print("\nNominees:")
    for award, noms in nominees.items():
        if noms:
            noms = ", ".join([nom[0] for nom in noms])
        else:
            noms = "None Found"
        print(f"{award}: {noms}")
    
def get_nominees_counts(tweets, award, things):
    award_names = award['formatted']
    nominees = defaultdict(int)
    for tweet in tweets:
            
        for alt in award_names:
            if alt in tweet.lower():
                split_tweet = tweet.split()
                for i in range(len(split_tweet)):
                    for j in range(i+1, len(split_tweet)):
                        substring = " ".join(split_tweet[i:j])
                        if substring in things:
                            if substring in nominees:
                                continue
                            else:
                                nominees[substring] = things[substring]
    
    # check if any key is a substring of another key
    keys = list(nominees.keys())
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            if keys[i] in keys[j] and keys[i] in nominees:
                nominees[keys[j]] += nominees[keys[i]]
                del nominees[keys[i]]
    
    # return a list of the top 5 nominees
    return sorted(nominees.items(), key=lambda x: x[1], reverse=True)[:5]

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
    return tweets

def split_camel_case(text):
    return ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', text))

def remove_gg(text):
    # remove the words "golden globe" or "goldenglobe" from the text
    return re.sub(r'golden ?globe', '', text, flags=re.IGNORECASE)