import requests
import pandas as pd
from datetime import datetime

# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-28] + '/data/'
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

print('Data allnode saved')