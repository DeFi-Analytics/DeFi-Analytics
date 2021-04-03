import os
import tweepy as tw
import pandas as pd
from datetime import datetime

scriptPath = __file__
path = scriptPath[:-36] + '/data/'

auth = tw.OAuthHandler('ffPBjkGwiuDJQM3KOdYy0cz5H', 'LaqDMQhyJ4nT9bOat96oMpiUJoJfkpr0BZUVlzof9UaQmQXAVQ')
auth.set_access_token('1325833977836556288-4eBpurdKwwloCm9xmUYLT41NhagHcz', 'UWQgE20rtf9d4xVZYnhllkHGppdcjsAeKaoqtGu7OfNWf')
api = tw.API(auth, wait_on_rate_limit=True)

dateTimeObj = datetime.now()
strTimestamp = dateTimeObj.strftime("%Y-%m-%d %H:%M")

ids = []
for page in tw.Cursor(api.followers_ids, screen_name="DanielZirkel").pages():
    ids.extend(page)

dfTwitterFollower = pd.DataFrame()


dfTwitterFollower[]