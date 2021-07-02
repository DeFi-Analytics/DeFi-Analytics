import requests
import pandas as pd
import json
from datetime import datetime


# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-30] + '/data/'
filepath = path + 'mnNodehub.csv'


# API request masternode number
link='https://nodehub.io/public_api/coins'
siteContent = requests.get(link)
dfJSON = pd.read_json(siteContent.text, orient='columns')
dfDFI = dfJSON[dfJSON.ticker=='DFI']

dateTimeObj = datetime.now()
strTimestamp = dateTimeObj.strftime("%Y-%m-%d")
s = pd.Series([strTimestamp])
dfDFI.set_index([s], inplace=True)


dfMNgetnodeio = pd.read_csv(filepath, index_col=0)
dfMNgetnodeio = dfMNgetnodeio.append(dfDFI)
dfMNgetnodeio.to_csv(filepath)

print('Data nodehub.io saved')