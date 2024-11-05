from collections import defaultdict
import re
import spacy
import json

def get_winner(tweets, award):
    tweets = [tweet for tweet in tweets if "wins" in tweet.lower() or "won" in tweet.lower() or "win" in tweet.lower() or "goes" in tweet.lower() or "won by" in tweet.lower()]
    nlp = spacy.load("en_core_web_sm")
    # Get all tweets
    # Populate Regex expressions and get tweets that follow Nominee wins Award  
    
    with open("movie_names.json", "r") as json_file:
        movie_names = json.load(json_file)
        movies_set = set(movie_names)

    person_first = [
        "has won award for AWARD",
        "has won the award for AWARD",
        "wins award for AWARD",
        "wins the award for AWARD",
        "wins AWARD",
        "wins the AWARD award",
    ]
    award_first = [
        "AWARD award goes to",
        "AWARD goes to",
        "AWARD won by"
    ]
    result = defaultdict(int)
    for tweet in tweets:
        for a in award['formatted']:
            # Process if award type is "Movie"
            if award['category'] == "Movie":
                for template in person_first:
                    template = template.replace("AWARD", a)
                    if template in tweet:
                        first_part = tweet.split(template)[0]
                        subphrases = get_all_subphrases(first_part)
                        for s in subphrases:
                            if s in movies_set:
                                result[s.lower()] += 1
                        doc = nlp(first_part)
                        entities = [ent.text.lower() for ent in doc.ents]
                        for ent in entities:
                            result[ent] += 1

                for template in award_first:
                    template = template.replace("AWARD", a)
                    if template in tweet:
                        second_part = tweet.split(template)[1]
                        subphrases = get_all_subphrases(second_part)
                        for s in subphrases:
                            if s in movies_set:
                                result[s.lower()] += 1
                        doc = nlp(first_part)
                        entities = [ent.text.lower() for ent in doc.ents]
                        for ent in entities:
                            result[ent] += 1


            # Process if award type is "Person"
            elif award['category'] == "Person":
                for template in person_first:
                    template = template.replace("AWARD", a)
                    if template in tweet:
                        first_part = tweet.split(template)[0]
                        doc = nlp(first_part)
                        entities = [ent.text.lower() for ent in doc.ents]
                        for ent in entities:
                            result[ent] += 1

                for template in award_first:
                    template = template.replace("AWARD", a)
                    if template in tweet:
                        second_part = tweet.split(template)[1]
                        doc = nlp(second_part)
                        entities = [ent.text.lower() for ent in doc.ents]
                        for ent in entities:
                            result[ent] += 1

    # Get the winner from the tweets through max frequency
    if not result:
        return ""
    return max(result, key=result.get)

def get_all_winners(tweets, awards):
    print("\nWinners:") 
    results = {}
    for award in awards:
        winner = get_winner(tweets, awards[award])
        results[award] = winner
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