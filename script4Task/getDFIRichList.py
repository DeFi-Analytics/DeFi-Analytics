# Script for getting the Richlist and saving the result into a csv-file
import requests
import ast
import time
import json

import pandas as pd
from datetime import datetime

# filename and add timestamp to it
now = datetime.now()
timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
scriptPath = __file__
path = scriptPath[:-29] + '/data/Richlist/'
filepath = path + timestamp + '_Richlist.csv'
filepathOldMNList = scriptPath[:-29] + '/data/currentMNList.csv'

print('Start script ...')

bGetRichlist = True

while bGetRichlist:
    # get DFI-Richlist data
    link = "https://chainz.cryptoid.info/dfi/api.dws?q=allbalances&key=6ba465be70b4"
    cryptoIDContent = requests.get(link)
    if cryptoIDContent.status_code == 200:
        apiCryptoIDAsDict = ast.literal_eval(cryptoIDContent.text)
        dfRichList = pd.DataFrame(data={'address': list(apiCryptoIDAsDict['balances'].keys()), 'balance': list(apiCryptoIDAsDict['balances'].values())}).sort_values(by=['balance'],ascending=False)
        dfRichList = dfRichList.drop(dfRichList[dfRichList.address.isin(['nulldata', 'op_return'])].index).reset_index(drop=True)  # remove line with nulldata and op_return
        bGetRichlist = False
        print('Finished getting complete DFI richlist')
    else:
        print('Error with API for complete Richlist')
        time.sleep(300)

# get DFI token amount and add to richlist as own entry
# try:
#     link = "https://api.defichain.io/v1/gettokenrichlist?id=0&network=mainnet"
#     siteContent = requests.get(link)
#     temp = pd.read_json(siteContent.text)
#
#     seriesDFI2Add = pd.Series(['DFITokenOnDefiChain', temp.balance.sum()], index=['address', 'balance'])
#     dfRichList = dfRichList.append(seriesDFI2Add, ignore_index=True, sort=False)
#     print('Finished getting DFI Token data')
# except:
#     print('Error with API for DFI token data')


# get list of masternodes
try:
    link = 'https://api.mydeficha.in/v1/listmasternodes/?state=ENABLED'
    siteContent = requests.get(link)
    dfMNList = pd.read_json(siteContent.text).transpose() 
    dfRichList['mnAddressAPI'] = dfRichList['address'].isin(dfMNList.ownerAuthAddress)
    dfRichList = dfRichList.merge(dfMNList[['ownerAuthAddress','timelock']].set_index('ownerAuthAddress'),how='left', left_on='address', right_index=True)
    print('Finished getting masternode list')
except:
    dfOldMNList = pd.read_csv(filepathOldMNList, index_col=0)
    dfRichList['mnAddressAPI'] = dfRichList['address'].isin(dfOldMNList.ownerAuthAddress)
    print('Error with API of masternode list')


# get list of masternodes hosted by Cake
headers = { 'User-Agent': 'Safari/537.36'}
try:
    link = 'https://poolapi.cakedefi.com/nodes?order=status&orderBy=DESC'
    siteContent = requests.get(link, headers=headers)
    dfMNListCake = pd.read_json(siteContent.text)
    dfRichList['mnAddressCakeAPI'] = dfRichList['address'].isin(dfMNListCake[dfMNListCake.coin=='DeFi'].address)
    print('Finished getting Cake masternode list')
except:
    print('Error with API of Cake masternode list')

# save data to csv-file
dfRichList.to_csv(filepath, index=False)
print('... Richlist saved')
