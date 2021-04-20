import tweepy as tw
import pandas as pd
from datetime import datetime

scriptPath = __file__
path = scriptPath[:-34] + '/data/'
filepath = path +'TwitterData_follower.csv'
filepathLastList = path +'TwitterData_lastFollowerList.csv'

# create API for Twitter access
auth = tw.OAuthHandler('ffPBjkGwiuDJQM3KOdYy0cz5H', 'LaqDMQhyJ4nT9bOat96oMpiUJoJfkpr0BZUVlzof9UaQmQXAVQ')
auth.set_access_token('1325833977836556288-4eBpurdKwwloCm9xmUYLT41NhagHcz', 'UWQgE20rtf9d4xVZYnhllkHGppdcjsAeKaoqtGu7OfNWf')
api = tw.API(auth, wait_on_rate_limit=True)

# get current date
dateTimeObj = datetime.now()
strTimestamp = dateTimeObj.strftime("%Y-%m-%d")

# create list of defichain followers
ids = []
for page in tw.Cursor(api.followers_ids, screen_name="defichain").pages():
    ids.extend(page)
dfCurrentTwitterFollower = pd.DataFrame()
dfCurrentTwitterFollower[strTimestamp] = ids

# get absolute number of followers
nbFollower = dfCurrentTwitterFollower.shape[0]

# compare current follower list with old list
dfOldTwitterFollower = pd.read_csv(filepathLastList, index_col=0)
nbFollowed = (~dfCurrentTwitterFollower.iloc[:, 0].isin(dfOldTwitterFollower.iloc[:, 0])).sum()
nbUnfollowed = (~dfOldTwitterFollower.iloc[:, 0].isin(dfCurrentTwitterFollower.iloc[:, 0])).sum()

# extract data from old and new follower list; add to exisiting database
#dfTwitterFollowerData = pd.DataFrame(columns=['Date', 'Follower', 'followedToday', 'unfollowedToday'])         # if a need database is needed
dfTwitterFollowerData = pd.read_csv(filepath, index_col=0)
newDataSeries = pd.Series([strTimestamp, nbFollower, nbFollowed, nbUnfollowed], index=dfTwitterFollowerData.columns, name=strTimestamp)
dfTwitterFollowerData = dfTwitterFollowerData.append(newDataSeries, ignore_index=True)


# dfTwitterFollower = pd.read_csv(filepath,index_col=0)

# saving data
#dfTwitterFollower[strTimestamp] = ids
dfTwitterFollowerData.to_csv(filepath)
dfCurrentTwitterFollower.to_csv(filepathLastList)