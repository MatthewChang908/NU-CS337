import pandas as pd
import json
import datetime

# Load TV show data from tvs.json
with open("tvs.json", "r") as input_file:
    tv_shows = json.load(input_file)

def get_names(shows):
    show_names = []
    threshold_date = datetime.datetime(2010, 1, 1)
    
    for show in shows:
        # Ensure last_air_date and popularity are valid
        last_air_date_str = show.get("last_air_date")
        popularity = show.get("popularity", 0)
        
        if last_air_date_str is None:
            continue  # Skip this entry if last_air_date is missing

        # Convert last_air_date to datetime
        last_air_date = datetime.datetime.strptime(last_air_date_str, "%Y-%m-%d")
        
        # Check if the last air date is past 2010 and popularity is greater than 10
        if last_air_date > threshold_date and popularity > 10:
            show_names.append(show["name"])
    
    return show_names

# Get the list of show names with last air date past 2010 and popularity > 10
names = get_names(tv_shows)

# Write the list of names to a JSON file
with open("tv_shows.json", "w") as output_file:
    json.dump(names, output_file, indent=4)