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

def get_all_winners(tweets, awards):
    results = {}
    for award in awards:
        nominees = award['nominees']
        award_name = award['name']
        winner = get_winner(tweets, award_name, nominees)
        results[award_name] = winner
    nominees = {}
    for award in awards:
        nominees[award['name']] = award['nominees']
    return [results, nominees]

def print_all_winners(results, nominees):
    for award in results:
        print("Award:", award)
        print("Presenters WIP")
        print("Nominees:", nominees[award])
        print("Winner:", results[award])
        print()

# Part 2: Given the award name, return the nominees and the presenter
def get_nominees(tweets, award):
    return 

def get_presenters(tweets, award):
    return

# Part 3: Extract the award names from the tweets
def get_awards(tweets):
    return
    
def __main__():
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

    # PART 3
    awards_names = get_awards(tweets)

    # PART 2
    awards = {}
    for award in awards_names:
        obj = {}
        nominees = get_nominees(tweets, award)
        presenters = get_presenters(tweets, award)
        obj['name'] = award
        obj['nominees'] = nominees
        obj['presenters'] = presenters
        awards[award] = obj

    # PART 1
    awards = config['Awards'] # TODO: Replace with results from Part 2
    results, nominees = get_all_winners(tweets, awards)
    print_all_winners(results, nominees)

    return

if __name__ == "__main__":
    __main__()