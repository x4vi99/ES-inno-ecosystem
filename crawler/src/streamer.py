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

class MyListener:
    def __init__(self,output_file=None, user_file=None):
        self.num_tweets = 0
        if output_file == None:
            if not OUTPUT_JSON.parent.is_dir():
                OUTPUT_JSON.parent.mkdir(parents=False)
        self.output_file = output_file if output_file is not None else str(OUTPUT_JSON)
        self.tweet_ids = set()

    def save_tweet(self, tweet):
            with open(self.output_file, 'a') as f:
                jdata = json.loads(tweet)
                filter_data = self.get_tweet(jdata)
                if filter_data['ID'] in self.tweet_ids:
                    return
                self.tweet_ids.add(filter_data['ID'])
                self.num_tweets += 1
                print('%d' % (self.num_tweets), end='\r')
                f.write(json.dumps(filter_data)+'\n')
    

    def get_tweet(self, jdata):
        filter_data = {}
        if 'extended_tweet' in jdata:
            filter_data['Tweet_text'] = jdata['extended_tweet']['full_text']
            hashtags = jdata['extended_tweet']['entities']['hashtags']
        else:
            filter_data['Tweet_text'] = jdata['text']
            hashtags = jdata['entities']['hashtags']
        filter_data['Hashtags'] = [ht['text'] for ht in hashtags]
        filter_data['UserId'] = jdata['user']['id']
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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-output', default=None, help='Output json of tweets')
    return parser.parse_args()

OUTPUT_JSON = Path('/Users/xaviamat/Desktop/TFG/Innovation_Tool/data/tweets.json')

if __name__ == '__main__':
    nltk.download('stopwords')

    consumer_key = 'UPtQiALNjB7rWxcIY8CB9IXmb'
    consumer_secret = 'lsU5NELQCDfE7eGs0f2fraobK34LoF7X0OSreaOAdLR7n7uwv8'
    access_token = '3796381515-0VrTXAZlasSMTWGlYBDa5djTsKjS6hl1eqrHmIt'
    access_secret = 'juiVqZVBAoqQyFjXfsWWt8LkBM0ikqpNsWmhHrh8ZyHA3'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    args = parse_args()
    start_time = time.time()
    listener = MyListener(output_file=args.output)

    #twitter_stream = Stream(auth, listener)
    api = tweepy.API(auth)
    users = ["marabales","cris_aranda_","XavierFerras","oalcoba","XavierMarcet","PereCondom","ealmirall","rodriguezhernan","carmeartigas","Elena_Gil_Liza","HoracioMorellG","oscarpierremi","davidcierco","MiguelVicente_","carlosblanco","aiglesiasfraga","MartaAntunezBCN","NadiaCalvino","MLMelo"]
     #initialize a list to hold all the tweepy Tweets
    alltweets = []  

    for user in users:
        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = user,count=200)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print(f"getting tweets before {oldest}")
            
            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name = user,count=200,max_id=oldest)
            
            #save most recent tweets
            alltweets.extend(new_tweets)
            
            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            
            print(f"...{len(alltweets)} tweets downloaded so far")
        for tweet in alltweets:
            listener.save_tweet(json.dumps(tweet._json))

    total_time = time.time() - start_time
    print('_______ End _______')
    print('Tweets: ', listener.num_tweets)
    print('Total time: ', total_time)