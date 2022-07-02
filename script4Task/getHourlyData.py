import requests
import pandas as pd
import datetime
import json
import numpy as np

from bscScanCredentials import apiKeyToken


scriptPath = __file__
path = scriptPath[:-29] + '/data/'

def getBSCBridgeData():
    # generate filepath relative to script location
    print('   Start acquisition bridgeData ...')
    filepathRaw = path + 'bscDFIBridgeTxData.csv'
    filepath = path + 'bscDFIBridgeData.csv'

    # dfBridgeRaw = pd.DataFrame(columns=['block', 'txId', 'time', 'type', 'amount'])
    dfBridgeRaw = pd.read_csv(filepathRaw, index_col=0)
    newDataAPI = True
    nextPage = ''
    while newDataAPI:
        link = 'https://ocean.defichain.com/v0/mainnet/address/8Jgfq4pBUdJLiFGStunoTCy2wqRQphP6bQ/transactions?size=200'+nextPage
        siteContent = requests.get(link)
        tempData = json.loads(siteContent.text)
        # check if another page must be requested
        if 'page' in tempData:
            nextPage = '&next=' + tempData['page']['next']
        else:
            newDataAPI = False
        # get needed data out of json structure
        for item in tempData['data']:
            if item['id'] in dfBridgeRaw.index:
                print('        reached existing id in bscBridgeData')
                newDataAPI = False
                break
            else:
                dfBridgeRaw.loc[item['id']] = [item['block']['height'], item['txid'], datetime.datetime.fromtimestamp(item['block']['medianTime']).strftime('%Y-%m-%d %H:%M:%S'), item['type'], item['value']]
    # Sort and save tx data
    dfBridgeRaw.sort_values(by=['block'], ascending=False, inplace=True)
    dfBridgeRaw.to_csv(filepathRaw)
    dfBridgeRaw['amount'] = dfBridgeRaw.amount.astype(float)

    # create dataframe by unique tx
    dfBridgeTx = pd.DataFrame()
    dfBridgeTx['time'] = pd.to_datetime(dfBridgeRaw.groupby('txId').time.first())
    dfBridgeTx['block'] = dfBridgeRaw.groupby('txId').block.first()
    dfBridgeTx['nbTx'] = dfBridgeRaw.groupby('txId').block.count()
    dfBridgeTx['vinAmount'] = dfBridgeRaw[dfBridgeRaw['type']=='vin'].groupby('txId').amount.sum()
    dfBridgeTx['voutAmount'] = dfBridgeRaw[dfBridgeRaw['type'] == 'vout'].groupby('txId').amount.sum()
    dfBridgeTx['deltaAmount'] = dfBridgeTx['voutAmount'].fillna(0)-dfBridgeTx['vinAmount'].fillna(0)
    dfBridgeTx.sort_values(by=['block'], ascending=False, inplace=True)

    # create hourly in- and outflow data
    dfBridgeTx.set_index('time', inplace=True)
    dfBridgeData = pd.DataFrame()


    dfBridgeData['bridgeInflow'] = dfBridgeTx[dfBridgeTx['deltaAmount'] >= 0].deltaAmount.groupby(pd.Grouper(freq='H')).sum()

    tempDF = pd.DataFrame()
    tempDF['bridgeOutflow'] = dfBridgeTx[dfBridgeTx['deltaAmount'] < 0].deltaAmount.groupby(pd.Grouper(freq='H')).sum()
    dfBridgeData = dfBridgeData.merge(tempDF['bridgeOutflow'], left_index=True, right_index=True, how='outer')

    tempDF = pd.DataFrame()
    tempDF['bridgeNbInSwaps'] = dfBridgeTx[dfBridgeTx['deltaAmount'] >= 0].block.groupby(pd.Grouper(freq='H')).count()
    dfBridgeData = dfBridgeData.merge(tempDF['bridgeNbInSwaps'], left_index=True, right_index=True, how='outer')

    tempDF = pd.DataFrame()
    tempDF['bridgeNbOutSwaps'] = dfBridgeTx[dfBridgeTx['deltaAmount'] < 0].block.groupby(pd.Grouper(freq='H')).count() # get data, where available
    dfBridgeData = dfBridgeData.merge(tempDF['bridgeNbOutSwaps'], left_index=True, right_index=True, how='outer')

    dfBridgeData['bridgeInflow'] = dfBridgeData['bridgeInflow'].fillna(0)
    dfBridgeData['bridgeOutflow'] = dfBridgeData['bridgeOutflow'].fillna(0)
    dfBridgeData['bridgeNbInSwaps'] = dfBridgeData['bridgeNbInSwaps'].fillna(0)
    dfBridgeData['bridgeNbOutSwaps'] = dfBridgeData['bridgeNbOutSwaps'].fillna(0)
    dfBridgeData.to_csv(filepath)

    print('   finished bridge data acquisition')

def getDFIPFuturesData(timeStampData):
    filepath = path + 'DFIPFuturesData.csv'

    newData = pd.Series(name=timeStampData, dtype=object)

    # API request available loan schemes
    link = 'http://api.mydefichain.com/v1/listgovs/'
    siteContent = requests.get(link)
    tempData = json.loads(siteContent.text)
    tempDataDFIP = tempData[8][0]['ATTRIBUTES']

    if 'v0/live/economy/dfip2203_burned' in tempDataDFIP:
        for item in tempDataDFIP['v0/live/economy/dfip2203_burned']:
            dataName = 'DFIPFuture_burned_' + item[item.find('@') + 1:]
            newData[dataName] = item[:item.find('@')]

    if 'v0/live/economy/dfip2203_minted' in tempDataDFIP:
        for item in tempDataDFIP['v0/live/economy/dfip2203_minted']:
            dataName = 'DFIPFuture_minted_' + item[item.find('@') + 1:]
            newData[dataName] = item[:item.find('@')]

    if 'v0/live/economy/dfip2203_current' in tempDataDFIP:
        for item in tempDataDFIP['v0/live/economy/dfip2203_current']:
            dataName = 'DFIPFuture_current_' + item[item.find('@') + 1:]
            newData[dataName] = item[:item.find('@')]

    dfOldDFIPData = pd.read_csv(filepath, index_col=0)
    # dfOldDFIPData = pd.DataFrame()
    dfDFIPData = dfOldDFIPData.append(newData, sort=False)
    dfDFIPData.to_csv(filepath)

    print('   finished DFIP futures data acquisition')

def getVaultsData(timeStampData):
    # generate filepath relative to script location
    filepath = path + 'vaultsData.csv'
    print('   start vaults/loans data acquisition')

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

    print('   get all vaults via API')
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
    print('   saving vaults/loans data')
    vaultsDataHeader = pd.read_csv(filepath, index_col=0, nrows=0).columns
    types_dict = {'burnedPayback': str, 'dexfeetokens': str, 'dfipaybacktokens': str}
    types_dict.update({col: float for col in vaultsDataHeader if col not in types_dict})
    dfOldVaultData = pd.read_csv(filepath, index_col=0, dtype=types_dict)

    dfVaultData = dfOldVaultData.append(vaultData, sort=False)
    dfVaultData.to_csv(filepath)

    print('   finished vaults/loans data acquisition')


timeStampData = pd.Timestamp.now()

# DFIP Futures data
try:
    getDFIPFuturesData(timeStampData)
    print('DFIP Futures data saved')
except:
    print('### Error in DFIP Futures data acquisition')

# Vaults data
try:
    getVaultsData(timeStampData)
    print('Vaults data saved')
except:
    print('### Error in vaults data acquisition')

# BSC bridge data
try:
    getBSCBridgeData()
    print('BSC bridge data saved')
except:
    print('### Error in BSC bridge data acquisition')

