from collections import defaultdict
import re
import json

def get_awards(tweets):
    celebrity_names_set = set()
    with open("recent_celebrity_names.json", "r") as f:
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
                elif award_name.startswith("nominated for best"):
                    award_name = award_name[18:]
                awards[award_name.lower()] += 1
                break
    awards = [[k, v] for k, v in awards.items() if v > 1]
    print(len(awards))
    awards = sorted(awards, key=lambda x: x[1], reverse=True)
    
    award_names = [award[0] for award in awards]
    
    # Remove award names with celebrity names
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
                    found = True
                    break
            if found: break

    awards = awards[:30]
    for k, v in awards:
        print(k, v)
    return [k for k, v in awards]