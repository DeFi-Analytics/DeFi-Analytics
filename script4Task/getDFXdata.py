import requests
import pandas as pd
import json
import numpy as np

from datetime import datetime


# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-26] + '/data/'
filepath = path + 'dfxData.csv'


# API request for freezer DFI
link='https://api.dfx.swiss/v1/statistic'
siteContent = requests.get(link)
temp= json.loads(siteContent.text)

try:
    buyOrder = temp['dfxStatistic']['routes']['buy']
    sellOrder = temp['dfxStatistic']['routes']['sell']
except:
    print('Error in volume data')
    buyOrder = np.nan
    sellOrder = np.nan

try:
    buyVolume = temp['dfxStatistic']['volume']['DFI']['buy']
    sellVolume = temp['dfxStatistic']['volume']['DFI']['sell']
except:
    print('Error in DFI volume data')
    buyVolume = np.nan
    sellVolume = np.nan

try:
    buyVolumeCHF = temp['dfxStatistic']['volume']['CHF']['buy']
    sellVolumeCHF = temp['dfxStatistic']['volume']['CHF']['sell']
except:
    print('Error in CHF volume data')
    buyVolume = np.nan
    sellVolume = np.nan

dateTimeObj = datetime.now()
strTimestamp = dateTimeObj.strftime("%Y-%m-%d %H:%M")

# load existing data and add new row
# dfDFXData = pd.DataFrame(columns=['buyOrder', 'sellOrder', 'buyVolume', 'sellVolume'])                        # needed for first time without old data
dfDFXData = pd.read_csv(filepath, index_col=0)

# get remaining time for frozen DFI
newData = pd.Series(data=[buyOrder, sellOrder, buyVolume, sellVolume, buyVolumeCHF, sellVolumeCHF], index=['buyOrder', 'sellOrder', 'buyVolume', 'sellVolume', 'buyVolumeCHF', 'sellVolumeCHF'])
newData.name = strTimestamp
dfDFXData = dfDFXData.append(newData)

# writing file
dfDFXData.to_csv(filepath)
print('Data for DFX saved')