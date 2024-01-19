from dotenv import load_dotenv
import os
import tweepy

load_dotenv()


BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
CONSUMER_KEY = os.getenv('TWITTER_API_KEY')
CONSUMER_SECRET=os.getenv('TWITTER_API_SECRET_KEY')
ACCESS_TOKEN=os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

api = tweepy.Client(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def tweet_thread(thread : list[str]): 
    """
    Tweet a thread of tweets
    """
    first_tweet_in_thread_response = api.create_tweet(text=thread[0])
    tweet_to_reply_to=first_tweet_in_thread_response.data['id']

    for remaining_tweet in thread[1:]:
        next_tweet_in_thread_response = api.create_tweet(text=remaining_tweet, in_reply_to_tweet_id=tweet_to_reply_to)
        tweet_to_reply_to = next_tweet_in_thread_response.data['id']
