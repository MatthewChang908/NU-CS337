from collections import defaultdict
import re
import Levenshtein
import openai

api_key = "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"
def identify_award_names(award_counts):
    client = openai.Client(api_key=api_key)
    award_counts_str = "\n".join([f"{award}: {count}" for award, count in award_counts.items()])

    # Prepare prompt with the award data
    prompt = (
        "Based on the following list of potential award names with their frequency counts, "
        "identify the names of the actual awards given at the Golden Globes:\n\n"
    )
    for award, count in award_counts.items():
        prompt += f"{award}: {count}\n"
    print("Sending prompt to OpenAI:")
    print(prompt)
    # Ask the model to identify likely award names

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "You analyze award names and consolidate similar ones."
            },
            {
                "role": "user", 
                "content": "Based on the following list of potential award names with counts, identify the likely awards given at the Golden Globes."
            },
            {
                "role": "user", 
                "content": award_counts_str
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "award_name_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "awards": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "award_name": {
                                        "type": "string",
                                        "description": "The name of a valid award'."
                                    }
                                },
                                "required": ["award_name"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["awards"],
                    "additionalProperties": False
                }
            }
        }
    )
    print("Received response from OpenAI:")
    print(response.choices[0].message.content)
    # return response['choices'][0]['message']['content']
    # response = openai.ChatCompletion.create(
    #     model="gpt-4-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are an assistant that identifies actual Golden Globes award names."},
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    # return response['choices'][0]['message']['content'].strip()

def get_awards(tweets):
    tweets = [tweet.lower() for tweet in tweets if "best" in tweet.lower() and not tweet.lower().startswith("rt")]
    patterns = [
        r"\bBest\s.*?(?=\sgoes\b)",
        r"\bwins\sbest\s.*?(?=(\s(for|to|at|and))|[.!?:\"#]|$)"
    ]
    awards = defaultdict(int)
    for tweet in tweets:
        for pattern in patterns:
            match = re.search(pattern, tweet, re.IGNORECASE)
            if match:
                award_name = match.group(0).strip()
                if "best tv series - drama" in award_name:
                    print(award_name)
                if ":" in award_name or "\"" in award_name:
                    break
                if award_name.startswith("wins"):
                    # remove it
                    award_name = award_name[5:]
                
                awards[award_name] += 1
                break
    awards = [[k, v] for k, v in awards.items() if v > 1]
    print(len(awards))
    awards = sorted(awards, key=lambda x: x[1], reverse=True)
    print(awards)
    # res = identify_award_names({award: count for award, count in awards})
    # print(res)
    # awards = awards[:20]
    # print("Top 20 Awards:")
    # for k, v in awards:
    #     print(k, v)
    # print(significant_clusters)