import googlemaps
from datetime import datetime
import json
import pandas as pd

gmaps=googlemaps.Client(key='AIzaSyBKOzmQIiZ-c1DqAYiNiyjsoh72I68W7lQ')

dictionaries = []
#USE './tweets/merged_es.json' for spanish
with open ('data/tweets_es.json','r') as file:
    for line in file: 
        tweet=json.loads(line)
        dictionaries.append(tweet)
tweets = pd.DataFrame(dictionaries)

tweets["Location"] = ""

for location in tweets.UserLocation:
    try:
        location=gmaps.geocode(location)
        print(location)
    except:
        pass

tweets.to_json (r'test.json')
