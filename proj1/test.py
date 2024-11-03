import json
# open recent_celebrity_names.json
with open('recent_celebrity_names.json', 'r') as f:
    data = json.load(f)
    recent_celebrities = set(data['recent_celebrity_names'])
    
    print(("Original") in recent_celebrities)