import json

def output_results(awards, host, presenters, nominees, winners):

    """Output the results of the Golden Globes analysis to a file."""
    with open("results.json", "w") as file:
        res = {}
        res['Hosts'] = host
        for award in awards:
            award_name = award
            res[award_name] = {}
            res[award_name]["nominees"] = nominees[award_name]
            res[award_name]["winner"] = winners[award_name]
            res[award_name]["presenters"] = presenters[award_name]