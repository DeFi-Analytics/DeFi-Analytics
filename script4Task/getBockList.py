import requests
import ast

import pandas as pd

scriptPath = __file__
path = scriptPath[:-27] + '/data/'
filepath = path +'BlockListStatistics.csv'

limit4Block = 8000
link = 'http://mainnet-api.defichain.io/api/DFI/mainnet/block?limit='+str(limit4Block)+'&anchorsOnly=false'
siteContent = requests.get(link)
apiContentAsDict=ast.literal_eval(siteContent.text)

dfBlockList = pd.DataFrame(apiContentAsDict)
dfBlockList.set_index('height',inplace=True)
dfBlockList.drop(columns=['chain','network','previousBlockHash','nextBlockHash'],inplace=True)

dfBlockList.sort_values(by='time',inplace=True)

dfBlockList['DateFormatted'] = pd.to_datetime(dfBlockList['time'],utc=True).dt.strftime('%Y-%m-%d')
dfBlockList['DiffTime'] = pd.to_datetime(dfBlockList['time']).diff().dt.seconds
dfBlockList['transactionCountWOReward'] = dfBlockList.transactionCount.sub(1)
dfBlockList.sort_index(ascending=False, inplace=True)

## Generate Block-Statistics
dfBlockStatistic = pd.DataFrame(index = dfBlockList['DateFormatted'].unique(), columns=[])
dfBlockStatistic['nbBlocks'] = dfBlockList.groupby(dfBlockList['DateFormatted'])['hash'].count()
dfBlockStatistic['txCount'] = dfBlockList.groupby(dfBlockList['DateFormatted']).transactionCount.sum()
dfBlockStatistic['txWOreward'] = dfBlockList.groupby(dfBlockList['DateFormatted']).transactionCountWOReward.sum()

dfBlockStatistic['meanBlockTime'] = dfBlockList.groupby(dfBlockList['DateFormatted']).DiffTime.mean()

dfBlockStatistic['MinBlockTime'] = dfBlockList.groupby(dfBlockList['DateFormatted']).DiffTime.min()
dfBlockStatistic['10PercentBlockTime'] = dfBlockList.groupby(dfBlockList['DateFormatted']).DiffTime.quantile(0.1)
dfBlockStatistic['30PercentBlockTime'] = dfBlockList.groupby(dfBlockList['DateFormatted']).DiffTime.quantile(0.3)
dfBlockStatistic['medianBlockTime'] = dfBlockList.groupby(dfBlockList['DateFormatted']).DiffTime.median()
dfBlockStatistic['70PercentBlockTime'] = dfBlockList.groupby(dfBlockList['DateFormatted']).DiffTime.quantile(0.7)
dfBlockStatistic['90PercentBlockTime'] = dfBlockList.groupby(dfBlockList['DateFormatted']).DiffTime.quantile(0.9)
dfBlockStatistic['MaxBlockTime'] = dfBlockList.groupby(dfBlockList['DateFormatted']).DiffTime.max()

# read exisiting statistic and add new days
dfOldBlockStatistic = pd.read_csv(filepath,index_col=0)
dfOldBlockStatistic = dfOldBlockStatistic.iloc[2:] # delete newest entry to avoid incomplete data

# merge old and current data
dfNewBlockStatistic = dfOldBlockStatistic.append(dfBlockStatistic.loc[~dfBlockStatistic.index.isin(dfOldBlockStatistic.index)])
dfNewBlockStatistic.sort_index(ascending=False,inplace=True)

# save data
dfNewBlockStatistic.to_csv(filepath)