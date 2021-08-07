import requests
import pandas as pd
import numpy as np

import json
import dateutil

# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-34] + '/data/'
filepath = path + 'hourlyDEXTrades.csv'

availablePools = {'ETH':4,'BTC':5,'USDT':6,'DOGE':8,'LTC':10,'BCH':12,'USDC':14}
dfTradeHourlyResult = pd.DataFrame()

# get all swaps over all pools
for key in availablePools: 
    print('Checking trades of pool: ' + key)
    linkTrade = 'https://api.defichain.io/v1/getswaptransaction?id='+str(availablePools.get(key))+'&network=mainnet&skip=0&limit=10000'
    siteContent = requests.get(linkTrade)
    dfJSON = pd.read_json(siteContent.text,orient='columns')
    nbTradesDEX = dfJSON['total'].max()
    
    dfTrades = pd.DataFrame(dfJSON.data.tolist())
    dfTrades['Date'] = pd.to_datetime(dfTrades['blockTime'],utc=True).dt.strftime('%Y-%m-%d')
    dfTrades['DateHour'] = pd.to_datetime(dfTrades['blockTime'],utc=True).dt.round('60min')

    if ((dfTrades['DateHour'].values[0]-dfTrades['DateHour'].values[-1])/ np.timedelta64(1, 's')) / 60 / 60 < 13:
        print('#### ERROR: not enough trades for 13 hours')

    availableBaseToken = dfTrades.baseTokenSymbol.unique()
    dfTradeHourlyResult[key+'pool_nbTrades'] = dfTrades.groupby('DateHour')['_id'].count()
    dfTradeHourlyResult[key+'pool_base'+availableBaseToken[0]] = dfTrades.loc[dfTrades.baseTokenSymbol==availableBaseToken[0]].groupby('DateHour')['baseTokenAmount'].sum()
    dfTradeHourlyResult[key+'pool_quote'+availableBaseToken[0]] = dfTrades.loc[dfTrades.quoteTokenSymbol==availableBaseToken[0]].groupby('DateHour')['quoteTokenAmount'].sum()
    dfTradeHourlyResult[key+'pool_base'+availableBaseToken[1]] = dfTrades.loc[dfTrades.baseTokenSymbol==availableBaseToken[1]].groupby('DateHour')['baseTokenAmount'].sum()
    dfTradeHourlyResult[key+'pool_quote'+availableBaseToken[1]] = dfTrades.loc[dfTrades.quoteTokenSymbol==availableBaseToken[1]].groupby('DateHour')['quoteTokenAmount'].sum()

# keep max last x hours and remove newest row (both may not complete)
lastUsedHours = 24
dfTradeHourlyResult = dfTradeHourlyResult[dfTradeHourlyResult.index[-1]-dateutil.relativedelta.relativedelta(hours=lastUsedHours):dfTradeHourlyResult.index[-2]]


# add usd price information for all coins
nbDays = '30'
currNameCoingecko = ['bitcoin', 'ethereum', 'tether', 'dogecoin', 'litecoin', 'bitcoin-cash', 'usd-coin', 'defichain']
currName = ['BTC', 'ETH', 'USDT', 'DOGE', 'LTC', 'BCH', 'USDC', 'DFI']

for ind in range(8):
    print('Get coinprice for: ' + currName[ind])
    link = 'https://api.coingecko.com/api/v3/coins/'+currNameCoingecko[ind]+'/market_chart?vs_currency=usd&days='+nbDays
    siteContent = requests.get(link)
    tempData = json.loads(siteContent.text)
    dfTemp = pd.DataFrame(tempData['prices'], columns=['timestamp', currName[ind]+'-USD'])
    dfTemp.set_index(pd.to_datetime(dfTemp['timestamp'], unit='ms').dt.round('60min'), inplace=True)
    dfTemp.index = dfTemp.index.tz_localize(tz='UTC')

    #dfTradeHourlyResult = dfTradeHourlyResult.merge(dfTemp[currName[ind]+'-USD'], how='outer', left_index=True, right_index=True) # create new column (first time)
    #dfTradeHourlyResult[currName[ind]+'-USD'].interpolate(method='pad', inplace=True)
    #dfTradeHourlyResult.drop(['BTC-USD'],inplace=True, axis=1)

    dfTemp = dfTemp[~dfTemp.index.duplicated(keep='first')]     # remove duplicates
    dfTradeHourlyResult.loc[dfTemp.index[dfTemp.index.isin(dfTradeHourlyResult.index)], currName[ind] + '-USD'] = dfTemp.loc[dfTemp.index[dfTemp.index.isin(dfTradeHourlyResult.index)], currName[ind] + '-USD'].values # replace existing price entries with new ones, but only for available index values
    dfTradeHourlyResult[currName[ind] + '-USD'].interpolate(method='pad', inplace=True)


# save updated file

dfOldTradeHourlyResult = pd.read_csv(filepath, index_col=0)
dfOldTradeHourlyResult.index = pd.to_datetime(dfOldTradeHourlyResult.index)
dfOldTradeHourlyResult = dfOldTradeHourlyResult[~dfOldTradeHourlyResult.index.isin(dfTradeHourlyResult.index)]
dfTradeHourlyResult = dfOldTradeHourlyResult.append(dfTradeHourlyResult, sort=False)
dfTradeHourlyResult.to_csv(filepath)



