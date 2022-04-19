import requests
import pandas as pd
from datetime import datetime
import json
import numpy as np


scriptPath = __file__
path = scriptPath[:-29] + '/data/'

def getDFIPFuturesData(timeStampData):
    filepath = path + 'DFIPFuturesData.csv'

    newData = pd.Series(name=timeStampData, dtype=object)

    # API request available loan schemes
    link = 'http://api.mydefichain.com/v1/listgovs/'
    siteContent = requests.get(link)
    tempData = json.loads(siteContent.text)
    tempDataDFIP = tempData[8][0]['ATTRIBUTES']

    for item in tempDataDFIP['v0/live/economy/dfip2203_burned']:
        dataName = 'DFIPFuture_burned_' + item[item.find('@') + 1:]
        newData[dataName] = item[:item.find('@')]

    for item in tempDataDFIP['v0/live/economy/dfip2203_minted']:
        dataName = 'DFIPFuture_minted_' + item[item.find('@') + 1:]
        newData[dataName] = item[:item.find('@')]

    for item in tempDataDFIP['v0/live/economy/dfip2203_current']:
        dataName = 'DFIPFuture_current_' + item[item.find('@') + 1:]
        newData[dataName] = item[:item.find('@')]

    dfOldDFIPData = pd.read_csv(filepath, index_col=0)
    # dfOldDFIPData = pd.DataFrame()
    dfDFIPData = dfOldDFIPData.append(newData, sort=False)
    dfDFIPData.to_csv(filepath)

    print('finished DFIP futures data acquisition')

def getVaultsData(timeStampData):
    # generate filepath relative to script location
    filepath = path + 'vaultsData.csv'

    # API request available loan schemes
    link = 'https://ocean.defichain.com/v0/mainnet/loans/schemes?size=200'
    siteContent = requests.get(link)
    tempData = json.loads(siteContent.text)
    listAvailableSchemes =[]
    for item in tempData['data']:
        listAvailableSchemes.append(item['id'])


    # API request of available decentralized tokens
    listAvailableTicker = []
    newDataAPI = True
    nextPage = ''
    while newDataAPI:
        link = 'https://ocean.defichain.com/v0/mainnet/loans/tokens?size=200'
        siteContent = requests.get(link)
        tempData = json.loads(siteContent.text)
        if 'page' in tempData:
            nextPage = tempData['page']['next']
        else:
            newDataAPI = False
        for item in tempData['data']:
            listAvailableTicker.append(item['token']['symbol'])
    listAvailableTokens = ['sumLoan' + item for item in listAvailableTicker] + ['sumLoanLiquidation' + item for item in listAvailableTicker]

    # API request of available ticker prices
    dfOracle = pd.DataFrame()
    newDataAPI = True
    nextPage = ''
    while newDataAPI:
        link = 'https://ocean.defichain.com/v0/mainnet/prices?size=50'+nextPage
        siteContent = requests.get(link)
        tempData = json.loads(siteContent.text)
        # check if another page must be requested
        if 'page' in tempData:
            nextPage = '&next=' + tempData['page']['next']
        else:
            newDataAPI = False
        # get needed data out of json structure
        tempDataDict = {}
        for item in tempData['data']:
            tempDataDict[item['id']] = item['price']['aggregated']['amount']
        dfOracle = dfOracle.append(pd.DataFrame(data=tempDataDict.values(), index=tempDataDict.keys()))

    linkBurninfo = 'http://main.mackchain.de/api/getburninfo'
    siteContent = requests.get(linkBurninfo)
    try:
        tempData = json.loads(siteContent.text)
        burnedAuction = tempData['auctionburn']
        burnedPayback = tempData['paybackburn']
        burnedDFIPayback = tempData['dfipaybackfee']
        dfipaybacktokens = tempData['dfipaybacktokens']
        dexfeetokens = tempData['dexfeetokens']

    except:
        print('### Error getburninfo ###')
        burnedAuction = np.NaN
        burnedPayback = np.NaN
        burnedDFIPayback = np.NaN

    vaultData = pd.Series(index=listAvailableTokens+listAvailableSchemes+['nbVaults', 'nbLoans', 'nbLiquidation', 'sumInterest', 'sumDFI', 'sumBTC', 'sumUSDC', 'sumUSDT', 'sumDUSD', 'sumETH']+dfOracle.index.to_list()+['burnedAuction', 'burnedPayback','burnedDFIPayback','dfipaybacktokens', 'dexfeetokens'],
                          data=len(listAvailableTokens)*[0] + len(listAvailableSchemes)*[0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]+dfOracle.iloc[:,0].tolist()+[burnedAuction, burnedPayback, burnedDFIPayback, dfipaybacktokens, dexfeetokens])


    # API request current vaults
    newDataAPI = True
    nextPage = ''
    while newDataAPI:
        link = 'https://ocean.defichain.com/v0/mainnet/loans/vaults?size=30'+nextPage
        siteContent = requests.get(link)
        tempData = json.loads(siteContent.text)

        # check if another page must be requested
        if 'page' in tempData:
            nextPage = '&next=' + tempData['page']['next']
        else:
            newDataAPI = False


        # evaluate the data inside the vaults
        for item in tempData['data']:
            vaultData['nbVaults'] += 1
            if item['state'] == 'ACTIVE':
                vaultData['nbLoans'] += len(item['loanAmounts'])
                vaultData[item['loanScheme']['id']] += 1
                vaultData['sumInterest'] += float(item['interestValue'])
                for coinsCollateral in item['collateralAmounts']:
                    vaultData['sum'+coinsCollateral['symbol']] += float(coinsCollateral['amount'])
                for coinsMinted in item['loanAmounts']:
                    vaultData['sumLoan'+coinsMinted['symbol']] += float(coinsMinted['amount'])

            elif item['state'] == 'IN_LIQUIDATION':
                for batches in item['batches']:
                    vaultData['sumLoanLiquidation'+batches['loan']['symbol']] += float(batches['loan']['amount'])
                vaultData['nbLiquidation'] += 1

        vaultData.name = timeStampData

    # save file
    # dfOldVaultData = pd.DataFrame()
    dfOldVaultData = pd.read_csv(filepath, index_col=0)
    dfVaultData = dfOldVaultData.append(vaultData, sort=False)
    dfVaultData.to_csv(filepath)

    print('finished vaults/loans data acquisition')

timeStampData = pd.Timestamp.now()
getDFIPFuturesData(timeStampData)
getVaultsData(timeStampData)

