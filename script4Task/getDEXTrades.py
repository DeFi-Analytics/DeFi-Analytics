import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime
import time

# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-28] + '/data/'

filepathCoinPrices = path + 'coinPriceList.csv'
filepathTradingResults = path + 'dailyTradingResultsDEX.csv'


availablePools = {'ETH':4,'BTC':5,'USDT':6,'DOGE':8,'LTC':10,'BCH':12,'USDC':14}
availablePools = {'BTC':5,'USDT':6,'DOGE':8,'LTC':10,'BCH':12,'USDC':14}
dfTradeResult = pd.DataFrame()

for key in availablePools:
    print('Getting swaps of pool: ' + key)
    dfSwaplist = pd.DataFrame()

    newData = True
    nextPage = ''
    while newData:
        linkSwaps = 'https://ocean.defichain.com/v0/mainnet/poolpairs/' + str(availablePools.get(key)) + '/swaps/verbose'+nextPage
        siteContent = requests.get(linkSwaps)
        while siteContent.status_code == 500:
            print('Retry API Call')
            time.sleep(2)
            siteContent = requests.get(linkSwaps)



        tempData = json.loads(siteContent.text)

        # check if another page must be requested
        if 'page' in tempData:
            nextPage = '?next=' + tempData['page']['next']
        else:
            newData = False

        tempDataframe = pd.DataFrame(tempData['data'])
        tempDataframe['Time'] = [datetime.utcfromtimestamp(element.get('medianTime')).strftime('%Y-%m-%d %H:%M:%S')  for element in tempDataframe['block'] ]
        tempDataframe['blockNb'] = [element.get('medianTime') for element in tempDataframe['block'] ]
        tempDataframe['fromSymbol'] = [element.get('symbol') for element in tempDataframe['from']]
        tempDataframe['toAmount'] = [element.get('amount') if element is not np.nan else np.nan for element in tempDataframe['to']]
        tempDataframe['toSymbol'] = [element.get('symbol') if element is not np.nan else np.nan for element in tempDataframe['to']]
        tempDataframe.drop(['id', 'sort', 'fromTokenId', 'block', 'from', 'to'], axis=1, inplace=True)
        tempDataframe.set_index('txid', inplace=True)

        listNewSwaps = tempDataframe.index.difference(dfSwaplist.index)
        listOldSwaps = tempDataframe.index.intersection(dfSwaplist.index)
        tempDataframe.loc[listNewSwaps]
        newData = listOldSwaps.empty
        print(nextPage + ' ' + str(newData))
        dfSwaplist = dfSwaplist.append(tempDataframe.loc[listNewSwaps], verify_integrity=True)

    #     # evaluate the data inside the vaults
    #     for item in tempData['data']:
    #         vaultData['nbVaults'] += 1
    #         if item['state'] == 'ACTIVE':
    #             vaultData['nbLoans'] += len(item['loanAmounts'])
    #             vaultData[item['loanScheme']['id']] += 1
    #             vaultData['sumInterest'] += float(item['interestValue'])
    #             for coinsCollateral in item['collateralAmounts']:
    #                 vaultData['sum'+coinsCollateral['symbol']] += float(coinsCollateral['amount'])
    #             for coinsMinted in item['loanAmounts']:
    #                 vaultData['sumLoan'+coinsMinted['symbol']] += float(coinsMinted['amount'])
    #
    #         elif item['state'] == 'IN_LIQUIDATION':
    #             for batches in item['batches']:
    #                 vaultData['sumLoanLiquidation'+batches['loan']['symbol']] += float(batches['loan']['amount'])
    #             vaultData['nbLiquidation'] += 1
    #
    #     vaultData.name = pd.Timestamp.now()
    #
    # # save file
    # # dfOldVaultData = pd.DataFrame()
    # dfOldVaultData = pd.read_csv(filepath, index_col=0)
    # dfVaultData = dfOldVaultData.append(vaultData, sort=False)
    # dfVaultData.to_csv(filepath)


# get all swaps over all pools
for key in availablePools: 
    print('Checking trades of pool: ' + key)
    linkTrade = 'https://api.defichain.io/v1/getswaptransaction?id='+str(availablePools.get(key))+'&network=mainnet&skip=0&limit=1000000'
    siteContent = requests.get(linkTrade)
    dfJSON = pd.read_json(siteContent.text,orient='columns')
    nbTradesDEX = dfJSON['total'].max()
    
    dfTrades = pd.DataFrame(dfJSON.data.tolist())
    dfTrades['Date'] = pd.to_datetime(dfTrades['blockTime'],utc=True).dt.strftime('%Y-%m-%d')
    
    availableBaseToken = dfTrades.baseTokenSymbol.unique()
    dfTradeResult[key+'pool_nbTrades'] = dfTrades.groupby('Date')['_id'].count()
    dfTradeResult[key+'pool_base'+availableBaseToken[0]] = dfTrades.loc[dfTrades.baseTokenSymbol==availableBaseToken[0]].groupby('Date')['baseTokenAmount'].sum()
    dfTradeResult[key+'pool_quote'+availableBaseToken[0]] = dfTrades.loc[dfTrades.quoteTokenSymbol==availableBaseToken[0]].groupby('Date')['quoteTokenAmount'].sum()
    dfTradeResult[key+'pool_base'+availableBaseToken[1]] = dfTrades.loc[dfTrades.baseTokenSymbol==availableBaseToken[1]].groupby('Date')['baseTokenAmount'].sum()
    dfTradeResult[key+'pool_quote'+availableBaseToken[1]] = dfTrades.loc[dfTrades.quoteTokenSymbol==availableBaseToken[1]].groupby('Date')['quoteTokenAmount'].sum()


# add usd price information for all coins
# dfCoinPrices = pd.read_csv(filepathCoinPrices,index_col=0)
# dfTradeResult = dfTradeResult.iloc[:-1].merge(dfCoinPrices[['DFIPriceUSD','BTCPriceUSD','ETHPriceUSD','USDTPriceUSD','DOGEPriceUSD','LTCPriceUSD','BCHPriceUSD','USDCPriceUSD']],
#                                     how='outer',left_index=True, right_index=True)

# calculate trading volume in USD for each base coin and sum of pool
print('Calculating USD trading volume')
for key in availablePools: 
    dfTradeResult[key+'pool_base'+key+'_inUSD'] = dfTradeResult[key+'pool_base'+key]*dfTradeResult[key+'PriceUSD']
    dfTradeResult[key+'pool_baseDFI_inUSD'] = dfTradeResult[key+'pool_baseDFI']*dfTradeResult['DFIPriceUSD']
    dfTradeResult[key+'pool_sum_inUSD'] = dfTradeResult[key+'pool_base'+key+'_inUSD']+dfTradeResult[key+'pool_baseDFI_inUSD']

dfTradeResult.to_csv(filepathTradingResults)