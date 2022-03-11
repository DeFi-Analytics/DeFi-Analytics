import requests
import pandas as pd
import json
import numpy as np

from datetime import datetime


# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-26] + '/data/'
filepathSummary = path + 'dfxData.csv'
filepathComplete = path + 'dfxAllOrdersData.csv'

# API request for complete transaction list of DFX
link='https://api.dfx.swiss/v1/statistic/transactions'
siteContent = requests.get(link)
tempData= json.loads(siteContent.text)

# load existing list of orders
dfDFXorders = pd.DataFrame()

tempDataframe = pd.DataFrame(tempData['buy'])
tempDataframe['order'] = 'buy'
dfDFXorders = dfDFXorders.append(tempDataframe)

tempDataframe = pd.DataFrame(tempData['sell'])
tempDataframe['order'] = 'sell'
dfDFXorders = dfDFXorders.append(tempDataframe)

dfDFXorders.drop_duplicates(inplace=True)
dfDFXorders['date'] = pd.to_datetime(dfDFXorders['date'])
dfDFXorders.sort_values(by='date', inplace=True)
dfDFXorders.set_index('date', inplace=True)

# dfDFXorders.to_csv(filepathComplete)


# get hourly data
dfDFXData = pd.DataFrame(columns=['dfxBuyVolume', 'dfxSellVolume'])
dfDFXData['dfxBuyVolume'] = dfDFXorders[dfDFXorders.order == 'buy'].fiatAmount.groupby(pd.Grouper(freq='H')).sum()
dfDFXData['dfxBuyVolume'] = dfDFXData['dfxBuyVolume'].fillna(0).cumsum()
dfDFXData['dfxSellVolume'] = dfDFXorders[dfDFXorders.order == 'sell'].fiatAmount.groupby(pd.Grouper(freq='H')).sum()
dfDFXData['dfxSellVolume'] = dfDFXData['dfxSellVolume'].fillna(0).cumsum()

dfDFXData.index = dfDFXData.index.strftime('%Y-%m-%d %H:%M')
# writing file
dfDFXData.to_csv(filepathSummary)
print('Data for DFX saved')