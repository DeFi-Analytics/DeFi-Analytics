import os
import glob
import pathlib
import re
import base64

import pandas as pd

from datetime import datetime, timedelta

# https://www.pythonanywhere.com/forums/topic/29390/        for measuring the RAM usage on pythonanywhere

class defichainAnalyticsModelClass:
    def __init__(self):
        workDir = os.path.abspath(os.getcwd())
        self.dataPath = workDir[:-9] + '/data/'

        # data for controller/views
        self.dailyData = pd.DataFrame()
        self.hourlyData = pd.DataFrame()
        self.minutelyData = pd.DataFrame()
        self.lastRichlist = None
        self.snapshotData = None
        self.changelogData = None

        # last update of csv-files
        self.updated_nodehubIO = None
        self.updated_allnodes = None
        self.updated_extractedRichlist = None
        self.updated_tradingData = None
        self.updated_blocktime = None
        self.updated_dexHourly = None
        self.update_dexMinutely = None
        self.updated_daa = None
        self.updated_LastRichlist = None
        self.updated_dexVolume = None
        self.updated_tokenCryptos = None
        self.updated_twitterData = None
        self.updated_twitterFollower = None
        self.update_snapshotData = None
        self.update_changelogData = None
        self.update_incomeVisits = None
        self.update_portfolioDownloads = None
        self.update_promoDatabase = None
        self.update_analyticsVisits = None
        self.updated_hourlyDEXTrades = None

        # background image for figures
        with open(workDir + "/assets/analyticsLandscapeGrey2.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        self.figBackgroundImage = "data:image/png;base64," + encoded_string         # Add the prefix that plotly will want when using the string as source

    #### DAILY DATA #####
    def loadDailyData(self):
        self.loadHourlyDEXdata()
        self.loadDEXVolume()
        self.loadDailyTradingData()
        self.loadExtractedRichlistData()
        self.loadDailyBlocktimeData()
        self.loadDAAData()
        self.loadTwitterData()
        self.loadTwitterFollowerData()
        self.loadIncomeVisitsData()
        self.loadPortfolioDownloads()
        self.loadPromoDatabase()
        self.loadMNMonitorDatabase()
        self.loadAnalyticsVisitsData()

    def loadMNnodehub(self):
        print('>>>> Start update nodehub.IO data ...  <<<<')
        filePath = self.dataPath + 'mnNodehub.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_nodehubIO:
            nodehubData = pd.read_csv(filePath, index_col=0)
            nodehubData.rename(columns={"amount": "nbMNNodehub"}, inplace=True)

            ind2Delete = self.dailyData.columns.intersection(nodehubData.columns)
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                        # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(nodehubData['nbMNNodehub'], how='outer', left_index=True, right_index=True)

            self.updated_nodehubIO = fileInfo.stat()
            print('>>>> nodehub data loaded from csv-file <<<<')

    def loadMNAllnodes(self):
        print('>>>> Start update allnodes data ...  <<<<')
        filePath = self.dataPath + 'mnAllnodes.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_allnodes:
            allnodesData = pd.read_csv(filePath, index_col=0)
            allnodesData.set_index('date', inplace=True)

            ind2Delete = self.dailyData.columns.intersection(allnodesData.columns)
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                        # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(allnodesData['nbMNAllnode'], how='outer', left_index=True, right_index=True)

            self.updated_allnodes = fileInfo.stat()
            print('>>>> allnodes data loaded from csv-file <<<<')

    def loadExtractedRichlistData(self):
        self.loadMNnodehub()  # number masternode hosted by nodehub must be load here to ensure correct values for other and relative representation
        self.loadMNAllnodes()  # number masternode hosted by Allnodes must be load here to ensure correct values for other and relative representation
        print('>>>> Start update extracted richlist data ...  <<<<')
        filePath = self.dataPath + 'extractedDFIdata.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_extractedRichlist:
            extractedRichlist = pd.read_csv(filePath, index_col=0)

            ind2Delete = self.dailyData.columns.intersection(extractedRichlist.columns)                                 # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(extractedRichlist, how='outer', left_index=True, right_index=True)      # add new columns to daily table

            self.dailyData['nbMNOther'] = self.dailyData['nbMnId']-self.dailyData['nbMnCakeId']-self.dailyData['nbMydefichainId']\
                                          -self.dailyData['nbMNNodehub'].fillna(0)-self.dailyData['nbMNAllnode'].fillna(0)
            self.dailyData['nbMNnonCake'] = self.dailyData['nbMnId']-self.dailyData['nbMnCakeId']

            self.dailyData['nbMnCakeIdRelative'] = self.dailyData['nbMnCakeId']/self.dailyData['nbMnId']*100
            self.dailyData['nbMNOtherRelative'] = self.dailyData['nbMNOther'] / self.dailyData['nbMnId'] * 100
            self.dailyData['nbMydefichainRelative'] = self.dailyData['nbMydefichainId'] / self.dailyData['nbMnId'] * 100
            self.dailyData['nbMNNodehubRelative'] = self.dailyData['nbMNNodehub'] / self.dailyData['nbMnId'] * 100
            self.dailyData['nbMNAllnodeRelative'] = self.dailyData['nbMNAllnode'] / self.dailyData['nbMnId'] * 100

            # extracting DFI in Liquidity-Mining
            lmCoins = pd.DataFrame(index=self.dailyData.index)
            lmCoins['BTC_pool'] = self.hourlyData.groupby('Date')['BTC-DFI_reserveB'].first()
            lmCoins['ETH_pool'] = self.hourlyData.groupby('Date')['ETH-DFI_reserveB'].first()
            lmCoins['USDT_pool'] = self.hourlyData.groupby('Date')['USDT-DFI_reserveB'].first()
            lmCoins['DOGE_pool'] = self.hourlyData.groupby('Date')['DOGE-DFI_reserveB'].first()
            lmCoins['LTC_pool'] = self.hourlyData.groupby('Date')['LTC-DFI_reserveB'].first()
            lmCoins['USDC_pool'] = self.hourlyData.groupby('Date')['USDC-DFI_reserveB'].first()
            lmCoins['overall'] = lmCoins['BTC_pool'] + lmCoins['ETH_pool'] + lmCoins['USDT_pool'] + lmCoins['DOGE_pool'].fillna(0) + lmCoins['LTC_pool'].fillna(0) + lmCoins['USDC_pool'] .fillna(0)
            self.dailyData['lmDFI'] = lmCoins['overall']

            # sum of addresses and DFI
            self.dailyData['nbOverall'] = self.dailyData['nbMnId'] + self.dailyData['nbOtherId']
            self.dailyData['circDFI'] = self.dailyData['mnDFI'] + self.dailyData['otherDFI'] + self.dailyData['tokenDFI'].fillna(0) + self.dailyData['lmDFI'].fillna(0) + self.dailyData['erc20DFI'].fillna(0)
            self.dailyData['totalDFI'] = self.dailyData['circDFI'] + self.dailyData['fundDFI'] + self.dailyData['foundationDFI'].fillna(0) + self.dailyData['burnedDFI'].fillna(method="ffill")

            # calc market cap data in USD and BTC
            print('>>>>>>>> Update market cap in loadExtractedRichlistData...  <<<<<<<<')
            self.dailyData['marketCapUSD'] = self.dailyData['circDFI']*self.dailyData['DFIPriceUSD']
            self.dailyData['marketCapBTC'] = self.dailyData['marketCapUSD'] / self.dailyData['BTCPriceUSD']

            # calculate daily change in addresses and DFI amount
            self.dailyData['diffDate'] = pd.to_datetime(self.dailyData.index).to_series().diff().values
            self.dailyData['diffDate'] = self.dailyData['diffDate'].fillna(pd.Timedelta(seconds=0))  # set nan-entry to timedelta 0
            self.dailyData['diffDate'] = self.dailyData['diffDate'].apply(lambda x: float(x.days))

            self.dailyData['diffNbOther'] = self.dailyData['nbOtherId'].diff() / self.dailyData['diffDate']
            self.dailyData['diffNbMN'] = self.dailyData['nbMnId'].diff() / self.dailyData['diffDate']
            self.dailyData['diffNbNone'] = None

            self.dailyData['diffotherDFI'] = self.dailyData['otherDFI'].diff() / self.dailyData['diffDate']
            self.dailyData['diffmnDFI'] = self.dailyData['mnDFI'].diff() / self.dailyData['diffDate']
            self.dailyData['difffundDFI'] = self.dailyData['fundDFI'].diff() / self.dailyData['diffDate']
            self.dailyData['difffoundationDFI'] = self.dailyData['foundationDFI'].diff() / self.dailyData['diffDate']
            self.dailyData['diffLMDFI'] = self.dailyData['lmDFI'].diff() / self.dailyData['diffDate']


            self.updated_extractedRichlist = fileInfo.stat()
            print('>>>> Richlist data loaded from csv-file <<<<')

    def loadDailyTradingData(self):
        print('>>>> Start update trading data ...  <<<<')
        filePath = self.dataPath + 'dailyTradingResultsDEX.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_tradingData:
            dailyTradingResults = pd.read_csv(self.dataPath+'dailyTradingResultsDEX.csv',index_col=0)

            ind2Delete = self.dailyData.columns.intersection(dailyTradingResults.columns)                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(dailyTradingResults, how='outer', left_index=True, right_index=True)    # add new columns to daily table

            # calc market cap data in USD and BTC (same as in loadExtractedRichlistData to get updated price information
            if 'circDFI' in self.dailyData.columns:
                print('>>>>>>>> Update market cap in loadDailyTradingData...  <<<<<<<<')
                self.dailyData['marketCapUSD'] = self.dailyData['circDFI']*self.dailyData['DFIPriceUSD']
                self.dailyData['marketCapBTC'] = self.dailyData['marketCapUSD'] / self.dailyData['BTCPriceUSD']

            self.updated_tradingData = fileInfo.stat()
            print('>>>> Trading data loaded from csv-file <<<<')

    def loadDailyBlocktimeData(self):
        print('>>>> Start update blocktime data ... <<<<')
        filePath = self.dataPath + 'BlockListStatistics.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_blocktime:
            dailyBlocktimeData = pd.read_csv(filePath, index_col=0)
            dailyBlocktimeData['tps'] = dailyBlocktimeData['txCount'] / (24 * 60 * 60)

            ind2Delete = self.dailyData.columns.intersection(dailyBlocktimeData.columns)                                # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(dailyBlocktimeData, how='outer', left_index=True,right_index=True)    # add new columns to daily table

            self.updated_blocktime = fileInfo.stat()
            print('>>>> Blocktime data loaded from csv-file <<<<')

    def loadDAAData(self):
        print('>>>> Start update DAA data ... <<<<')
        filePath = self.dataPath + 'analyzedDataDAA.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_daa:
            dailyDAAData = pd.read_csv(filePath, index_col=0)

            ind2Delete = self.dailyData.columns.intersection(dailyDAAData.columns)                                          # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                           # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(dailyDAAData, how='outer', left_index=True, right_on='Date')              # add new columns to daily table
            self.dailyData.set_index('Date', inplace=True)
            self.dailyData.sort_index(inplace=True)

            self.updated_daa = fileInfo.stat()
            print('>>>> DAA data loaded from csv-file <<<<')

    def loadTwitterData(self):
        print('>>>> Start update twitter data ... <<<<')
        filePath = self.dataPath + 'analyzedTwitterData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_twitterData:
            twitterData = pd.read_csv(filePath, index_col=0)

            columns2update = ['overall_Activity', 'defichain_Activity', 'dfi_Activity', 'overall_Likes', 'overall_UniqueUserOverall', 'overall_UniqueUserTweet', 'overall_UniqueUserReply', 'overall_UniqueUserRetweet']

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(twitterData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.updated_twitterData = fileInfo.stat()
            print('>>>> Twitter data loaded from csv-file <<<<')

    def loadTwitterFollowerData(self):
        print('>>>> Start update twitter follower data ... <<<<')
        filePath = self.dataPath + 'TwitterData_follower.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_twitterFollower:
            twitterFollowData = pd.read_csv(filePath, index_col=0)
            twitterFollowData.set_index('Date',inplace=True)
            columns2update = ['Follower', 'followedToday', 'unfollowedToday']

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(twitterFollowData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.updated_twitterFollower = fileInfo.stat()
            print('>>>> Twitter data loaded from csv-file <<<<')

    def loadIncomeVisitsData(self):
        print('>>>> Start update income visits data ... <<<<')
        filePath = self.dataPath + 'dataVisitsIncome.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_incomeVisits:
            incomeVisitsData = pd.read_csv(filePath, index_col=0)
            incomeVisitsData.rename(columns={'0': 'incomeVisits'}, inplace=True)
            incomeVisitsData.set_index(incomeVisitsData.index.str[:10], inplace=True)   # just use date information without hh:mm
            columns2update = ['incomeVisits']

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(incomeVisitsData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.update_incomeVisits = fileInfo.stat()
            print('>>>> Income visits data loaded from csv-file <<<<')

    def loadPortfolioDownloads(self):
        print('>>>> Start update portfolio downloads data ... <<<<')
        filePath = self.dataPath + 'dataPortfolioDownloads.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_portfolioDownloads:
            portfolioRawData = pd.read_csv(filePath)

            columns2update = ['PortfolioWindows', 'PortfolioMac', 'PortfolioLinux']
            dfPortfolioData = pd.DataFrame(index=portfolioRawData['DateCaptured'].unique(), columns=columns2update)

            dfPortfolioData['PortfolioWindows'] = portfolioRawData.groupby(portfolioRawData.DateCaptured).Windows.sum()
            dfPortfolioData['PortfolioMac'] = portfolioRawData.groupby(portfolioRawData.DateCaptured).Mac.sum()
            dfPortfolioData['PortfolioLinux'] = portfolioRawData.groupby(portfolioRawData.DateCaptured).Linux.sum()

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(dfPortfolioData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.update_portfolioDownloads = fileInfo.stat()
            print('>>>> Portfolio downloads data loaded from csv-file <<<<')

    def loadPromoDatabase(self):
        print('>>>> Start update DefiChain promo database ... <<<<')
        filePath = self.dataPath + 'defichainPromoData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_promoDatabase:
            promoRawData = pd.read_csv(filePath, index_col=0)

            columns2update = ['postActive', 'mediaActive', 'incentivePointsToday', 'incentiveUsers']

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(promoRawData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.update_promoDatabase = fileInfo.stat()
            print('>>>> DefiChain promo database loaded from csv-file <<<<')

    def loadMNMonitorDatabase(self):
        print('>>>> Start update masternode monitor database ... <<<<')
        filePath = self.dataPath + 'masternodeMonitorData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_promoDatabase:
            monitorRawData = pd.read_csv(filePath, index_col=0)

            columns2update = ['nbMasternodes', 'nbAccounts']

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(monitorRawData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.update_promoDatabase = fileInfo.stat()
            print('>>>> MN Monitor database loaded from csv-file <<<<')

    def loadAnalyticsVisitsData(self):
        print('>>>> Start update raw data analytics visits ... <<<<')
        filePath = self.dataPath + 'rawDataUserVisit.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_analyticsVisits:
            analyticsRawVisitsData = pd.read_csv(filePath, index_col=0)
            analyticsRawVisitsData['visitDate'] = pd.to_datetime(analyticsRawVisitsData.visitTimestamp).dt.date

            analyticsVisitData = analyticsRawVisitsData.groupby('visitDate').count()
            analyticsVisitData.rename(columns={'visitTimestamp': 'analyticsVisits'}, inplace=True)
            columns2update = ['analyticsVisits']
            analyticsVisitData.index = analyticsVisitData.index.map(str)    # change index from dt to str format

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(analyticsVisitData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.update_analyticsVisits = fileInfo.stat()
            print('>>>> Analytics visits data loaded from csv-file <<<<')


    #### HOURLY DATA ####
    def loadHourlyData(self):
        self.loadHourlyDEXdata()
        self.loadDEXVolume()
        self.loadTokenCrypto()
        self.loadHourlyDEXTrades()


    def loadHourlyDEXdata(self):
        print('>>>> Start update hourly DEX data ... <<<<')
        filePath = self.dataPath + 'LMPoolData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_dexHourly:
            hourlyDEXData = pd.read_csv(filePath, index_col=0)
            hourlyDEXData['timeRounded'] = pd.to_datetime(hourlyDEXData.Time).dt.floor('H')
            hourlyDEXData.set_index(['timeRounded'], inplace=True)
            hourlyDEXData['reserveA_DFI'] = hourlyDEXData['reserveA'] / hourlyDEXData['DFIPrices']

            for poolSymbol in hourlyDEXData.symbol.dropna().unique():
                df2Add = hourlyDEXData[hourlyDEXData.symbol == poolSymbol]
                df2Add = df2Add.drop(columns=['Time', 'symbol'])

                # calculate locked DFI and corresponding values
                df2Add = df2Add.assign(lockedDFI=df2Add['reserveB'] + df2Add['reserveA_DFI'])
                df2Add = df2Add.assign(lockedUSD=df2Add['lockedDFI']*hourlyDEXData[hourlyDEXData.symbol == 'USDT-DFI'].DFIPrices)
                df2Add = df2Add.assign(lockedBTC=df2Add['lockedDFI'] * hourlyDEXData[hourlyDEXData.symbol == 'BTC-DFI'].DFIPrices)

                # calculate relative price deviations
                df2Add = df2Add.assign(relPriceDevCoingecko=((df2Add['DFIPrices'] - df2Add['reserveA/reserveB'])/df2Add['DFIPrices']))
                df2Add = df2Add.assign(relPriceDevBittrex=((df2Add['DFIPricesBittrex'] - df2Add['reserveA/reserveB']) / df2Add['DFIPricesBittrex']))

                # add prefix to column names for pool identification
                colNamesOrig = df2Add.columns.astype(str)
                colNamesNew = poolSymbol+'_' + colNamesOrig
                df2Add = df2Add.rename(columns=dict(zip(colNamesOrig, colNamesNew)))

                # delete existing information and add new one
                ind2Delete = self.hourlyData.columns.intersection(colNamesNew)                                          # check if columns exist
                self.hourlyData.drop(columns=ind2Delete, inplace=True)                                                          # delete existing columns to add new ones
                self.hourlyData = self.hourlyData.merge(df2Add, how='outer', left_index=True, right_index=True)           # add new columns to daily table

            self.hourlyData['Date'] = pd.to_datetime(self.hourlyData.index).strftime('%Y-%m-%d')
            self.updated_dexHourly = fileInfo.stat()
            print('>>>> Hourly DEX data loaded from csv-file <<<<')

    def loadDEXVolume(self):
        print('>>>> Start update DEX volume data ... <<<<')
        filePath = self.dataPath + 'DEXVolumeData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_dexVolume:
            volumeData = pd.read_csv(filePath, index_col=0)
            volumeData['timeRounded'] = pd.to_datetime(volumeData.Time).dt.floor('H')
            volumeData.set_index(['timeRounded'], inplace=True)

            for poolSymbol in volumeData['base_name'].unique():
                df2Add = volumeData[volumeData['base_name']==poolSymbol][['base_volume', 'quote_volume']]
                df2Add['VolTotal'] = df2Add[['base_volume', 'quote_volume']].sum(axis=1)
                # add prefix to column names for pool identification
                colNamesOrig = df2Add.columns.astype(str)
                colNamesNew = poolSymbol + '_' + colNamesOrig
                df2Add = df2Add.rename(columns=dict(zip(colNamesOrig, colNamesNew)))

                # delete existing information and add new one
                ind2Delete = self.hourlyData.columns.intersection(colNamesNew)                                          # check if columns exist
                self.hourlyData.drop(columns=ind2Delete, inplace=True)                                                          # delete existing columns to add new ones
                self.hourlyData = self.hourlyData.merge(df2Add, how='outer', left_index=True, right_index=True)           # add new columns to daily table

            # calculate total volume after merge of data
            self.hourlyData['VolTotal'] = self.hourlyData['BTC_VolTotal']*0   # only use rows with data; BTC was the first pool and have to most data (beside ETH, USDT)
            for poolSymbol in volumeData['base_name'].unique():
                self.hourlyData['VolTotal'] = self.hourlyData['VolTotal'] + self.hourlyData[poolSymbol+'_'+'VolTotal'].fillna(0)

            self.hourlyData['VolTotalCoingecko'] = volumeData[volumeData['base_name']=='BTC']['coingeckoVolume']
            self.updated_dexVolume = fileInfo.stat()
            print('>>>> DEX volume data loaded from csv-file <<<<')

    def loadHourlyDEXTrades(self):
        print('>>>> Start update hourly DEX trade data ... <<<<')
        filePath = self.dataPath + 'hourlyDEXTrades.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_hourlyDEXTrades:
            hourlyTrades = pd.read_csv(filePath, index_col=0)
            hourlyTrades.fillna(0, inplace=True)
            hourlyTrades.index = pd.to_datetime(hourlyTrades.index).tz_localize(None)

            columns2update = []
            currName = ['BTC', 'ETH', 'USDT', 'DOGE', 'LTC', 'BCH', 'USDC', 'DFI']
            for ind in range(7):
                hourlyTrades['volume'+currName[ind]+'buyDFI'] = hourlyTrades[currName[ind]+'pool_base'+currName[ind]] * hourlyTrades[currName[ind]+'-USD']
                hourlyTrades['volume'+currName[ind]+'sellDFI'] = hourlyTrades[currName[ind]+'pool_quote'+currName[ind]] * hourlyTrades[currName[ind]+'-USD']
                columns2update.extend(['volume'+currName[ind]+'buyDFI', 'volume'+currName[ind]+'sellDFI'])

            hourlyTrades['volumeOverallbuyDFI'] = hourlyTrades['volumeBTCbuyDFI']+hourlyTrades['volumeETHbuyDFI']+hourlyTrades['volumeUSDTbuyDFI'] + \
                                                    hourlyTrades['volumeDOGEbuyDFI']+hourlyTrades['volumeLTCbuyDFI']+hourlyTrades['volumeBCHbuyDFI'] + \
                                                    hourlyTrades['volumeUSDCbuyDFI']
            hourlyTrades['volumeOverallsellDFI'] = hourlyTrades['volumeBTCsellDFI']+hourlyTrades['volumeETHsellDFI']+hourlyTrades['volumeUSDTsellDFI'] + \
                                                    hourlyTrades['volumeDOGEsellDFI']+hourlyTrades['volumeLTCsellDFI']+hourlyTrades['volumeBCHsellDFI'] + \
                                                    hourlyTrades['volumeUSDCsellDFI']
            columns2update.extend(['volumeOverallbuyDFI', 'volumeOverallsellDFI'])

            ind2Delete = self.hourlyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.hourlyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.hourlyData = self.hourlyData.merge(hourlyTrades[columns2update], how='outer', left_index=True, right_index=True)                                                                   # delete existing columns to add new ones


            self.updated_hourlyDEXTrades = fileInfo.stat()
            print('>>>> DEX volume data loaded from csv-file <<<<')

    def loadTokenCrypto(self):
        print('>>>> Start update token data ... <<<<')
        filePath = self.dataPath + 'TokenData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_tokenCryptos:
            tokenData = pd.read_csv(filePath, index_col=0)
            tokenData['timeRounded'] = pd.to_datetime(tokenData.Time).dt.floor('H')
            tokenData.set_index(['timeRounded'], inplace=True)

            for coinSymbol in tokenData['symbol'].unique():
                df2Add = tokenData[tokenData['symbol']==coinSymbol][['Burned', 'minted', 'Collateral']]
                df2Add['tokenDefiChain'] = df2Add['minted'] - df2Add['Burned'].fillna(0)
                df2Add['diffToken'] = df2Add['Collateral']-df2Add['minted']+df2Add['Burned'].fillna(0)

                # add prefix to column names for pool identification
                colNamesOrig = df2Add.columns.astype(str)
                colNamesNew = coinSymbol + '_' + colNamesOrig
                df2Add = df2Add.rename(columns=dict(zip(colNamesOrig, colNamesNew)))

                # delete existing information and add new one
                ind2Delete = self.hourlyData.columns.intersection(colNamesNew)                                          # check if columns exist
                self.hourlyData.drop(columns=ind2Delete, inplace=True)                                                          # delete existing columns to add new ones
                self.hourlyData = self.hourlyData.merge(df2Add, how='outer', left_index=True, right_index=True)           # add new columns to daily table

            self.updated_tokenCryptos = fileInfo.stat()
            print('>>>> DAT Cryptos data loaded from csv-file <<<<')


    #### MINUTELY DATA ####
    def loadMinutelyData(self):
        self.loadMinutelyDEXdata()

    def loadMinutelyDEXdata(self):
        filePath = self.dataPath + 'LMPoolData_ShortTerm.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_dexMinutely:
            minutelyDEXData = pd.read_csv(filePath, index_col=0)
            minutelyDEXData['timeRounded'] = pd.to_datetime(minutelyDEXData.Time).dt.floor('min') #.dt.strftime('%Y-%m-%d %H:%M')
            minutelyDEXData.set_index(['timeRounded'], inplace=True)

            for poolSymbol in minutelyDEXData.symbol.unique():
                df2Add = minutelyDEXData[minutelyDEXData.symbol == poolSymbol]
                df2Add = df2Add.drop(columns=['Time', 'symbol'])

                # calculate relative price deviations
                df2Add = df2Add.assign(relPriceDevCoingecko=((df2Add['DFIPrices'] - df2Add['reserveA/reserveB'])/df2Add['DFIPrices']))
                df2Add = df2Add.assign(relPriceDevBittrex=((df2Add['DFIPricesBittrex'] - df2Add['reserveA/reserveB']) / df2Add['DFIPricesBittrex']))

                # add prefix to column names for pool identification
                colNamesOrig = df2Add.columns.astype(str)
                colNamesNew = poolSymbol+'_' + colNamesOrig
                df2Add = df2Add.rename(columns=dict(zip(colNamesOrig, colNamesNew)))

                # delete existing information and add new one
                ind2Delete = self.minutelyData.columns.intersection(colNamesNew)                                          # check if columns exist
                self.minutelyData.drop(columns=ind2Delete, inplace=True)                                                          # delete existing columns to add new ones
                self.minutelyData = self.minutelyData.merge(df2Add, how='outer', left_index=True, right_index=True)           # add new columns to daily table

            self.minutelyData.dropna(axis=0, how='all',inplace=True)
            self.update_dexMinutely = fileInfo.stat()
            print('>>>> Minutely DEX data loaded from csv-file <<<<')

    #### NO TIMESERIES ####
    def loadNoTimeseriesData(self):
        self.loadLastRichlist()
        self.loadSnapshotData()
        self.loadChangelogData()

    def loadLastRichlist(self):
        filePath = self.dataPath + 'Richlist/'
        listCSVFiles = glob.glob(filePath + "*_01-*.csv")  # get all csv-files generated at night

        newestDate = self.dailyData['nbMnId'].dropna().index.max()  # find newest date in extracted Data
        file2Load = [x for x in listCSVFiles if re.search(newestDate, x)]  # find corresponding csv-file of richlist

        fname = pathlib.Path(file2Load[0])
        if fname.stat() != self.updated_LastRichlist:
            self.lastRichlist = pd.read_csv(file2Load[0])  # load richlist

            # date for information/explanation
            self.lastRichlist['date'] = pd.to_datetime(newestDate)

            self.updated_LastRichlist = fname.stat()
            print('>>>>>>>>>>>>> Richlist ', file2Load[0], ' loaded <<<<<<<<<<<<<')

    def loadSnapshotData(self):
        filePath = self.dataPath + 'snapshotData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_snapshotData:
            self.snapshotData = pd.read_csv(filePath, index_col=0)
            meanBlockTime = self.dailyData['meanBlockTime'].dropna().iloc[-11:-1].mean()
            duration = timedelta(seconds=self.snapshotData['blocksLeft'].values[0]*meanBlockTime)
            self.snapshotData['duration'] = duration-timedelta(microseconds=duration.microseconds)          # remove microseconds
            self.snapshotData['etaEvent'] = datetime.utcnow()+self.snapshotData['duration']
            self.update_snapshotData = fileInfo.stat()
            print('>>>>>>>>>>>>> Snapshot data loaded <<<<<<<<<<<<<')

    def loadChangelogData(self):
        filePath = self.dataPath + 'changelogHistory.xlsx'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_changelogData:
            self.changelogData = pd.read_excel(filePath, engine='openpyxl')
            self.changelogData.sort_values(by=['Date'], inplace=True, ascending=False)
            self.changelogData['Date'] = pd.to_datetime(self.changelogData['Date'], utc=True).dt.strftime('%Y-%m-%d')
            self.update_changelogData = fileInfo.stat()
            print('>>>>>>>>>>>>> Changelog data loaded <<<<<<<<<<<<<')