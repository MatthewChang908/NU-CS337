import re
# def get_nominees(tweets, awards):
#     print("Getting Nominees")
#     nominee_prediction_phrases = [
#         "should have been",
#         "should've been",
#     ]
    
#     patterns = [
#         r"([A-Z][a-z]+(?: [A-Z][a-z]+)*) nominated for (.+)",
#         r"(.+) nominee ([A-Z][a-z]+(?: [A-Z][a-z]+)*)",
#         r"(.+) nomination goes to ([A-Z][a-z]+(?: [A-Z][a-z]+)*)",
#         r"([A-Z][a-z]+(?: [A-Z][a-z]+)*) is a nominee for (.+)",
#         r"([A-Z][a-z]+(?: [A-Z][a-z]+)*) receives (.+) nomination",
#         r"(.+) nod to ([A-Z][a-z]+(?: [A-Z][a-z]+)*)"
#     ]

    
#     # filter tweets by prodiction phrases
#     print("old", len(tweets))  
#     for phrase in nominee_prediction_phrases:
#         tweets = [tweet for tweet in tweets if phrase not in tweet]    
#     tweets = [tweet for tweet in tweets if "nominated" in tweet or "nominee" in tweet]
#     print("new", len(tweets))
    
#     nominees = {}
#     for award_key in awards:
#         award_name = awards[award_key]
#         nominees[award_name] = []
        
#         for tweet in tweets:
#             # Check each pattern for a match
#             if ("nominated" in tweet or "nominee" in tweet) and "django unchained" in tweet.lower():
#                 print(tweet)
#             # for pattern in patterns:
#             #     match = re.search(pattern, tweet, re.IGNORECASE)
#             #     if match:
#             #         if "nominated for" in pattern or "is a nominee for" in pattern:
#             #             nominee, award_in_tweet = match.groups()
#             #         else:
#             #             award_in_tweet, nominee = match.groups()
                    
#             #         # Check if the award matches the intended award name
#             #         if award_name.lower() in award_in_tweet.lower():
#             #             nominees[award_name].append(nominee)
        
#         # Remove duplicates by converting to set and back to list
#         # nominees[award_name] = list(set(nominees[award_name]))
#         # print(f"Found {len(nominees[award_name])} nominees for {award_name}")

#     return nominees

import re
import spacy
from collections import defaultdict
def get_nominees(tweets, awards):
    nominee_prediction_phrases = [
        "should have been",
        "should've been",
    ]
    for phrase in nominee_prediction_phrases:
        tweets = [tweet for tweet in tweets if phrase not in tweet.lower()]    
    tweets = [tweet for tweet in tweets if "nominated" in tweet.lower() or "nominee" in tweet.lower() or "nomination" in tweet.lower()]

    nlp = spacy.load("en_core_web_sm")
    
    # # Compile regex patterns for each award using alternative names
    # award_patterns = {
    #     award: re.compile(r'\b(' + '|'.join(map(re.escape, alts)) + r')\b', re.IGNORECASE)
    #     for award, alts in awards.items()
    # }
    
    # # Initialize dictionary to store nominees per award
    # nominees = {award: [] for award in awards}
    
    # # Process each tweet
    # for tweet in tweets:
        
    #     doc = nlp(tweet)
        
    #     # Extract both person names and film titles from the tweet
    #     entities = [ent.text for ent in doc.ents if ent.label_ in {"PERSON", "WORK_OF_ART"}]
    #     temp = tweet.lower()
    #     if ("nomination" in temp or "nominated" in temp or "nominee" in temp) and "foreign language film" in temp:
    #         print("found", tweet)
    #         print(entities)
    #     # Check for mentions of each award in the tweet
    #     for award, pattern in award_patterns.items():
    #         if pattern.search(tweet):  # If an award is mentioned
    #             # Add all detected people and films as potential nominees for this award
    #             nominees[award].extend(entities)
    
    # # Remove duplicates from nominee lists for each award
    # nominees = {award: list(set(names)) for award, names in nominees.items()}
    # for award, names in nominees.items():
    #     print(f"Found {len(names)} nominees for {award}")
    # # return nominees
    
    nominees = defaultdict(set)
        
    for i, tweet in enumerate(tweets):
        doc = nlp(tweet)
        tweets[i] = [ent.text for ent in doc.ents if ent.label_ in {"PERSON", "WORK_OF_ART"}]

    
    return nominees