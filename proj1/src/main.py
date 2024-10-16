import json
# STEP 1: Get the winner of the award given the award and the nominees
def get_winner(tweets, award, nominees):
    # Get all tweets
    result = []
    # Populate Regex expressions and get tweets that follow Nominee wins Award
    # NOMINEE has won award for AWARD
    # NOMINEE has won the award for AWARD
    # NOMINEE wins award for AWARD
    # NOMINEE wins the award for AWARD
    # NOMINEE wins AWARD
    # AWARD award goes to NOMINEE
    # NOMINEE wins the AWARD award
    # AWARD goes to NOMINEE
    # AWARD won by NOMINEE
    regex_template = "AWARD goes to NOMINEE"

    # NOMINEE wins AWARD
    # LINCOLN wins BEST DRAMA in our hearts
    # 
    # 
    regex = []

    for nominee in nominees:
        regex.append(regex_template.replace("NOMINEE", nominee).replace("AWARD", award))
    print(regex)
    
    # Run the tweets thru the regex expressions
    for tweet in tweets[:10]:
        for reg in regex:
            print("reg", reg, "\ntweet", tweet)
            if reg in tweet:
                result.append(tweet)
        # if regex[0] in tweet:
        #     result.append(tweet)
    
    print(result)
    # Get the winner from the tweets thru max frequency
    return ""


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
    
    # for award in config['Awards'][0]:
    #     nominees = award['nominees']
    #     award_name = award['name']
    #     winner = get_winner(tweets, award_name, nominees)
    #     print("Winner of " + award_name + " is " + winner)
    award = config['Awards'][0]
    nominees = award['nominees']
    award_name = award['name']
    winner = get_winner(tweets, award_name, nominees)
    print("Winner of " + award_name + " is " + winner)
    
    return

if __name__ == "__main__":
    __main__()