import pandas as pd
import json

# Load the IMDb name.basics.tsv file
df = pd.read_csv("name.basics.tsv", sep='\t', usecols=['primaryName', 'primaryProfession', 'birthYear', 'deathYear'], na_values='\\N')

# Define professions that typically belong to celebrities
celebrity_professions = {'actor', 'actress', 'director', 'producer', 'writer'}

# Filter rows where primaryProfession matches celebrity roles
df['primaryProfession'] = df['primaryProfession'].fillna('')
df['is_celebrity'] = df['primaryProfession'].apply(
    lambda x: any(profession in celebrity_professions for profession in str(x).split(','))
)

# Convert birthYear to numeric, coercing errors to NaN (e.g., non-numeric values)
df['birthYear'] = pd.to_numeric(df['birthYear'], errors='coerce')

# Get original count of celebrity names
original_celebrity_names = df[df['is_celebrity']]['primaryName'].tolist()
print("Original number of celebrity names:", len(original_celebrity_names))

# Filter for celebrities still active in the past 20 years, with a valid integer birth year, and names with at least 3 characters
df['deathYear'] = df['deathYear'].fillna(9999).astype(int)  # Replace NaN with 9999 for still-living celebrities
recent_celebrities = df[(df['is_celebrity']) & (df['deathYear'] > 2004) & (df['birthYear'].notna()) & (df['primaryName'].str.len() >= 3)]['primaryName'].tolist()

# Get the new filtered count of recent celebrity names
print("Filtered number of recent celebrity names (last 20 years, with valid birth year, and names with 3+ characters):", len(recent_celebrities))

# Output the recent celebrity names to a JSON file
output_data = {"recent_celebrity_names": recent_celebrities}
with open("recent_celebrity_names.json", "w") as f:
    json.dump(output_data, f)

print("Recent celebrity names extracted to 'recent_celebrity_names.json'")
