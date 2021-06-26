import os
import tweepy as tw
import pandas as pd


scriptPath = __file__
path = scriptPath[:-36] + '/data/'

auth = tw.OAuthHandler('ffPBjkGwiuDJQM3KOdYy0cz5H', 'LaqDMQhyJ4nT9bOat96oMpiUJoJfkpr0BZUVlzof9UaQmQXAVQ')
auth.set_access_token('1325833977836556288-4eBpurdKwwloCm9xmUYLT41NhagHcz', 'UWQgE20rtf9d4xVZYnhllkHGppdcjsAeKaoqtGu7OfNWf')
api = tw.API(auth, wait_on_rate_limit=True)

search_words = ['(%24DFI%20OR%20%40defichain%20OR%20defichain)%20-dEarn%20-dEarnFinance%20-defiqa3', '%40defichain','-dEarn%20-dEarnFinance%20-defiqa3%20(%23%24DFI)', '-defiqa3%20%23DFI', '%23NativeDeFi']
filenames = ['TwitterData_overall', 'TwitterData_defichain', 'TwitterData_dfi', 'TwitterData_hashtagDFI', 'TwitterData_nativeDefi']

filenamesLastweek = ['TwitterDataLastWeek_overall', 'TwitterDataDataLastWeek_defichain', 'TwitterDataDataLastWeek_dfi', 'TwitterDataDataLastWeek_hashtagDFI', 'TwitterDataDataLastWeek_nativeDefi']

for i in range(len(search_words)):
    date_since = "2020-09-01"
    tweets = tw.Cursor(api.search, q=search_words[i], result_type='recent', since=date_since).items(1000)

    json_data = [r._json for r in tweets]   # extract result as json-structure
    temp_df = pd.json_normalize(json_data)  # map json to dataframe

    dfTwitter = temp_df[['id', 'created_at', 'text', 'in_reply_to_screen_name', 'favorite_count', 'user.id', 'user.name', 'retweeted_status.id']]

    scriptPath = os.path.abspath(os.getcwd())
    if scriptPath[0] == 'H':
        scriptPath = scriptPath[:-14]
    filepath = path + filenames[i] + '.csv'


    dfOldData = pd.read_csv(filepath, index_col=0)
    dfOldData = dfOldData[~dfOldData.id.isin(dfTwitter.id)]

    dfTwitter = dfTwitter.append(dfOldData, ignore_index=True)


    dfTwitter.to_csv(filepath)
    print(filepath+' updated')

