import pandas as pd
import plotly.io as pio

pio.renderers.default = 'browser'


scriptPath = __file__
path = scriptPath[:-33] + '/data/'

# create new dataframe for analyzed data
dfRawData = pd.read_csv(path +'TwitterData_overall.csv')
dfRawData['date'] = pd.to_datetime(dfRawData.created_at, errors='coerce')   # convert to datetime and write NaT in case of invalid string
dfRawData = dfRawData[~dfRawData['date'].isna()]                            # remove invalid entries
dfRawData['date'] = dfRawData['date'].dt.strftime('%Y-%m-%d')               # convert format to only day (remove time information)

dfRawData['date'].unique()
dfAnalyzedData = pd.DataFrame(index=dfRawData['date'].unique())

print('Empty Dataframe created')

# files to be evaluated
filenames = ['defichain', 'dfi', 'overall']         # overall must be the last entry to get correct unique users numbers

for twitterSearch in filenames:
    filepath = path +'TwitterData_'+twitterSearch+'.csv'
    
    dfRawData = pd.read_csv(filepath)
    dfRawData['date'] = pd.to_datetime(dfRawData.created_at, errors='coerce')  # convert to datetime and write NaT in case of invalid string
    dfRawData = dfRawData[~dfRawData['date'].isna()]  # remove invalid entries
    dfRawData['date'] = dfRawData['date'].dt.strftime('%Y-%m-%d')  # convert format to only day (remove time information)
    
    # define keywords to filter out non-defichain related Tweets
    filterKeywords = ['@defiqa3']
    index2Use = ~dfRawData.text.str.contains('|'.join(filterKeywords))
    dfRawData = dfRawData[index2Use]
    
    temp = dfRawData.groupby(dfRawData['date'])
    dfAnalyzedData[twitterSearch+'_Activity'] = temp.date.count()
    dfAnalyzedData[twitterSearch+'_Reply'] = temp.in_reply_to_screen_name.count()
    dfAnalyzedData[twitterSearch+'_Likes'] = temp.favorite_count.sum()    
    dfAnalyzedData[twitterSearch+'_Retweet'] = temp['retweeted_status.id'].count()

    temp = dfRawData[dfRawData['in_reply_to_screen_name'].isna() & dfRawData['retweeted_status.id'].isna()].groupby(dfRawData['date'])
    dfAnalyzedData[twitterSearch+'_Tweet'] = temp.date.count()
    print('Information of '+twitterSearch+' analyzed')


# Extract unique users
temp = dfRawData.groupby(dfRawData['date'])
dfAnalyzedData[twitterSearch+'_UniqueUserOverall'] = temp['user.name'].nunique()

temp = dfRawData[~dfRawData['in_reply_to_screen_name'].isna()].groupby(dfRawData['date'])
dfAnalyzedData[twitterSearch+'_UniqueUserReply'] = temp['user.name'].nunique()

temp = dfRawData[~dfRawData['retweeted_status.id'].isna()].groupby(dfRawData['date'])
dfAnalyzedData[twitterSearch+'_UniqueUserRetweet'] = temp['user.name'].nunique()

temp = dfRawData[dfRawData['in_reply_to_screen_name'].isna() & dfRawData['retweeted_status.id'].isna()].groupby(dfRawData['date'])
dfAnalyzedData[twitterSearch+'_UniqueUserTweet'] = temp['user.name'].nunique()
# delete old entries (before 14th Nov), because of wrong search syntax on Twitter    
dfAnalyzedData = dfAnalyzedData.iloc[:-9]   


# save analyzed data
filepath = path + 'analyzedTwitterData.csv'
dfAnalyzedData.to_csv(filepath)
print(filepath+' updated')
