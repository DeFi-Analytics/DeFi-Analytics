import requests
import pandas as pd

from datetime import datetime


# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-40] + '/data/'
filepath = path + 'dataVisitsIncome.csv'


# API request for freezer DFI
link='https://analytics.topiet.de/index.php?module=API&method=VisitsSummary.getVisits&idSite=6&period=day&date=last35&format=JSON&token_auth=d9f89b984d8701dec0ddf59e9c6fb196'
siteContent = requests.get(link)
dataVisits = pd.read_json(siteContent.text, typ='series')
dataVisits.drop(dataVisits.index[-1],inplace=True) # delete last entry, while current day is not complete

#dfDataVisits = pd.Series(dtype=int)
dfDataVisits = pd.read_csv(filepath, index_col=0, squeeze=True)
newEntry = dataVisits[~dataVisits.index.isin(dfDataVisits.index)]
dfDataVisits = dfDataVisits.append(newEntry)

dfDataVisits.to_csv(filepath)