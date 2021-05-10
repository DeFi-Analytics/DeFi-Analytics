import requests
import pandas as pd
import json
from datetime import datetime


# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-40] + '/data/'
filepath = path + 'masternodeMonitorData.csv'


# API request masternode number
link='https://sync.defichain-masternode-monitor.com/v1/statistics/count/masternodes'
siteContent = requests.get(link)
nbMasternodes = int(siteContent.text)

# API request account number
link='https://sync.defichain-masternode-monitor.com/v1/statistics/count/accounts'
siteContent = requests.get(link)
nbAccounts = int(siteContent.text)

colNames = ['nbMasternodes', 'nbAccounts']
currentData = [nbMasternodes, nbAccounts]

dateTimeObj = datetime.now()
strTimestamp = dateTimeObj.strftime("%Y-%m-%d")

# load existing data and add new row
# dfMNMonitor = pd.DataFrame(columns=colNames)                        # needed for first time without old data
dfMNMonitor = pd.read_csv(filepath, index_col=0)

# get remaining time for frozen DFI
newData = pd.Series(index=colNames, data=currentData)
newData.name = strTimestamp
dfMNMonitor = dfMNMonitor.append(newData)
#dfPromoData.loc[strTimestamp] = newData.values

# writing file
dfMNMonitor.to_csv(filepath)
print('Defichain Promo data saved')