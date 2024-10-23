import json
from collections import defaultdict
# STEP 1: Get the winner of the award given the award and the nominees
def get_winner(tweets, award, nominees):
    # Get all tweets
    # Populate Regex expressions and get tweets that follow Nominee wins Award
    regex_templates = [
        "NOMINEE has won award for AWARD",
        "NOMINEE has won the award for AWARD",
        "NOMINEE wins award for AWARD",
        "NOMINEE wins the award for AWARD",
        "NOMINEE wins AWARD",
        "AWARD award goes to NOMINEE",
        "NOMINEE wins the AWARD award",
        "AWARD goes to NOMINEE",
        "AWARD won by NOMINEE"
    ] 
    regex = defaultdict(list)

    for nominee in nominees:
        for template in regex_templates:
            reg = template.replace("NOMINEE", nominee).replace("AWARD", award)
            regex[nominee].append(reg)
    # print(regex)
    # return
    result = defaultdict(int) # mapping nominee to frequency

    # Run the tweets thru the regex expressions
    for tweet in tweets:
        found = False
        for nominee in regex:
            if found: 
                break # We can return if we already found a match
            templates = regex[nominee]
            for reg in templates:
                if reg in tweet:
                    result[nominee] += 1
                    found = True
                    break
            if not found:
                if nominee in tweet and award in tweet:
                    result[nominee] += 1
                    found = True
                    break
    
    # Get the winner from the tweets thru max frequency
    if not result:
        return ""
    return max(result, key=result.get)

def test(tweets):
    for tweet in tweets:
        if "Best Actor in a Motion Picture - Comedy or Musical" in tweet:
            print(tweet)
    
def __main__():
    
    # for each award in the award config:
    # call get_winner(award, nominees)
    
    config = None
    with open ('config.json', 'r') as file:
        config = json.load(file)

    # List of all the tweets
    tweets = []
    
    # Open the data
    with open('gg2013.json', 'r') as file:
        data = json.load(file)
        for tweet in data:
            text = tweet['text']
            tweets.append(text)
    print(len(tweets))
    for award in config['Awards']:
        nominees = award['nominees']
        award_name = award['name']
        winner = get_winner(tweets, award_name, nominees)
        if not winner:
            print("No winner found for " + award_name)
            continue
        print("Winner of " + award_name + " is " + winner)
    # test(tweets)
    return

if __name__ == "__main__":
    __main__()