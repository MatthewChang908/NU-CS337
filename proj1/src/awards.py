from collections import defaultdict
import re
import spacy
import json
from imdb import IMDb
def get_awards(tweets):
    celebrity_names_set = set()
    with open("recent_celebrity_names.json", "r") as f:
        data = json.load(f)
        celebrity_names_set = set(data["recent_celebrity_names"])
    tweets = [tweet for tweet in tweets if "best" in tweet.lower()]
    patterns = [
        r"\bBest\s.*?(?=\s(?:goes|is|wins|win|of|award|awarded|part|for)\b|:)",
        r"\bwins\sbest\s.*?(?=(\s(for|to|at|and|win|part|of))|[.!?:\"#]|$)",
        r"\bnominated\sfor\sbest\s.*?(?=(\s(for|to|at|and|win|part|of))|[.!?:\"#]|$)"
    ]
    awards = defaultdict(int)
    for tweet in tweets:
        # if "Maggie Smith" in tweet:
        #     print("tweet", tweet)
        for pattern in patterns:
            match = re.search(pattern, tweet, re.IGNORECASE)
            if match:
                award_name = match.group(0).strip()
                # if "best actor in a miniseries or tv movie" in award_name:
                #     print(tweet)
                if award_name.startswith("wins"):
                    # remove it
                    award_name = award_name[5:]
                elif award_name.startswith("nominated for best"):
                    award_name = award_name[18:]
                # if "Best Supporting Actress in a TV Movie Series or Miniseries goes to Maggie Smith for Downton Abbey" in tweet:
                #     print("award name", award_name)
                awards[award_name.lower()] += 1
                break
    awards = [[k, v] for k, v in awards.items() if v > 1]
    print(len(awards))
    awards = sorted(awards, key=lambda x: x[1], reverse=True)
    # remove all award names with a person entity with spacy
    # nlp = spacy.load("en_core_web_sm")
    # for i, award in enumerate(awards):

    #     doc = nlp(award[0])
    #     if "maggie smith" in award[0].lower():
    #         print("this is a person", award)  
    #         print(doc.ents)  
    #     for ent in doc.ents:
    #         if "maggie smith" in award[0].lower():
    #             print("ent", ent)
    #         if ent.label_ == "PERSON":
    #             print("removed", award, "for", ent.text, "being a" , ent.label_)
    #             print("ent", doc.ents)   
    #             awards.pop(i)
    award_names = [award[0] for award in awards]
    print("awards:", award_names)
    for i, award in enumerate(award_names):
        words = award.split()
        words = [word.capitalize() for word in words]
        for i in range(len(words)):
            found = False
            for j in range(i+1, i+3):
                if j > len(words):
                    break
                name = " ".join(words[i:j])
                if name in celebrity_names_set:
                    awards.pop(i)
                    print("name found:", name, "deleted", award)
                    found = True
                    break
            if found: break

    awards = awards[:30]
    print("Top 40 Awards:")
    for k, v in awards:
        print(k, v)
    # print(significant_clusters)
    return []