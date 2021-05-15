# Script for getting the Richlist and saving the result into a csv-file
import requests
import ast

import pandas as pd
from datetime import datetime

# filename and add timestamp to it
now = datetime.now()
timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
scriptPath = __file__
path = scriptPath[:-29] + '/data/Richlist/'
filepath = path + timestamp + '_Richlist.csv'
filepathOldMNList = scriptPath[:-29] + '/data/currentMNList.csv'

# get DFI-Richlist data
link = "http://mainnet-api.defichain.io/api/DFI/mainnet/address/stats/rich-list?pageno=1&pagesize=200000"
siteContent = requests.get(link)
text2extract = siteContent.text.replace('null','None')
apiContentAsDict=ast.literal_eval(text2extract)
dfRichList = pd.DataFrame(apiContentAsDict['data'])


# convert fi balance into dfi balance
dfRichList.balance = dfRichList.balance/100000000

# get DFI token amount and add to richlist as own entry
try:
    link = "https://api.defichain.io/v1/gettokenrichlist?id=0&network=mainnet"
    siteContent = requests.get(link)
    temp = pd.read_json(siteContent.text)

    seriesDFI2Add = pd.Series(['DFITokenOnDefiChain', temp.balance.sum()], index=['address', 'balance'])
    dfRichList = dfRichList.append(seriesDFI2Add, ignore_index=True, sort=False)
except:
    print('Error with API for DFI token data')


# get list of masternodes
try:
    link = 'http://api.mydeficha.in/v1/listmasternodes/?state=ENABLED'
    siteContent = requests.get(link)
    dfMNList = pd.read_json(siteContent.text).transpose() 
    dfRichList['mnAddressAPI'] = dfRichList['address'].isin(dfMNList.ownerAuthAddress)
except:
    dfOldMNList = pd.read_csv(filepathOldMNList, index_col=0)
    dfRichList['mnAddressAPI'] = dfRichList['address'].isin(dfOldMNList.ownerAuthAddress)
    print('Error with API of masternode list')


# get list of masternodes hosted by Cake
try:
    link = 'https://poolapi.cakedefi.com/nodes?order=status&orderBy=DESC'
    siteContent = requests.get(link)
    dfMNListCake = pd.read_json(siteContent.text)
    dfRichList['mnAddressCakeAPI'] = dfRichList['address'].isin(dfMNListCake[dfMNListCake.coin=='DeFi'].address)
except:
    print('Error with API of Cake masternode list')

# save data to csv-file
dfRichList.to_csv(filepath, index=False)
