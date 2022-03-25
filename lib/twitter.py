import os

import tweepy, logging
from dotenv import dotenv_values

config = dotenv_values()

consumer_key = config.get("tw_consumer_key")
consumer_secret = config.get("tw_consumer_secret")

access_token = config.get("tw_access_token")
access_token_secret = config.get("tw_access_token_secret")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def test():
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)


def p__ost_tweet(str):
    original_tweet = api.update_status(status=str)


def post_thread(peaces, image_filename=None):
    """
    Post a thread in tweeter. Optionally attach the image to the FIRST tweet
    :param peaces:
    :param image_filename:
    :return:
    """
    first = True
    media_list = []
    logging.info("update_status()")
    for p in peaces:
        if first:
            if image_filename:
                response = api.media_upload(image_filename)
                media_list.append(response.media_id_string)
                # Sakita ! no me subas más de 1 imagen porque quemás todo !
            last_tweet = api.update_status(status=p, media_ids=media_list)
            first = False
        else:
            last_tweet = api.update_status(status=p, in_reply_to_status_id=last_tweet.id,
                                           auto_populate_reply_metadata=True)
