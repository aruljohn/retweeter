import tweepy
import os
from dotenv import load_dotenv
import time

# Get tokens 
load_dotenv()

# Get the keys and tokens from .env
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
TOKEN_SECRET = os.getenv('TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# Create a session
client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, ACCESS_TOKEN, TOKEN_SECRET)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# StreamingClient class
class TelgoduListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        client.retweet(tweet.id)
        client.like(tweet.id)
        client.follow_user(tweet.author_id)
        print(tweet.id, tweet.author_id)
        time.sleep(30)

    def on_exception(self, data):
        print('on_exception', data)
        exit()

# Stream and retweet
stream = TelgoduListener(bearer_token=BEARER_TOKEN)
rule = tweepy.StreamRule("(#python OR #programming OR #cybersecurity OR #web3)")
stream.add_rules(rule)
stream.filter(tweet_fields=["author_id"])
