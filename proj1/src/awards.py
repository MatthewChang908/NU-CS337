from collections import defaultdict
import re
import Levenshtein

def get_awards(tweets):
    tweets = [tweet.lower() for tweet in tweets if "best" in tweet.lower() and not tweet.lower().startswith("rt")]
    patterns = [
        r"\bBest\s.*?(?=\sgoes\b)",
        r"\bwins\sbest\s.*?(?=(\s(for|to|at|and))|[.!?:\"#]|$)"
    ]
    awards = defaultdict(int)
    for tweet in tweets:
        for pattern in patterns:
            match = re.search(pattern, tweet, re.IGNORECASE)
            if match:
                if "best original song while taylor swift gives her stank eye" in tweet:
                    print(tweet)
                award_name = match.group(0).strip()

                if ":" in award_name or "\"" in award_name:
                    break
                if award_name.startswith("wins"):
                    # remove it
                    award_name = award_name[5:]
                
                awards[award_name] += 1
                break
    awards = [[k, v] for k, v in awards.items() if v > 1]
    awards = sorted(awards, key=lambda x: x[1], reverse=True)

    print("Awards:")
    for k, v in awards:
        print(k, v)
    awards = awards[:20]
    print()
    print("Top 20 Awards:")
    for k, v in awards:
        print(k, v)
    # print(significant_clusters)