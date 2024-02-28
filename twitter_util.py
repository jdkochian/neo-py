from dotenv import load_dotenv
import os
import re
import tweepy
import schedule

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

    for remaining_tweet, img_filepath in thread[1:]:
        diagram_media_id = upload_media(img_filepath)
        next_tweet_in_thread_response = api.create_tweet(text=remaining_tweet, in_reply_to_tweet_id=tweet_to_reply_to, media_ids=[diagram_media_id])
        os.remove(img_filepath)
        tweet_to_reply_to = next_tweet_in_thread_response.data['id']


def tweet_at_specific_time(tweet : str, img_src : str): 

    api.create_tweet(text=tweet)
    diagram_media_id = upload_media(img_src)
    api.create_tweet(text=tweet, media_ids=[diagram_media_id])
    os.remove(img_src)

    return schedule.CancelJob


# TODO: One tweepy v2 can handle media uploading, update code
def upload_media(filepath): 
    """
    Upload the image to twitter using v1.1 api (not supported in tweepy api v2 for some reason)
    """
    tweepy_auth = tweepy.OAuth1UserHandler(
        "{}".format(CONSUMER_KEY),
        "{}".format(CONSUMER_SECRET),
        "{}".format(ACCESS_TOKEN),
        "{}".format(ACCESS_TOKEN_SECRET),
    )
    tweepy_api = tweepy.API(tweepy_auth)

    post = tweepy_api.simple_upload(filepath)
    text = str(post)
    media_id = re.search("media_id=(.+?),", text).group(1)
    return media_id
