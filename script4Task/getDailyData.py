import requests
import pandas as pd
from datetime import datetime
import json

scriptPath = __file__
path = scriptPath[:-28] + '/data/'

def getMNallnode():
    # generate filepath relative to script location
    filepath = path + 'mnAllnodes.csv'

    # API request masternode number
    link='https://mydeficha.in/en/content/allnodes.php'
    siteContent = requests.get(link)
    nbMN = int(siteContent.text)

    dateTimeObj = datetime.now()
    strTimestamp = dateTimeObj.strftime("%Y-%m-%d")
    dfMN = pd.Series(index=['date','nbMNAllnode'], data=[strTimestamp,nbMN])

    dfMNallnode = pd.read_csv(filepath, index_col=0)
    dfMNallnode = dfMNallnode.append(dfMN,ignore_index=True)
    dfMNallnode.to_csv(filepath)

def getMNnodehubio():
    filepath = path + 'mnNodehub.csv'

    # API request masternode number
    link = 'https://nodehub.io/public_api/coins'
    siteContent = requests.get(link)
    dfJSON = pd.read_json(siteContent.text, orient='columns')
    dfDFI = dfJSON[dfJSON.ticker == 'DFI']

    dateTimeObj = datetime.now()
    strTimestamp = dateTimeObj.strftime("%Y-%m-%d")
    s = pd.Series([strTimestamp])
    dfDFI.set_index([s], inplace=True)

    dfMNgetnodeio = pd.read_csv(filepath, index_col=0)
    dfMNgetnodeio = dfMNgetnodeio.append(dfDFI)
    dfMNgetnodeio.to_csv(filepath)

def getMNMonitorData():
    # generate filepath relative to script location
    filepath = path + 'masternodeMonitorData.csv'

    # API request masternode number
    link = 'https://sync.defichain-masternode-monitor.com/v1/statistics/count/masternodes'
    siteContent = requests.get(link)
    nbMasternodes = int(siteContent.text)

    # API request account number
    link = 'https://sync.defichain-masternode-monitor.com/v1/statistics/count/accounts'
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
    # dfPromoData.loc[strTimestamp] = newData.values

    # writing file
    dfMNMonitor.to_csv(filepath)

def getDFISignalData():
    # generate filepath relative to script location
    filepath = path + 'dfiSignalData.csv'

    # API request masternode number
    link='https://api.dfi-signal.com/v1/statistics/all'
    siteContent = requests.get(link)
    jsonData = json.loads(siteContent.text)
    dfNewData = pd.DataFrame(jsonData['data'])
    dfNewData.set_index('date', inplace=True)


    dfDFISignal = pd.read_csv(filepath, index_col=0)
    dfDFISignal = pd.concat([dfDFISignal, dfNewData]).drop_duplicates().sort_index()
    dfDFISignal.to_csv(filepath)

def getDobbyData():
    # generate filepath relative to script location
    filepath = path + 'dobbyData.csv'

    # API request masternode numaber
    link='https://api.defichain-dobby.com/statistics?page=1'
    siteContent = requests.get(link)
    jsonData = json.loads(siteContent.text)
    dfNewData = pd.DataFrame(columns = ['date', 'user_count', 'vault_count', 'sum_messages', 'sum_collateral', 'sum_loan', 'avg_ratio'],
                             data = [[item['date'],item['user_count'],item['vault_count'],item['messages']['sum_messages'],item['sum_collateral'],item['sum_loan'],item['avg_ratio']] for item in jsonData['data']])
    dfNewData.set_index('date', inplace=True)


    dfDobby = pd.read_csv(filepath, index_col=0)
    dfDobby = pd.concat([dfDobby, dfNewData]).drop_duplicates().sort_index()
    dfDobby.to_csv(filepath)

def getEmissionData():
    # generate filepath relative to script location
    filepath = path + 'dfiEmissionData.csv'

    dateTimeObj = datetime.now()
    strTimestamp = dateTimeObj.strftime("%Y-%m-%d")

    # API request masternode number
    link='https://ocean.defichain.com/v0/mainnet/stats'
    siteContent = requests.get(link)
    jsonData = json.loads(siteContent.text)
    dfNewData = pd.Series(jsonData['data']['emission'])
    dfNewData['dToken'] = dfNewData['total']*0.1234*2
    dfNewData['burned'] = dfNewData['burned'] - dfNewData['dToken']
    dfNewData.name = strTimestamp

    dfDFIemission = pd.read_csv(filepath, index_col=0)
    dfDFIemission = dfDFIemission.append(dfNewData)
    # dfPromoData.loc[strTimestamp] = newData.values

    # writing file
    dfDFIemission.to_csv(filepath)

def getRedditData():
    # generate filepath relative to script location
    filepath = path + 'redditDefichainData.csv'

    dateTimeObj = datetime.now()
    strTimestamp = dateTimeObj.strftime("%Y-%m-%d")

    # API request reddit user number
    headers = {'User-Agent': 'Safari/537.36'}
    link='https://www.reddit.com/r/defiblockchain/about.json'
    siteContent = requests.get(link, headers=headers)
    jsonData = json.loads(siteContent.text)

    dfReddit = pd.read_csv(filepath, index_col=0)
    dfReddit.loc[strTimestamp] = jsonData['data']['subscribers']

    # writing file
    dfReddit.to_csv(filepath)



# call all acquisition functions with error handling

# Allnode Masternodes
try:
    getMNallnode()
    print('Data allnode saved')
except:
    print('### Error in allnode data acquisition')

# Nodehubio masternodes
try:
    getMNnodehubio()
    print('Data nodehub.io saved')
except:
    print('### Error in nodehub.io data acquisition')

# Masternode monitor data
try:
    getMNMonitorData()
    print('Data Masternode Monitor saved')
except:
    print('### Error in Masternode monitor data acquisition')

# DFI-Signal data
try:
    getDFISignalData()
    print('Data DFI-Signal saved')
except:
    print('### Error in DFI-Signal data acquisition')

# Dobby data
try:
    getDobbyData()
    print('Data Dobby saved')
except:
    print('### Error in Dobby data acquisition')

# DFI emission data
try:
    getEmissionData()
    print('Data DFI emission saved')
except:
    print('### Error in DFI emission data acquisition')


# Official DefiChain Reddit
try:
    getRedditData()
    print('Reddit data saved')
except:
    print('### Error in Reddit data acquisition')