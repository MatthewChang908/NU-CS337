from collections import defaultdict
import re
import spacy
import json

def get_winner(tweets, award, nlp, films):
    # Define regex patterns for person and award matching
    person_first_pattern = re.compile(r"(.*?) (has won|wins?) (the award for )?AWARD", re.IGNORECASE)
    award_first_pattern = re.compile(r"AWARD (award )?(goes to|won by) (.*?)", re.IGNORECASE)

    result = defaultdict(int)
    for tweet in tweets:
        for a in award['formatted']:
            a_escaped = re.escape(a)  # Escape award name for regex safety
            # Compile patterns for the current award format
            person_first = re.compile(person_first_pattern.pattern.replace("AWARD", a_escaped), re.IGNORECASE)
            award_first = re.compile(award_first_pattern.pattern.replace("AWARD", a_escaped), re.IGNORECASE)

            # Process if award type is "Movie/song"
            if award['category'] == "Movie":
                # Check for person-first pattern
                person_match = person_first.search(tweet)
                if person_match:
                    first_part = person_match.group(1)
                    subphrases = get_all_subphrases(first_part)
                    for s in subphrases:
                        if s in films:
                            result[s.lower()] += 1
                    doc = nlp(first_part)
                    entities = [ent.text.lower() for ent in doc.ents]
                    for ent in entities:
                        result[ent] += 1

                # Check for award-first pattern
                award_match = award_first.search(tweet)
                if award_match:
                    second_part = award_match.group(3)
                    subphrases = get_all_subphrases(second_part)
                    for s in subphrases:
                        if s in films:
                            result[s.lower()] += 1
                    doc = nlp(second_part)
                    entities = [ent.text.lower() for ent in doc.ents]
                    for ent in entities:
                        result[ent] += 1

            # Process if award type is "Person"
            elif award['category'] == "Person":
                # Check for person-first pattern
                person_match = person_first.search(tweet)
                if person_match:
                    first_part = person_match.group(1)
                    doc = nlp(first_part)
                    entities = [ent.text.lower() for ent in doc.ents]
                    for ent in entities:
                        result[ent] += 1

                # Check for award-first pattern
                award_match = award_first.search(tweet)
                if award_match:
                    second_part = award_match.group(3)
                    doc = nlp(second_part)
                    entities = [ent.text.lower() for ent in doc.ents]
                    for ent in entities:
                        result[ent] += 1
    # Get the winner from the tweets through max frequency
    if not result:
        return ""
    return max(result, key=result.get)

def get_all_winners(tweets, awards, print_results=True):
    
    with open("data/awards.json", "r") as json_file:
        awards = json.load(json_file)

    # Filter tweets that contain winning-related words
    tweets = [tweet for tweet in tweets if re.search(r"\bwins?\b|\bwon\b|\bgoes\b|\bwon by\b", tweet, re.IGNORECASE)]
    nlp = spacy.load("en_core_web_sm")
    
    # Load the set of known movie names
    movies_set = set()
    with open("data/movie_names.json", "r") as json_file:
        movie_names = json.load(json_file)
        movies_set = set(movie_names)
        
    shows_set = set()
    with open("data/tv_shows.json", "r") as json_file:  
        tv_shows = json.load(json_file)
        shows_set = set(tv_shows)
        
    films = movies_set | shows_set
    if print_results:
        print("\nWinners:") 
    results = {}
    for award in awards:
        winner = get_winner(tweets, awards[award], nlp, films)
        results[award] = winner.capitalize()
        if print_results:
            print("Award:", award)
            print("Winner:", winner)
            print()
    return results

def get_all_subphrases(sentence):
    words = sentence.split()
    subphrases = []
    for i in range(len(words)):
        for j in range(i + 1, len(words) + 1):
            subphrases.append(" ".join(words[i:j]))
    return subphrases