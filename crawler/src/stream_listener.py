import re
import simplejson as json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import tweepy
from tweet import Tweet
from utils import get_terms
import argparse
from pathlib import Path
import nltk
import time
import googlemaps
from geopy.geocoders import Nominatim
from datetime import datetime
import pandas as pd

class MyListener(StreamListener):
    def __init__(self, max_tweets, output_file=None):
        super(StreamListener, self).__init__()
        self.num_tweets = 0
        self.max_tweets = max_tweets
        if output_file == None:
            if not OUTPUT_JSON.parent.is_dir():
                OUTPUT_JSON.parent.mkdir(parents=False)
        self.output_file = output_file if output_file is not None else str(OUTPUT_JSON)
        self.tweet_ids = set()

    #Writes the stream data on the output file
    def on_data(self, data):
        try:
            with open(self.output_file, 'a') as f:
                jdata = json.loads(data)
                if 'retweeted_status' in jdata:
                    filter_data = self.get_tweet(jdata)
                    filter_data_original = self.get_tweet(jdata['retweeted_status'])
                    if filter_data == False or filter_data_original == False :
                        return
                    if filter_data['ID'] in self.tweet_ids:
                        return
                    self.tweet_ids.add(filter_data['ID'])
                    self.tweet_ids.add(filter_data_original['ID'])
                    self.num_tweets += 2
                    print('%d / %d' % (self.num_tweets, self.max_tweets), end='\r')
                    f.write(json.dumps(filter_data)+'\n')
                    f.write(json.dumps(filter_data_original)+'\n')
                else:
                    filter_data = self.get_tweet(jdata)
                    if filter_data == False:
                        return
                    if filter_data['ID'] in self.tweet_ids:
                        return
                    self.tweet_ids.add(filter_data['ID'])
                    self.num_tweets += 1
                    print('%d / %d' % (self.num_tweets, self.max_tweets), end='\r')
                    f.write(json.dumps(filter_data)+'\n')

                # Setting a limit in the number of tweets collected
                if self.num_tweets < self.max_tweets:
                    return True
                else:
                    return False

        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    #Formats tweet data to a python dictionary
    def get_tweet(self, jdata):

        filter_data = {}

        if 'retweeted_status' in jdata:
            filter_data['IsRetweet']=1
            filter_data['RT_UserId']=jdata['retweeted_status']['user']['id_str']
            filter_data['RT_UserName']=jdata['retweeted_status']['user']['screen_name']
        else:
            filter_data['IsRetweet']=0
        if 'extended_tweet' in jdata:
            filter_data['Tweet_text'] = jdata['extended_tweet']['full_text']
            if any(substring in filter_data['Tweet_text'] for substring in KEYWORDS)==False:
                return False
            hashtags = jdata['extended_tweet']['entities']['hashtags']
            filter_data['Mentions']=jdata['extended_tweet']['entities']['user_mentions']
        else:
            filter_data['Tweet_text'] = jdata['text']
            if any(substring in filter_data['Tweet_text'] for substring in KEYWORDS)==False:
                return False
            hashtags = jdata['entities']['hashtags']
            filter_data['Mentions']=jdata['entities']['user_mentions']
        if 'coordinates' in jdata and jdata['coordinates'] is not None:
            filter_data["Coordinates"] = jdata['coordinates']['coordinates']
        p=jdata['place']
        if p is not None and p=="ES":
            filter_data["Country"] = jdata['place']['country_code']
            filter_data["Place"] = jdata['place']['full_name']
    
        filter_data['Hashtags'] = [ht['text'] for ht in hashtags]
        filter_data['UserId'] = jdata['user']['id']
        filter_data['UserName'] = jdata['user']['screen_name']
        filter_data['UserLocation']=jdata['user']['location']
        try:
            #filter_data['MapsLocation']=gmaps.geocode(filter_data['UserLocation'])
            location = geolocator.geocode(filter_data['UserLocation'])
            filter_data['MapsLocation']=location.address
            filter_data['lat']=location.latitude
            filter_data['long']=location.longitude
        except:
            return False
        try:
            #lent=len(filter_data["MapsLocation"][0]['address_components'])
            #country=filter_data["MapsLocation"][0]['address_components'][lent-1]['short_name']
            t = 'España'
            if t not in filter_data['MapsLocation']:
                return False
        except:
            return False
        filter_data['ID'] = jdata['id']
        filter_data['Date'] = jdata['created_at']
        filter_data['Likes'] = jdata['favorite_count']
        filter_data['URL'] = f"https://twitter.com/{jdata['user']['screen_name']}/status/{jdata['id']}"
        filter_data['Number_Retweets'] = jdata['retweet_count']
        filter_data['terms'] = get_terms(filter_data['Tweet_text'])

        return filter_data

    def on_error(self, status):
        print('Error :', status.place)
        return False

#KEYWORDS used for the search
KEYWORDS = ["innovación", "tecnología", "startup", "digitalización","transformación digital", "emprend", "digital", "digit", "innov", "tech", "research", "open innovation","R&D","I+D"]
#idea, ecosistema, "iniciativa", "disrup", "industria": Too broad

#Argument parser
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', type=int, default=5000, help='Number of tweets')
    parser.add_argument('-output', default=None, help='Output json of tweets')
    return parser.parse_args()
#Default output path
OUTPUT_JSON = Path('/Users/xaviamat/Desktop/TFG/Innovation_Tool/data/tweets_es.json')

if __name__ == '__main__':
    nltk.download('stopwords')
    #Add your Twitter API keys
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_secret = ''

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    args = parse_args()
    start_time = time.time()
    listener = MyListener(args.N, output_file=args.output)
    twitter_stream = Stream(auth, listener)

    geolocator = Nominatim(user_agent="InnovationTool")
    #gmaps=googlemaps.Client(key='')

    #Spain geography bounding box
    bounding_box=[-18.3936845, 27.4335426, 4.5918885, 43.9933088]

    while(listener.num_tweets < args.N):
        try:
            twitter_stream.filter(track=KEYWORDS, locations=bounding_box, languages=['es']) # Add your keywords and other filters
        except:
            print('Exception at', listener.num_tweets)
            pass
            # str = input('Continue? ')
            # if str == 'n': #TODO make better
            #     break
            # pass
    total_time = time.time() - start_time
    print('_______ End _______')
    print('Tweets: ', listener.num_tweets)
    print('Total time: ', total_time)