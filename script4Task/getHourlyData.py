import requests
import pandas as pd
import datetime
import json
import numpy as np
import ast
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

    linkBurninfo = 'https://api.mydefichain.com/v1/getburninfo/'
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

    # check burn address
    linkBurnAddress = 'https://ocean.defichain.com/v0/mainnet/address/8defichainBurnAddressXXXXXXXdRQkSm/tokens?size=30'
    siteContent = requests.get(linkBurnAddress)
    try:
        tempData = json.loads(siteContent.text)
        burnedOverallDUSD = float(tempData['data'][8]['amount'])
    except:
        print('### Error burnAddress ###')
        burnedOverallDUSD = np.NaN

    # get minted value from ocean
    linkMintedOcean = 'https://ocean.defichain.com/v0/mainnet/tokens/15'
    siteContent = requests.get(linkMintedOcean)
    try:
        tempData = json.loads(siteContent.text)
        mintedDUSD = float(tempData['data']['minted'])
    except:
        print('### Error minted token ###')
        mintedDUSD = np.NaN

    # get minted value from node
    linkMintedNode = 'https://api.mydefichain.com/v1/gettoken/'
    siteContent = requests.get(linkMintedNode)
    try:
        tempData = json.loads(siteContent.text)
        mintedDUSDNode = float(tempData['15']['minted'])
    except:
        print('### Error minted token from Node ###')
        mintedDUSDNode = np.NaN

    vaultData = pd.Series(index=listAvailableTokens+listAvailableSchemes+['nbVaults', 'nbLoans', 'nbLiquidation', 'sumInterest', 'sumDFI', 'sumBTC', 'sumUSDC', 'sumUSDT', 'sumDUSD', 'sumETH']+dfOracle.index.to_list()+
                                ['burnedAuction', 'burnedPayback','burnedDFIPayback','dfipaybacktokens', 'dexfeetokens','burnedOverallDUSD', 'mintedDUSD', 'mintedDUSDnode'],
                          data=len(listAvailableTokens)*[0] + len(listAvailableSchemes)*[0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]+dfOracle.iloc[:,0].tolist()+
                                [burnedAuction, burnedPayback, burnedDFIPayback, dfipaybacktokens, dexfeetokens, burnedOverallDUSD, mintedDUSD, mintedDUSDNode])

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

def getDUSDBurnBotData():
    def acquireTXAdresse(botAddress, dfOldTxList):
        # get the first 200 entries of burn bot listaccounthistory
        link = 'https://ocean.defichain.com/v0/mainnet/address/'+botAddress+'/history?size=200'
        siteContent = requests.get(link)
        apiContentAsDict = ast.literal_eval(siteContent.text)
        dfBurnBotTxList = pd.DataFrame(apiContentAsDict['data'])

        dfBurnBotTxList = dfBurnBotTxList[~dfBurnBotTxList['txid'].isin(dfOldTxList['txid'])]

        if dfBurnBotTxList.shape[0] > 0:
            # get the rest of listaccounthistory
            while ('page' in apiContentAsDict) & (dfBurnBotTxList.shape[0].__mod__(20) == 0):
                link = 'https://ocean.defichain.com/v0/mainnet/address/'+botAddress+'/history?size=200&next=' + apiContentAsDict['page']['next']
                siteContent = requests.get(link)
                apiContentAsDict = ast.literal_eval(siteContent.text)
                dfBurnBotTxList = dfBurnBotTxList.append(pd.DataFrame(apiContentAsDict['data']))

            dfBurnBotTxList.reset_index(inplace=True, drop=True)
            dfBurnBotTxList = pd.concat([dfBurnBotTxList, dfBurnBotTxList['block'].apply(pd.Series)], axis=1)
            dfBurnBotTxList.drop(columns=['owner', 'txn', 'block', 'hash'], inplace=True)
            dfBurnBotTxList = dfBurnBotTxList[dfBurnBotTxList['type'] == 'PoolSwap']

            # screen burn address for corresponding dUSD amount
            # get the first 200 entries of burn bot listaccounthistory
            link = 'https://ocean.defichain.com/v0/mainnet/address/8defichainBurnAddressXXXXXXXdRQkSm/history?size=200'
            siteContent = requests.get(link)
            apiContentAsDict = ast.literal_eval(siteContent.text)
            dfBurnAddressTxList = pd.DataFrame(apiContentAsDict['data'])
            dfBurnBotTxList = dfBurnBotTxList.merge(dfBurnAddressTxList[['txid', 'amounts']], left_on='txid', right_on='txid', how='left')
            dfBurnBotTxList['amounts_y'] = pd.to_numeric(dfBurnBotTxList['amounts_y'].astype(str).str[2:-7]).fillna(0)

            # get the rest of listaccounthistory
            while ('page' in apiContentAsDict) & dfBurnBotTxList['amounts_y'].eq(0).any():
                link = 'https://ocean.defichain.com/v0/mainnet/address/8defichainBurnAddressXXXXXXXdRQkSm/history?size=200&next=' + apiContentAsDict['page']['next']
                siteContent = requests.get(link)
                apiContentAsDict = ast.literal_eval(siteContent.text)
                dfBurnAddressTxList = pd.DataFrame(apiContentAsDict['data'])
                dfBurnBotTxList = dfBurnBotTxList.merge(dfBurnAddressTxList[['txid', 'amounts']], left_on='txid', right_on='txid', how='left')
                dfBurnBotTxList['amounts'] = pd.to_numeric(dfBurnBotTxList['amounts'].astype(str).str[2:-7])
                dfBurnBotTxList['amounts_y'] = dfBurnBotTxList['amounts_y'].fillna(0) + dfBurnBotTxList['amounts'].fillna(0)
                dfBurnBotTxList.drop(columns=['amounts'], inplace=True)

            dfBurnBotTxList['amounts_x'] = pd.to_numeric(dfBurnBotTxList['amounts_x'].astype(str).str[2:-6])
            dfBurnBotTxList.set_index(pd.to_datetime(dfBurnBotTxList['time'], utc=True, unit='s'), inplace=True)
            dfBurnBotTxList.rename(columns={"time": "timeRaw"}, inplace=True)

        return dfBurnBotTxList

    # generate filepath relative to script location
    filepathTxList = path + 'dUSDBornBotTx.csv'
    filepathTxList2 = path + 'dUSDBornBot2Tx.csv'
    print('   start dUSD burn bot data acquisition')


    ######### get all swaps from Bot1 und Bot2 #########
    # Tx list Bot1
    dfBurnBotOldTxList = pd.read_csv(filepathTxList, index_col=0)
    dfBurnBotOldTxList.index = pd.to_datetime(dfBurnBotOldTxList.index)
    dfBurnBotTxList = acquireTXAdresse('df1qa6qjmtuh8fyzqyjjsrg567surxu43rx3na7yah', dfBurnBotOldTxList)
    dfBurnBotTxList = dfBurnBotOldTxList.append(dfBurnBotTxList)
    dfBurnBotTxList.sort_values(by=['height'], ascending=False, inplace=True)
    dfBurnBotTxList.to_csv(filepathTxList)
    print('   tx list burn bot 1 saved')

    #Tx List Bot2
    dfBurnBot2OldTxList = pd.read_csv(filepathTxList2, index_col=0)
    dfBurnBot2OldTxList.index = pd.to_datetime(dfBurnBot2OldTxList.index)
    # dfBurnBot2OldTxList = pd.DataFrame()
    dfBurnBot2TxList = acquireTXAdresse('df1qlwvtdrh4a4zln3k56rqnx8chu8t0sqx36syaea', dfBurnBot2OldTxList)
    dfBurnBot2TxList = dfBurnBot2OldTxList.append(dfBurnBot2TxList)
    dfBurnBot2TxList.sort_values(by=['height'], ascending=False, inplace=True)
    dfBurnBot2TxList.to_csv(filepathTxList2)
    print('   tx list burn bot 2 saved')


    ######### extract burned amount on hourly base #########
    filepathBurnAmount = path + 'dUSDBornBotAmounts.csv'
    dfBurnedAmount = pd.DataFrame()
    dfBurnedAmount['DUSDBurnBot_DFIAmount'] = dfBurnBotTxList['amounts_x'].groupby(pd.Grouper(freq='H')).sum()
    dfBurnedAmount['DUSDBurnBot_DUSDAmount'] = dfBurnBotTxList['amounts_y'].groupby(pd.Grouper(freq='H')).sum()
    dfBurnedAmount['DUSDBurnBot_SumDUSDAmount'] = dfBurnedAmount['DUSDBurnBot_DUSDAmount'].cumsum()

    dfBurnedAmount['DUSDBurnBot2_DFIAmount'] = dfBurnBot2TxList['amounts_x'].groupby(pd.Grouper(freq='H')).sum()
    dfBurnedAmount['DUSDBurnBot2_DUSDAmount'] = dfBurnBot2TxList['amounts_y'].groupby(pd.Grouper(freq='H')).sum()
    dfBurnedAmount['DUSDBurnBot2_DFIAmount'].fillna(value=0, inplace=True)
    dfBurnedAmount['DUSDBurnBot2_DUSDAmount'].fillna(value=0, inplace=True)
    dfBurnedAmount['DUSDBurnBot2_SumDUSDAmount'] = dfBurnedAmount['DUSDBurnBot2_DUSDAmount'].cumsum()

    dfBurnedAmount.index = dfBurnedAmount.index + np.timedelta64(1, 'h') # timeshift of 1h because Grouper is just using the hour information and removes minutes
    dfBurnedAmount.to_csv(filepathBurnAmount)

def getLOCKData():
    filepathSummary = path + 'LOCKData.csv'
    filepathComplete = path + 'LOCKAllOrdersData.csv'

    print('   start LOCK data acquisition')

    # API request for complete transaction list of DFX
    timeStampData = pd.Timestamp.now()-pd.Timedelta(days=1)
    fromDateAPI = timeStampData.strftime("%Y-%m-%d")
    link = 'https://api.lock.space/v1/analytics/staking/transactions?dateFrom='+fromDateAPI
    siteContent = requests.get(link)
    tempData = json.loads(siteContent.text)

    # load existing list of LOCK orders
    # dfLOCKorders = pd.DataFrame()
    dfLOCKorders = pd.read_csv(filepathComplete, index_col=0)
    dfLOCKorders.index = pd.to_datetime(dfLOCKorders.index)

    tempDataframe = pd.DataFrame(tempData['deposits'])
    tempDataframe['order'] = 'deposit'
    tempDataframe['date'] = pd.to_datetime(tempDataframe['date'])
    tempDataframe.set_index('date', inplace=True)
    index2Add = ~tempDataframe.index.isin(dfLOCKorders.index)
    dfLOCKorders = dfLOCKorders.append(tempDataframe[index2Add])

    tempDataframe = pd.DataFrame(tempData['withdrawals'])
    tempDataframe['order'] = 'withdrawal'
    tempDataframe['date'] = pd.to_datetime(tempDataframe['date'])
    tempDataframe.set_index('date', inplace=True)
    index2Add = ~tempDataframe.index.isin(dfLOCKorders.index)
    dfLOCKorders = dfLOCKorders.append(tempDataframe[index2Add])


    # get hourly data
    dfLOCKData = pd.DataFrame(columns=['DFIdepositsMNLOCK', 'DFIwithdrawalsMNLOCK','DFIdepositsYMLOCK', 'DFIwithdrawalsYMLOCK','DUSDdepositsYMLOCK', 'DUSDwithdrawalsYMLOCK'],
                              index=dfLOCKorders.amount.groupby(pd.Grouper(freq='H')).sum().index)
    dfLOCKData.index = dfLOCKorders.amount.groupby(pd.Grouper(freq='H')).sum().index
    dfLOCKData['DFIdepositsMNLOCK'] = dfLOCKorders[(dfLOCKorders.order == 'deposit') & (dfLOCKorders.asset == 'DFI') & (dfLOCKorders.stakingStrategy == 'Masternode')].amount.groupby(pd.Grouper(freq='H')).sum()
    dfLOCKData['DFIwithdrawalsMNLOCK'] = dfLOCKorders[(dfLOCKorders.order == 'withdrawal') & (dfLOCKorders.asset == 'DFI') & (dfLOCKorders.stakingStrategy == 'Masternode')].amount.groupby(pd.Grouper(freq='H')).sum()

    coinsYM = dfLOCKorders.asset.unique()
    for key in coinsYM:
        dfLOCKData[key+'depositsYMLOCK'] = dfLOCKorders[(dfLOCKorders.order == 'deposit') & (dfLOCKorders.asset == key) & (dfLOCKorders.stakingStrategy == 'LiquidityMining')].amount.groupby(pd.Grouper(freq='H')).sum()
        dfLOCKData[key+'withdrawalsYMLOCK'] = dfLOCKorders[(dfLOCKorders.order == 'withdrawal') & (dfLOCKorders.asset == key) & (dfLOCKorders.stakingStrategy == 'LiquidityMining')].amount.groupby(pd.Grouper(freq='H')).sum()

    dfLOCKData.fillna(0, inplace=True)
    dfLOCKData.index = dfLOCKData.index.strftime('%Y-%m-%d %H:%M')
    index2Add = ~tempDataframe.id.isin(dfLOCKorders.id)
    dfLOCKorders = dfLOCKorders.append(tempDataframe[index2Add])

    dfLOCKorders.sort_values(by='date', inplace=True)
    dfLOCKorders.to_csv(filepathComplete)



    # writing file
    dfLOCKData.to_csv(filepathSummary)

def getDFXData():
    filepathSummary = path + 'dfxData.csv'
    filepathComplete = path + 'dfxAllOrdersData.csv'

    print('   start DFX data acquisition')

    # API request for complete transaction list of DFX
    timeStampData = pd.Timestamp.now() - pd.Timedelta(days=2)
    fromDateAPI = timeStampData.strftime("%Y-%m-%d")
    link='https://api.dfx.swiss/v1/statistic/transactions?dateFrom='+fromDateAPI
    siteContent = requests.get(link)
    tempData= json.loads(siteContent.text)

    # load existing list of orders
    dfDFXorders = pd.read_csv(filepathComplete, index_col=0)
    dfDFXorders.index = pd.to_datetime(dfDFXorders.index)


    # get all new buy orders and add them to existing dataframe
    tempDataframe = pd.DataFrame(tempData['buy'])
    tempDataframe['order'] = 'buy'
    tempDataframe['date'] = pd.to_datetime(tempDataframe['date'])
    tempDataframe.set_index('date', inplace=True)
    index2Add = ~tempDataframe.index.isin(dfDFXorders.index)
    dfDFXorders = dfDFXorders.append(tempDataframe[index2Add])


    # get all new sell orders and add them to existing dataframe
    tempDataframe = pd.DataFrame(tempData['sell'])
    tempDataframe['order'] = 'sell'
    tempDataframe['date'] = pd.to_datetime(tempDataframe['date'])
    tempDataframe.set_index('date', inplace=True)
    index2Add = ~tempDataframe.index.isin(dfDFXorders.index)
    dfDFXorders = dfDFXorders.append(tempDataframe[index2Add])

    dfDFXorders.sort_values(by='date', inplace=True)
    dfDFXorders.to_csv(filepathComplete)


    # get hourly data
    dfDFXData = pd.DataFrame(columns=['dfxBuyVolume', 'dfxSellVolume'])
    dfDFXData['dfxBuyVolume'] = dfDFXorders[dfDFXorders.order == 'buy'].fiatAmount.groupby(pd.Grouper(freq='H')).sum()
    dfDFXData['dfxBuyVolume'] = dfDFXData['dfxBuyVolume'].fillna(0).cumsum()
    dfDFXData['dfxSellVolume'] = dfDFXorders[dfDFXorders.order == 'sell'].fiatAmount.groupby(pd.Grouper(freq='H')).sum()
    dfDFXData['dfxSellVolume'] = dfDFXData['dfxSellVolume'].fillna(0).cumsum()

    dfDFXData.index = dfDFXData.index.strftime('%Y-%m-%d %H:%M')
    # writing file
    dfDFXData.to_csv(filepathSummary)

def getQuantumLiquidity(timeStampData):
    # defichain side:
    # Cold: df1q9ctssszdr7taa8yt609v5fyyqundkxu0k4se9ry8lsgns8yxgfsqcsscmr
    # Hot: df1qgq0rjw09hr6vr7sny2m55hkr5qgze5l9hcm0lg
    #
    # Ethereum side,
    # 0x8D8cbEdf12F248Dfb0449BDD42Ce9d47deF092D0
    # hot would be the smart contract: 0x54346D39976629B65bA54EaC1C9Ef0af3be1921b

    filepath = path + 'QuantumLiquidityData.csv'
    newData = pd.Series(name=timeStampData, dtype=object,
                        index=['QuantumLiqu_Hot_ETH', 'QuantumLiqu_Hot_WBTC', 'QuantumLiqu_Hot_USDT', 'QuantumLiqu_Hot_USDC', 'QuantumLiqu_Hot_DFI', 'QuantumLiqu_Hot_EUROC',
                               'QuantumLiqu_Cold_ETH', 'QuantumLiqu_Cold_WBTC', 'QuantumLiqu_Cold_USDT', 'QuantumLiqu_Cold_USDC', 'QuantumLiqu_Cold_DFI', 'QuantumLiqu_Cold_EUROC',])

    #Ethereum holdings - hot wallet
    hotWalletAddress = '0x54346D39976629B65bA54EaC1C9Ef0af3be1921b'
    coldWalletAddress = '0x8D8cbEdf12F248Dfb0449BDD42Ce9d47deF092D0'

    contractWBTC = '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599'
    contractUSDT = '0xdac17f958d2ee523a2206206994597c13d831ec7'
    contractUSDC = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
    contractDFI = '0x8Fc8f8269ebca376D046Ce292dC7eaC40c8D358A'
    contractEUROC = '0x1aBaEA1f7C830bD89Acc67eC4af516284b1bC33c'

    # ETH holding - hot wallet
    link = 'https://api.etherscan.io/api?module=account' \
           '&action=balance' \
           '&address=' +hotWalletAddress+\
           '&tag=latest' \
           '&apikey=WZ8T48S9KDR1YWI8RJKT9PBRGB8GCU96AE'
    siteContent = requests.get(link)
    tempData = json.loads(siteContent.text)
    newData['QuantumLiqu_Hot_ETH'] = float(tempData['result']) * 1e-18

    # ETH holding - cold wallet
    link = 'https://api.etherscan.io/api?module=account' \
           '&action=balance' \
           '&address=' +coldWalletAddress+\
           '&tag=latest' \
           '&apikey=WZ8T48S9KDR1YWI8RJKT9PBRGB8GCU96AE'
    siteContent = requests.get(link)
    tempData = json.loads(siteContent.text)
    newData['QuantumLiqu_Cold_ETH'] = float(tempData['result']) * 1e-18


    availableToken = {'WBTC': contractWBTC, 'USDT': contractUSDT, 'USDC': contractUSDC, 'DFI':contractDFI, 'EUROC': contractEUROC}
    availableTokenFactor = {'WBTC': 1e-8, 'USDT': 1e-6, 'USDC': 1e-6, 'DFI': 1e-8, 'EUROC': 1e-6}
    for key in availableToken:
        # hot wallet holdings
        link = 'https://api.etherscan.io/api?module=account' \
               '&action=tokenbalance' \
               '&contractaddress='+availableToken.get(key)+ \
               '&address='+hotWalletAddress+ \
               '&tag=latest' \
               '&apikey=WZ8T48S9KDR1YWI8RJKT9PBRGB8GCU96AE'
        siteContent = requests.get(link)
        tempData = json.loads(siteContent.text)
        newData['QuantumLiqu_Hot_'+key] = float(tempData['result'])*availableTokenFactor.get(key)

        # cold wallet holdings
        link = 'https://api.etherscan.io/api?module=account' \
               '&action=tokenbalance' \
               '&contractaddress='+availableToken.get(key)+ \
               '&address='+coldWalletAddress+ \
               '&tag=latest' \
               '&apikey=WZ8T48S9KDR1YWI8RJKT9PBRGB8GCU96AE'
        siteContent = requests.get(link)
        tempData = json.loads(siteContent.text)
        newData['QuantumLiqu_Cold_'+key] = float(tempData['result'])*availableTokenFactor.get(key)

    dfQuantumLiquidity = pd.read_csv(filepath, index_col=0)
    #dfQuantumLiquidity = pd.DataFrame()
    dfQuantumLiquidity = dfQuantumLiquidity.append(newData, sort=False)
    dfQuantumLiquidity.to_csv(filepath)

    print('endOfFunction')


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

# Quantum bridge data
try:
    getQuantumLiquidity(timeStampData)
    print('Quantum bridge data saved')
except:
    print('### Error in Quantum bridge data acquisition')

# BSC bridge data
try:
    getBSCBridgeData()
    print('BSC bridge data saved')
except:
    print('### Error in BSC bridge data acquisition')

# dUSD Burn Bot data
try:
    getDUSDBurnBotData()
    print('dUSD Burn Bot data saved')
except:
    print('### Error in dUSD Burn Bot data acquisition')

# LOCK data
try:
    getLOCKData()
    print('LOCK data saved')
except:
    print('### Error in LOCK data acquisition')

# DFX data
try:
    getDFXData()
    print('DFX data saved')
except:
    print('### Error in DFX data acquisition')
