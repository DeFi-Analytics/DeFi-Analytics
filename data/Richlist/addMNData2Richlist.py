# Script for getting the Richlist and saving the result into a csv-file
import requests
import ast
import time
import json

import pandas as pd
from datetime import datetime

# filename and add timestamp to it
scriptPath = __file__
filepath = scriptPath[:-21] + '2022-05-24_01-01-47_Richlist.csv'


print('Start script ...')
dfRichList = pd.read_csv(filepath)
dfRichList.drop('mnAddressAPI', axis=1, inplace=True)

# get list of masternodes

link = 'http://api.mydeficha.in/v1/listmasternodes/?state=ENABLED'
siteContent = requests.get(link)
dfMNList = pd.read_json(siteContent.text).transpose()
dfRichList['mnAddressAPI'] = dfRichList['address'].isin(dfMNList.ownerAuthAddress)
dfRichList = dfRichList.merge(dfMNList[['ownerAuthAddress','timelock']].set_index('ownerAuthAddress'),how='left', left_on='address', right_index=True)
print('Finished getting masternode list')



# save data to csv-file
dfRichList.to_csv(filepath, index=False)
print('... Richlist saved')
