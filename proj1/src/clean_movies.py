import pandas as pd
import json
# Load the TSV file
df = pd.read_csv("title.basics.tsv", sep='\t', low_memory=False)
df['startYear'] = pd.to_numeric(df['startYear'], errors='coerce').fillna(0).astype(int)
df = df.dropna(subset=['primaryTitle'])
movies = df[(df['titleType'] == 'movie') & (df['startYear'] > 2012)]
movies = list(set(movies['primaryTitle'].tolist()))
movies = [movie for movie in movies if len(movie) > 1]
with open("movie_names.json", "w") as json_file:
    json.dump(movies, json_file)