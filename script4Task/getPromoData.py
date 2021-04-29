import requests
import pandas as pd
import json
from datetime import datetime


# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-28] + '/data/'
filepath = path + 'defichainPromoData.csv'


# API request for promo posts
link='https://api.defichain-promo.com/v1/posts'
siteContent = requests.get(link)
dataPostsAPI = json.loads(siteContent.text)

# API request for promo media
link='https://api.defichain-promo.com/v1/media'
siteContent = requests.get(link)
dataMediaAPI = json.loads(siteContent.text)

dateTimeObj = datetime.now()
strTimestamp = dateTimeObj.strftime("%Y-%m-%d")

colNames = ['postActive', 'postsDeclined', 'postsWaiting', 'mediaActive', 'mediaDeclined', 'mediaWaiting']
currentData = [dataPostsAPI['data']['active']['count'], dataPostsAPI['data']['declined']['count'], dataPostsAPI['data']['waiting']['count'], \
               dataMediaAPI['data']['active']['count'], dataMediaAPI['data']['declined']['count'], dataMediaAPI['data']['waiting']['count']]


# load existing data and add new row
# dfPromoData = pd.DataFrame(columns=colNames)                        # needed for first time without old data
dfPromoData = pd.read_csv(filepath, index_col=0)

# get remaining time for frozen DFI
newData = pd.Series(index=colNames, data=currentData)
newData.name = strTimestamp
#dfiFreezeRemaining = dfiFreezeRemaining.append(newData)    # needed for first time without old data
dfPromoData.loc[strTimestamp] = newData.values

# writing file
dfPromoData.to_csv(filepath)
print('Defichain Promo data saved')