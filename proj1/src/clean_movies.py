import pandas as pd
import json
# Load the TSV file
df = pd.read_csv("title.basics.tsv", sep='\t', low_memory=False)

# Filter for movies (titleType == 'movie') and released after 2010
# Assuming 'startYear' is the column for release year and 'primaryTitle' for movie title
df['startYear'] = pd.to_numeric(df['startYear'], errors='coerce').fillna(0).astype(int)
movies = df[(df['titleType'] == 'movie') & (df['startYear'] > 2010)]

# Get the list of movie titles
movies = movies['primaryTitle'].tolist()

# remove duplicates with set
movies = list(set(movies))

with open("movie_names.json", "w") as json_file:
    json.dump(movies, json_file)