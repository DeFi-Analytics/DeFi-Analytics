import pandas as pd
import numpy as np

from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta

import requests
import ast
import time

scriptPath = __file__
path = scriptPath[:-31] + '/data/'

filepath = path + 'snapshotData.csv'
filepathMNList = path + 'currentMNList.csv'

while True:
    print('Start updating ...')
    now = datetime.now()

    # loading old snapshot data
    oldSnapshot = pd.read_csv(filepath, index_col=0)

    if (now-pd.to_datetime(oldSnapshot['date'].values[0])) > timedelta(minutes=30):
        nowSnapshot = now
        # get DFI richlist data
        print('... getting Richlist')
        link = "http://mainnet-api.defichain.io/api/DFI/mainnet/address/stats/rich-list?pageno=1&pagesize=200000"
        siteContent = requests.get(link)
        text2extract = siteContent.text.replace('null','None')
        apiContentAsDict = ast.literal_eval(text2extract)
        dfRichList = pd.DataFrame(apiContentAsDict['data'])

        # convert fi balance into dfi balance
        dfRichList.balance = dfRichList.balance/100000000

        # special DFI addresses
        addFoundation = 'dJEbxbfufyPF14SC93yxiquECEfq4YSd9L'
        addFund = 'dZcHjYhKtEM88TtZLjp314H2xZjkztXtRc'

        # condition for mn-addresses and private wallets
        try:
            print('... getting MN-List')
            link = 'http://defichain-node.de/api/v1/listmasternodes/?state=ENABLED'
            siteContent = requests.get(link)
            dfMNList = pd.read_json(siteContent.text).transpose()
            dfMNList.to_csv(filepathMNList, index=True)
            condMN = (dfRichList['address'].isin(dfMNList.ownerAuthAddress)) & (dfRichList['address'].notnull())
        except:
            print('Error with API of masternode list')
            dfOldMNList = pd.read_csv(filepathMNList, index_col=0) # load available MN-List from the past
            condMN = (dfRichList['address'].isin(dfOldMNList.ownerAuthAddress)) & (dfRichList['address'].notnull())

        condPrivateAddress = (~condMN) & (dfRichList.address != addFund) & (dfRichList.address != addFoundation)

        # calc DFI Coin amounts
        nbMnId = dfRichList[condMN].balance.size
        nbOtherId = dfRichList[condPrivateAddress].balance.size
        if addFund in dfRichList.values:
            fundDFIValue = dfRichList[dfRichList.address == addFund].balance.values[0]
        mnDFIValue = dfRichList[condMN].balance.sum()
        otherDFIValue = dfRichList[condPrivateAddress].balance.sum()

        if addFoundation in dfRichList.values:
            foundationDFIValue = dfRichList[dfRichList.address==addFoundation].balance.values[0]
        else: # at the beginning there was no foundation address, should not be needed any longer
            foundationDFIValue = np.NaN


        # get DFI from LiquidityMining and DFI-Token
        print('... getting LM and token data')
        link='https://api.defichain.io/v1/listpoolpairs?start=0&limit=500&network=mainnet&including_start=false'
        siteContent = requests.get(link)
        dfLMPoolData = pd.read_json(siteContent.text).transpose()
        lmDFIValue = dfLMPoolData.reserveB.astype('float').sum()

        link = "https://api.defichain.io/v1/gettokenrichlist?id=0&network=mainnet"
        siteContent = requests.get(link)
        dfDFIToken = pd.read_json(siteContent.text)
        tokenDFIValue = dfDFIToken.balance.sum()

        # calculated statistical data
        totalDFI = mnDFIValue+otherDFIValue+foundationDFIValue+fundDFIValue+lmDFIValue+tokenDFIValue
        circDFIValue = mnDFIValue+otherDFIValue+lmDFIValue+tokenDFIValue
        maxDFIValue = 1200000000

        # get data from coingecko
        print('... getting coingecko data')
        try:
            cg = CoinGeckoAPI()
            DFIData = cg.get_price(ids='defichain', vs_currencies='usd', include_24hr_vol='true')
            currDFIPrice = DFIData['defichain']['usd']
            currDFI24hVol = DFIData['defichain']['usd_24h_vol']
            marketCapListCG = cg.get_coins_markets(vs_currency='usd', per_page=150)
            marketCapList = pd.DataFrame.from_dict(marketCapListCG)
            if (len(marketCapList) == 0):
                marketCapList = None
        except:
            currDFIPrice = np.NaN
            currDFI24hVol = np.NaN
            marketCapList = None
            print('############# Coingecko-API not reached #############')

        marketCap = currDFIPrice * circDFIValue
        # calculate marketcap rank
        if (np.isnan(marketCap)) | (marketCapList is None) | (circDFIValue < 0):
            marketCapRank = np.NaN
        else:
            marketCapRank = marketCapList[marketCapList.market_cap < marketCap].iloc[0].market_cap_rank
    else:
        print('... taking old snapshot data')
        nowSnapshot = oldSnapshot['date'].values[0]
        nbMnId = oldSnapshot['nbMnId'].values[0]
        nbOtherId = oldSnapshot['nbOtherId'].values[0]
        fundDFIValue = oldSnapshot['fundDFI'].values[0]
        mnDFIValue = oldSnapshot['mnDFI'].values[0]
        otherDFIValue = oldSnapshot['otherDFI'].values[0]
        foundationDFIValue = oldSnapshot['foundationDFI'].values[0]
        lmDFIValue = oldSnapshot['lmDFI'].values[0]
        tokenDFIValue = oldSnapshot['tokenDFI'].values[0]
        circDFIValue = oldSnapshot['circDFI'].values[0]
        totalDFI = oldSnapshot['totalDFI'].values[0]
        maxDFIValue = oldSnapshot['maxDFI'].values[0]
        currDFIPrice = oldSnapshot['DFIprice'].values[0]
        currDFI24hVol = oldSnapshot['tradingVolume'].values[0]
        marketCap = oldSnapshot['marketCap'].values[0]
        marketCapRank = oldSnapshot['marketCapRank'].values[0]

    # countdown block data data
    print('... getting block data for countdown')
    try:
        linkOverview = "https://api.defichain.io/v1/stats?"
        overviewContent = requests.get(linkOverview)
        apiOverviewAsDict = ast.literal_eval(overviewContent.text)
        reserveLM = float(apiOverviewAsDict['listCommunities']['IncentiveFunding'])

        linkAirdrop = 'https://api.defichain.io/v1/getaccount?start=0&limit=500&network=mainnet&including_start=true&owner=8UAhRuUFCyFUHEPD7qvtj8Zy2HxF5HH5nb'
        airdropContent = requests.get(linkAirdrop)
        dfAirdrop = pd.read_json(airdropContent.text, typ='series')
        airdropDFI = float(dfAirdrop[0][:-4])

        currentBlock = apiOverviewAsDict['blockHeight']
        goalBlock = int(currentBlock + np.floor((reserveLM + airdropDFI) / 58))
    except:
        currentBlock = 0
        goalBlock = 0
        print('############# Error getting current block #############')
    blocksLeft = goalBlock - currentBlock



    print('... saving data')
    # convert single data to pandas series
    colNames = ['date', 'nbMnId', 'nbOtherId', 'fundDFI',  'mnDFI', 'otherDFI', 'foundationDFI', 'lmDFI', 'tokenDFI', 'circDFI', 'totalDFI', 'maxDFI', 'DFIprice', 'tradingVolume', 'marketCap', 'marketCapRank', 'blocksLeft']
    listData = [nowSnapshot, nbMnId, nbOtherId, fundDFIValue, mnDFIValue, otherDFIValue, foundationDFIValue, lmDFIValue, tokenDFIValue, circDFIValue, totalDFI, maxDFIValue, currDFIPrice, currDFI24hVol, marketCap, marketCapRank, blocksLeft]
    seriesData = pd.Series(listData, index = colNames)

    data2Save = pd.DataFrame(columns=colNames)
    data2Save = data2Save.append(seriesData, ignore_index=True)

    # saving data and wait for next run
    data2Save.to_csv(filepath, index=True)
    duration = datetime.now()-now
    print('Data updated. Routine duration: '+str(duration))
    print('  ')
    time.sleep(120-duration.seconds)

print('Script finished')
























