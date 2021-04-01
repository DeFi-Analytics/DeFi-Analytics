import requests
import pandas as pd

from datetime import datetime


# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-28] + '/data/'
filepath = path + 'frozenDFICake.csv'


# API request for freezer DFI
link='https://poolapi.cakedefi.com/freezer-page'
siteContent = requests.get(link)
allFrozenCoins = pd.read_json(siteContent.text, orient='colums')

dateTimeObj = datetime.now()
strTimestamp = dateTimeObj.strftime("%Y-%m-%d %H:%M")

# load existing data and add new row
#dfiFreezeRemaining = pd.DataFrame()                        # needed for first time without old data
dfiFreezeRemaining = pd.read_csv(filepath, index_col=0)

# get remaining time for frozen DFI
newData = pd.Series(allFrozenCoins.loc['DFI','remainingTenureDistribution'])
newData.name = strTimestamp
#dfiFreezeRemaining = dfiFreezeRemaining.append(newData)    # needed for first time without old data
dfiFreezeRemaining.loc[strTimestamp] = newData.values

# writing file
dfiFreezeRemaining.to_csv(filepath)
print('Data for Freezer-DFI saved')