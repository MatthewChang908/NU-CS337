from collections import defaultdict

AWARDS_LIST = [
    "Best Motion Picture - Drama",
    "Best Motion Picture - Musical or Comedy",
    "Best Performance by an Actor in a Motion Picture - Drama",
    "Best Performance by an Actress in a Motion Picture - Drama",
    "Best Performance by an Actor in a Motion Picture - Musical or Comedy",
    "Best Performance by an Actress in a Motion Picture - Musical or Comedy",
    "Best Performance by an Actor in a Supporting Role in any Motion Picture",
    "Best Performance by an Actress in a Supporting Role in any Motion Picture",
    "Best Director - Motion Picture",
    "Best Screenplay - Motion Picture",
    "Best Original Score - Motion Picture",
    "Best Original Song - Motion Picture",
    "Best Animated Feature Film",
    "Best Foreign Language Film",
    "Best Television Series - Drama",
    "Best Television Series - Musical or Comedy",
    "Best Performance by an Actor in a Television Series - Drama",
    "Best Performance by an Actress in a Television Series - Drama",
    "Best Performance by an Actor in a Television Series - Musical or Comedy",
    "Best Performance by an Actress in a Television Series - Musical or Comedy",
    "Best Performance by an Actor in a Supporting Role in a Series, Miniseries or Motion Picture Made for Television",
    "Best Performance by an Actress in a Supporting Role in a Series, Miniseries or Motion Picture Made for Television",
    "Best Mini-Series or Motion Picture Made for Television",
    "Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television",
    "Best Performance by an Actress in a Mini-Series or Motion Picture Made for Television",
]


def process():
    awards = AWARDS_LIST
    res = defaultdict(dict)
    
    replacements = {
        "performance by an": "",
        "actor in a supporting role" : "supporting actor",
        "actress in a supporting role" : "supporting actress",
        "made for": "",
        " - " : " ",
        "any": "a",
        "motion picture": "picture",
        "picture": "",
        "television": "tv",
    }

    for award in awards:
        temp = award.lower()
        formatted_versions = set([temp])  # Start with the original lowercase version
        
        # Apply replacements incrementally to generate alternative formats
        for k, v in replacements.items():
            temp = temp.replace(k, v)
            temp = " ".join(temp.split())  # Remove any extra whitespace
            formatted_versions.add(temp)

        # Classify the award as "Movie" or "Person"
        if any(keyword in award.lower() for keyword in ["actor", "actress", "director"]):
            category = "Person"
        else:
            category = "Movie"
        
        res[award]["formatted"] = list(formatted_versions)
        res[award]["category"] = category
        print(award, ":", res[award])
    return res
