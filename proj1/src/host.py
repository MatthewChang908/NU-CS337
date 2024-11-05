import spacy 
from collections import defaultdict
import json
import numpy as np

def getHost(tweets):
    tweets = preprocess(tweets)
    hosts = defaultdict(int)
    
    nlp = spacy.load("en_core_web_sm")
    celebs = getCelebs()
    for tweet in tweets:
        split_tweet = tweet.split()
        
        for i in range(len(split_tweet)):
            for j in range(i+2, len(split_tweet)):
                substring = " ".join(split_tweet[i:j])
                if substring in celebs:
                    hosts[substring] += 1
    
    consolidated_hosts = defaultdict(int)
    for name, count in hosts.items():
        found_match = False
        for existing_name in consolidated_hosts.keys():
            # Check if the name is a part of an existing name or vice versa
            if name in existing_name or existing_name in name:
                consolidated_hosts[existing_name] += count
                found_match = True
                break
        if not found_match:
            consolidated_hosts[name] = count

    # get the top 2: 
    hosts = dict(sorted(consolidated_hosts.items(), key=lambda x: x[1], reverse=True)[:5])
    hosts = getRealHosts(hosts)
    print("\nHosts:")
    for host in hosts:
        print(host)
    return hosts

def preprocess(tweets):
    tweets = [tweet for tweet in tweets if "host" in tweet.lower() and "next year" not in tweet.lower()]
    return tweets

def getCelebs():
    celebs = set()
    with open("recent_celebrity_names.json", "r") as json_file:
        celebs = json.load(json_file)
        celebs = set(celebs['recent_celebrity_names'])
    return celebs

def getRealHosts(hosts):
    
    # Convert counts to a list
    counts = np.array(list(hosts.values()))
    # Calculate mean and standard deviation
    mean_count = np.mean(counts)
    std_dev = np.std(counts)

    # Calculate Z-scores for each name
    z_scores = {name: (count - mean_count) / std_dev for name, count in hosts.items()}
    # Set a threshold for Z-score to identify significant outliers
    z_threshold = 0.5
    likely_hosts = [name for name, z in z_scores.items() if z > z_threshold]
    return likely_hosts