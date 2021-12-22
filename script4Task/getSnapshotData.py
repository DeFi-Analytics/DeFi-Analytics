import pandas as pd
import numpy as np

from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta

import requests
import ast
import time
import json

scriptPath = __file__
path = scriptPath[:-31] + '/data/'

filepath = path + 'snapshotData.csv'
filepathMNList = path + 'currentMNList.csv'
filePathVaults = path + 'vaultsData.csv'

while True:
    print('Start updating ...')
    now = datetime.now()

    # loading old snapshot data
    oldSnapshot = pd.read_csv(filepath, index_col=0)

    # Some data is only updated every 30 minutes
    if (now-pd.to_datetime(oldSnapshot['date'].values[0])) > timedelta(minutes=15):
        nowSnapshot = now
        bCorrectValues = True

        # get DFI richlist data
        print('... getting Richlist')
        link = "https://chainz.cryptoid.info/dfi/api.dws?q=allbalances&key=6ba465be70b4"
        cryptoIDContent = requests.get(link)
        apiCryptoIDAsDict = ast.literal_eval(cryptoIDContent.text)
        dfRichList = pd.DataFrame(data={'address': list(apiCryptoIDAsDict['balances'].keys()), 'balance':list(apiCryptoIDAsDict['balances'].values())}).sort_values(by=['balance'], ascending=False)
        dfRichList = dfRichList.drop(dfRichList[dfRichList.address.isin(['nulldata', 'op_return'])].index).reset_index(drop=True) # remove line with nulldata and op_return


        # special DFI addresses
        addFoundation = 'dJEbxbfufyPF14SC93yxiquECEfq4YSd9L'
        addFund = 'dZcHjYhKtEM88TtZLjp314H2xZjkztXtRc'
        addERC20 = 'dZFYejknFdHMHNfHMNQAtwihzvq7DkzV49'
        addBurn = '8defichainBurnAddressXXXXXXXdRQkSm'

        # condition for mn-addresses and private wallets
        try:
            print('... getting MN-List from mydeficha.in API')
            link = 'http://api.mydeficha.in/v1/listmasternodes/?state=ENABLED'
            siteContent = requests.get(link)
            dfMNList = pd.read_json(siteContent.text).transpose()
            dfMNList.to_csv(filepathMNList, index=True)
            condMN = (dfRichList['address'].isin(dfMNList.ownerAuthAddress)) & (dfRichList['address'].notnull())
            nbMNlocked5 = dfMNList[dfMNList.timelock == '5 years'].shape[0]
            nbMNlocked10 = dfMNList[dfMNList.timelock == '10 years'].shape[0]
        except:
            print('Error with API of masternode list')
            dfOldMNList = pd.read_csv(filepathMNList, index_col=0) # load available MN-List from the past
            condMN = (dfRichList['address'].isin(dfOldMNList.ownerAuthAddress)) & (dfRichList['address'].notnull())
            nbMNlocked5 = dfOldMNList[dfOldMNList.timelock == '5 years'].shape[0]
            nbMNlocked10 = dfOldMNList[dfOldMNList.timelock == '10 years'].shape[0]


        condPrivateAddress = (~condMN) & (dfRichList.address != addFund) & (dfRichList.address != addFoundation) & (dfRichList.address != addERC20) \
                                & (dfRichList.address != addBurn)


        # calc DFI Coin amounts
        nbMnId = dfRichList[condMN].balance.size
        nbOtherId = dfRichList[condPrivateAddress].balance.size


        if addFund in dfRichList.values:
            fundDFIValue = dfRichList[dfRichList.address == addFund].balance.values[0]
        mnDFIOverallValue = dfRichList[condMN].balance.sum()
        otherDFIValue = dfRichList[condPrivateAddress].balance.sum()
        if addERC20 in dfRichList.values:
            erc20DFIValue = dfRichList[dfRichList.address == addERC20].balance.values[0]
        else:
            erc20DFIValue = 0

        # calculate DFI locked and not locked
        mnDFIValue = mnDFIOverallValue - (nbMNlocked5 + nbMNlocked10)*20000
        mnDFILockedValue = (nbMNlocked5 + nbMNlocked10)*20000


        # get all burned DFI
        linkBurninfo = 'http://api.mydeficha.in/v1/getburninfo/'
        siteContent = requests.get(linkBurninfo)
        if siteContent.status_code==200:
            tempData = pd.read_json(siteContent.text).transpose()
            burnedDFIFees = tempData.loc['feeburn', 0]
            burnedDFIRewards = tempData.loc['emissionburn',0]
            burnedDFICoins = tempData.loc['amount',0]
        else:
            burnedDFIFees = np.NaN
            burnedDFIRewards = np.NaN
            burnedDFICoins = np.NaN

        burnedDFIValue = float(burnedDFICoins) + float(burnedDFIFees) + float(burnedDFIRewards)

        # get DFI from LiquidityMining and DFI-Token
        print('... getting LM and token data')
        try:
            link='http://api.defichain.io/v1/listpoolpairs?start=0&limit=500&network=mainnet&including_start=false'
            siteContent = requests.get(link, timeout=60)
            if siteContent.status_code == 200:
                dfLMPoolData = pd.read_json(siteContent.text).transpose()
                lmDFIValue = dfLMPoolData[dfLMPoolData.idTokenB=='0'].reserveB.astype('float').sum()
            else:
                lmDFIValue = oldSnapshot['lmDFI'].values[0]
        except:
            print('### error lm api ')
            lmDFIValue = oldSnapshot['lmDFI'].values[0]

        try:
            link = "https://api.defichain.io/v1/gettokenrichlist?id=0&network=mainnet"
            siteContent = requests.get(link, timeout=10)
            if siteContent.status_code == 200:
                dfDFIToken = pd.read_json(siteContent.text)
                tokenDFIValue = dfDFIToken[dfDFIToken.address != addFoundation].balance.sum()
            else:
                tokenDFIValue = oldSnapshot['tokenDFI'].values[0]
        except:
            print('### error token richlist')
            tokenDFIValue = oldSnapshot['tokenDFI'].values[0]

        # get DFI in vaults of last capture (time consumptive API)
        vaultsData = pd.read_csv(filePathVaults, index_col=0)
        vaultsDFIValue = vaultsData.sumDFI[vaultsData.sumDFI.notna()].iloc[-1]

        if addFoundation in dfRichList.values:
            foundationDFIValue = dfRichList[dfRichList.address==addFoundation].balance.values[0]
        else: # at the beginning there was no foundation address, should not be needed any longer
            foundationDFIValue = 0

        # calculated statistical data
        if np.isnan(tokenDFIValue):
            tokenDFIValue = 0
            bCorrectValues = False


        circDFIValue = mnDFIValue + otherDFIValue + lmDFIValue + tokenDFIValue + erc20DFIValue + vaultsDFIValue
        totalDFI = circDFIValue+foundationDFIValue+fundDFIValue+burnedDFIValue + mnDFILockedValue

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
        mnDFILockedValue = oldSnapshot['mnDFILocked'].values[0]
        otherDFIValue = oldSnapshot['otherDFI'].values[0]
        foundationDFIValue = oldSnapshot['foundationDFI'].values[0]
        lmDFIValue = oldSnapshot['lmDFI'].values[0]
        tokenDFIValue = oldSnapshot['tokenDFI'].values[0]
        erc20DFIValue = oldSnapshot['erc20DFI'].values[0]
        vaultsDFIValue = oldSnapshot['vaultsDFI'].values[0]
        burnedDFIValue = oldSnapshot['burnedDFI'].values[0]
        circDFIValue = oldSnapshot['circDFI'].values[0]
        totalDFI = oldSnapshot['totalDFI'].values[0]
        maxDFIValue = oldSnapshot['maxDFI'].values[0]
        currDFIPrice = oldSnapshot['DFIprice'].values[0]
        currDFI24hVol = oldSnapshot['tradingVolume'].values[0]
        marketCap = oldSnapshot['marketCap'].values[0]
        marketCapRank = oldSnapshot['marketCapRank'].values[0]
        bCorrectValues = oldSnapshot['bCorrectValues'].values[0]
        nbMNlocked5 = oldSnapshot['nbMNlocked5'].values[0]
        nbMNlocked10 = oldSnapshot['nbMNlocked10'].values[0]

    # countdown block data data
    print('... getting block data for countdown')
    # at the moment no countdown implemented
    blocksLeft = 0



    print('... saving data')
    # convert single data to pandas series
    colNames = ['date', 'nbMnId', 'nbOtherId', 'fundDFI',  'mnDFI', 'mnDFILocked', 'otherDFI', 'foundationDFI', 'lmDFI', 'tokenDFI', 'erc20DFI', 'burnedDFI', 'circDFI',
                'totalDFI', 'maxDFI', 'DFIprice', 'tradingVolume', 'marketCap', 'marketCapRank', 'blocksLeft', 'bCorrectValues', 'nbMNlocked5', 'nbMNlocked10', 'vaultsDFI']
    listData = [nowSnapshot, nbMnId, nbOtherId, fundDFIValue, mnDFIValue, mnDFILockedValue, otherDFIValue, foundationDFIValue, lmDFIValue, tokenDFIValue, erc20DFIValue, burnedDFIValue, circDFIValue,
                totalDFI, maxDFIValue, currDFIPrice, currDFI24hVol, marketCap, marketCapRank, blocksLeft, bCorrectValues, nbMNlocked5, nbMNlocked10, vaultsDFIValue]
    seriesData = pd.Series(listData, index = colNames)

    data2Save = pd.DataFrame(columns=colNames)
    data2Save = data2Save.append(seriesData, ignore_index=True)

    # saving data and wait for next run
    data2Save.to_csv(filepath, index=True)
    duration = datetime.now()-now
    print('Data updated. Routine duration: '+str(duration))
    print('  ')
    time.sleep(120-np.minimum(duration.seconds, 120))   # avoid negative numbers for sleep

print('Script finished')
























