import spacy
import json
import re
nlp = spacy.load("en_core_web_sm")

def all_people(tweets, celebs_set):
    res = set()
    for tweet in tweets:
        doc = nlp(tweet)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                res.add(ent.text)
        set2 = get_person_from_set(tweet, celebs_set)
        res = res.union(set2)
    return res

def get_person_from_set(tweet, celebs_set):
    people = set()
    tweet = tweet.split()
    for i in range(len(tweet)):
        for j in range(i + 1, len(tweet)):
            name = " ".join(tweet[i:j+1])
            if name in celebs_set:
                people.add(name)
    return people

def get_movie_from_set(tweet, movies_set):
    movies = set()
    tweet = tweet.split()
    for i in range(len(tweet)):
        for j in range(i + 1, len(tweet)):
            name = " ".join(tweet[i:j])
            if name in movies_set:
                movies.add(name)
    return movies

def get_tv_from_set(tweet, shows_set):
    shows = set()
    tweet = tweet.split()
    for i in range(len(tweet)):
        for j in range(i + 1, len(tweet)):
            name = " ".join(tweet[i:j])
            if name in shows_set:
                shows.add(name)
    return shows

def get_person_from_nlp(tweet):
    people = set()
    doc = nlp(tweet)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            people.add(ent.text)
    