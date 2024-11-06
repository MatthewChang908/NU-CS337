from collections import defaultdict
import re
import json
import spacy
def get_awards(tweets):
    
    celebrity_names_set = set()
    with open("data/celebs.json", "r") as f:
        data = json.load(f)
        celebrity_names_set = set(data["recent_celebrity_names"])
    tweets = [tweet for tweet in tweets if "best" in tweet.lower()]
    
    patterns = [
        r"\bBest\s.*?(?=\s(?:goes|is|wins|win|of|award|awarded|part|for)\b|:)",
        r"\bwins\sbest\s.*?(?=(\s(for|to|at|and|win|part|of))|[.!?:\"#]|$)",
    ]
    awards = defaultdict(int)
    for tweet in tweets:
        for pattern in patterns:
            match = re.search(pattern, tweet, re.IGNORECASE)
            if match:
                award_name = match.group(0).strip()
                if award_name.startswith("wins"):
                    # remove it
                    award_name = award_name[5:]

                award_name = remove_celebs(award_name, celebrity_names_set)
                award_name = award_name.lower()
                award_name = award_name.replace("television", "tv")
                awards[award_name] += 1
                break
    awards = [[k, v] for k, v in awards.items() if v > 1]
    awards = sorted(awards, key=lambda x: x[1], reverse=True)
    awards = post_process_awards(awards)
    awards = awards[:30]
    for k, v in awards:
        print(k.title())

def remove_celebs(award, celeb_names):
    award = award.split()
    for i in range(len(award)):
        for j in range(i+1, len(award)+1):
            name = " ".join(award[i:j])
            if name in celeb_names:
                # remove the name
                award = award[:i]
                return " ".join(award)
    return " ".join(award)

def post_process_awards(awards):
    # remove everything after the stop words 
    stop_words = ["for", "to", "at", "and", "win", "part", "of", "goes", "is", "award", "awarded"]
    stop_puncts = [".", "!", "?", ":", "\"", "#"]

    temp_awards = []
    for i in range(len(awards)):
        award = awards[i][0]
        award = award.split()

        for word in stop_words:
            if word in award:
                award = award[:award.index(word)]
        if len(award) == 1:
            continue
        temp_awards.append([" ".join(award), awards[i][1]])

    awards = temp_awards
    for i in range(len(awards)):
        award = awards[i][0]
        for punct in stop_puncts:
            if punct in award:
                award = award.split(punct)[0]
        awards[i][0] = award
        
    # use spacy to catch any persons, and remove the person and everything after
    nlp = spacy.load("en_core_web_sm")
    for i in range(len(awards)):
        award = awards[i][0]
        doc = nlp(award)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                award = award.split(ent.text)[0]
                break
        awards[i][0] = award
        
    # recombine all keys since we might have duplicates
    awards_set = defaultdict(int)
    for award in awards:
        award_name = award[0].strip()
        award_value = award[1]
        awards_set[award_name] += award_value

    # handle if we have 'a or b' vs 'b or a' in the award name
    normalized_awards_set = defaultdict(int)
    for award, value in awards_set.items():
        award_string = award.split()
        
        if "or" in award_string:
            # Find the indices around "or"
            or_index = award_string.index("or")
            if or_index > 0 and or_index < len(award_string) - 1:
                # Sort the words around "or" to ensure consistency
                before_or = award_string[:or_index - 1]
                options = sorted([award_string[or_index - 1], award_string[or_index + 1]], reverse=True)
                after_or = award_string[or_index + 2:]
                normalized_award = " ".join(before_or + [options[0], "or", options[1]] + after_or)
            else:
                normalized_award = award  # If "or" is at an invalid position, use original
            
            normalized_awards_set[normalized_award] += value
        else:
            normalized_awards_set[award] += value
    
    return [[k, v] for k, v in normalized_awards_set.items()]