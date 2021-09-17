import requests
import pandas as pd
from datetime import datetime

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


