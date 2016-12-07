import json
import pandas as pd
import matplotlib.pyplot as plt

from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
# https://github.com/tweepy/tweepy/blob/cd46550b3ef068857f5de9c37bbdd0a72acb7462/examples/streaming.py
# http://tweepy.readthedocs.io/en/v3.5.0/getting_started.html

# Authentication set up
consumer_key = "UPoyqr6Saeixk8P3dCrE0SLFy"
consumer_secret = "QXktJB1v0kaL44W5Xlfnl9jzTl9vnKCa8MHXinO9Iyrmpe8xpr"
access_token_key = "153210170-HOypecDRgWbDFM9RfcM3hXSw374j5WzBgl43emDI"
access_token_secret = "t9KPrP71s3dWDEviO2Di1jUjawBTZ8o4UT012hIJOUUhg"


# pulled from the tweepy example code
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['harambe'])

# look up pdb parser and blast searches
