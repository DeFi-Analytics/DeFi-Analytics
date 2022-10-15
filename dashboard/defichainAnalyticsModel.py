import os
import glob
import pathlib
import re
import base64

import pandas as pd
import numpy as np
from ast import literal_eval

import time

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
        self.cfpData = None

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
        self.update_MNmonitor = None
        self.updated_dfx = None
        self.updated_dobby = None
        self.update_DFIsignal = None
        self.updated_vaults = None
        self.update_emissionRate=None
        self.update_coinPriceList = None
        self.updated_DFIPFutures = None
        self.updated_cfpData = None
        self.updated_BSCBridge = None
        self.update_dUSDMeasure = None
        self.updated_dUSDBurnBot = None


        # background image for figures
        with open(workDir + "/assets/analyticsLandscapeGrey2.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        self.figBackgroundImage = "data:image/png;base64," + encoded_string         # Add the prefix that plotly will want when using the string as source

    #### DAILY DATA #####
    def loadDailyData(self):
        self.loadCoinPriceList()
        self.loadHourlyDEXdata()
        self.loadDEXVolume()
        self.loadDailyTradingData()
        self.loadExtractedRichlistData()
        self.calcOverallTVLdata()
        self.loadDailyBlocktimeData()
        self.loadDAAData()
        self.loadTwitterData()
        self.loadTwitterFollowerData()
        self.loadIncomeVisitsData()
        self.loadPortfolioDownloads()
        self.loadPromoDatabase()
        self.loadMNMonitorDatabase()
        self.loadAnalyticsVisitsData()
        self.loadDFIsignalDatabase()
        self.loadDobbyDatabase()
        self.loadEmissionRateData()
        self.loadDUSDMeasureData()





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
            print('>>>> nodehub data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

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
            print('>>>> allnodes data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

    def loadExtractedRichlistData(self):
        print('>>>> Start update extracted richlist data ...  <<<<')
        filePath = self.dataPath + 'extractedDFIdata.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_extractedRichlist:
            extractedRichlist = pd.read_csv(filePath, index_col=0)

            ind2Delete = self.dailyData.columns.intersection(extractedRichlist.columns)                                 # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(extractedRichlist, how='outer', left_index=True, right_index=True)      # add new columns to daily table

            # extracting DFI in Liquidity-Mining
            lmCoins = pd.DataFrame(index=self.dailyData.index)
            lmCoins['BTC_pool'] = self.hourlyData.groupby('Date')['BTC-DFI_reserveB'].first()
            lmCoins['ETH_pool'] = self.hourlyData.groupby('Date')['ETH-DFI_reserveB'].first()
            lmCoins['USDT_pool'] = self.hourlyData.groupby('Date')['USDT-DFI_reserveB'].first()
            lmCoins['DOGE_pool'] = self.hourlyData.groupby('Date')['DOGE-DFI_reserveB'].first()
            lmCoins['LTC_pool'] = self.hourlyData.groupby('Date')['LTC-DFI_reserveB'].first()
            lmCoins['USDC_pool'] = self.hourlyData.groupby('Date')['USDC-DFI_reserveB'].first()
            lmCoins['dUSD_pool'] = self.hourlyData.groupby('Date')['DUSD-DFI_reserveB'].first()
            lmCoins['overall'] = lmCoins['BTC_pool'] + lmCoins['ETH_pool'] + lmCoins['USDT_pool'] + lmCoins['DOGE_pool'].fillna(0) + lmCoins['LTC_pool'].fillna(0) \
                                 + lmCoins['USDC_pool'] .fillna(0) + lmCoins['dUSD_pool'].fillna(0)
            self.dailyData['lmDFI'] = lmCoins['overall']

            # getting DFI in vaults
            vaultsDFI = self.hourlyData[['Date', 'sumDFI']]
            self.dailyData['vaultDFI'] = vaultsDFI[(vaultsDFI!=0.0) & (vaultsDFI.notnull())].groupby('Date')['sumDFI'].first()

            # sum of addresses and DFI
            self.dailyData['nbOverall'] = self.dailyData['nbMnId'] + self.dailyData['nbOtherId']
            self.dailyData['circDFI'] = self.dailyData['mnDFI'] + self.dailyData['otherDFI'] + self.dailyData['vaultDFI'].fillna(method='ffill')\
                                        + self.dailyData['tokenDFI'].fillna(0) + self.dailyData['lmDFI'].fillna(method='ffill') + self.dailyData['erc20DFI'].fillna(0) \
                                        - (self.dailyData['nbMNlocked10']+self.dailyData['nbMNlocked5']).fillna(0)*20000 + self.dailyData['fundDFI'] \
                                        + (self.dailyData['nbMNlocked10'] + self.dailyData['nbMNlocked5']).fillna(0) * 20000
            self.dailyData['totalDFI'] = self.dailyData['circDFI'] + self.dailyData['foundationDFI'].fillna(0) \
                                        + self.dailyData['burnedDFI'].fillna(method="ffill")

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
            self.dailyData['diffLMDFI'] = self.dailyData['lmDFI'].diff() / self.dailyData['diffDate']
            self.dailyData['diffvaultDFI'] = self.dailyData['vaultDFI'].diff() / self.dailyData['diffDate']

            self.updated_extractedRichlist = fileInfo.stat()
            print('>>>> Richlist data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

    def calcMasternodeNumbers(self):
        # load all relevant data
        self.loadExtractedRichlistData()
        self.loadMNnodehub()
        self.loadMNAllnodes()

        # calculate missing information
        self.dailyData['nbMNOther'] = self.dailyData['nbMnId'] - self.dailyData['nbMnCakeId'] - self.dailyData['nbMydefichainId'].fillna(method="ffill") - self.dailyData['nbMNNodehub'].fillna(method="ffill") - \
                                      self.dailyData['nbMNAllnode'].fillna(method="ffill")
        self.dailyData['nbMNnonCake'] = self.dailyData['nbMnId'] - self.dailyData['nbMnCakeId']

        self.dailyData['nbMnCakeIdRelative'] = self.dailyData['nbMnCakeId'] / self.dailyData['nbMnId'] * 100
        self.dailyData['nbMNOtherRelative'] = self.dailyData['nbMNOther'] / self.dailyData['nbMnId'] * 100
        self.dailyData['nbMydefichainRelative'] = self.dailyData['nbMydefichainId'] / self.dailyData['nbMnId'] * 100
        self.dailyData['nbMNNodehubRelative'] = self.dailyData['nbMNNodehub'] / self.dailyData['nbMnId'] * 100
        self.dailyData['nbMNAllnodeRelative'] = self.dailyData['nbMNAllnode'] / self.dailyData['nbMnId'] * 100

        self.dailyData['nbMNlocked10Relative'] = self.dailyData['nbMNlocked10'] / self.dailyData['nbMnId'] * 100
        self.dailyData['nbMNlocked5Relative'] = self.dailyData['nbMNlocked5'] / self.dailyData['nbMnId'] * 100
        print('>>>> Masternode data calculated <<<< ====')

    def calcOverallTVLdata(self):
        self.dailyData['tvlMNDFI'] = self.dailyData['nbMnId'] * ((pd.to_datetime(self.dailyData.index)<pd.Timestamp('2021-03-02')) * 1 * 1000000 + \
                                                                 (pd.to_datetime(self.dailyData.index)>=pd.Timestamp('2021-03-02')) * 1 * 20000)

        dexLockedDFI = (self.hourlyData['BTC-DFI_lockedDFI']+self.hourlyData['ETH-DFI_lockedDFI']+self.hourlyData['USDT-DFI_lockedDFI'] +
                      self.hourlyData['DOGE-DFI_lockedDFI'].fillna(0)+self.hourlyData['LTC-DFI_lockedDFI'].fillna(0) +
                      self.hourlyData['BCH-DFI_lockedDFI'].fillna(0) + self.hourlyData['USDC-DFI_lockedDFI'].fillna(0) +
                      self.hourlyData['DUSD-DFI_reserveB'].fillna(0))
        dexLockedDFI.index = dexLockedDFI.index.floor('D').astype(str) # remove time information, only date is needed
        self.dailyData['tvlDEXDFI'] = dexLockedDFI.groupby(level=0).first()

        vaultsLockedDFI = self.hourlyData.sumBTC / self.hourlyData['BTC-DFI_reserveA/reserveB'] + \
                            self.hourlyData.sumETH.fillna(0) / self.hourlyData['ETH-DFI_reserveA/reserveB'].fillna(0) + \
                            self.hourlyData.sumDFI + \
                            self.hourlyData.sumUSDC / self.hourlyData['USDC-DFI_reserveA/reserveB'] + \
                            self.hourlyData.sumUSDT / self.hourlyData['USDT-DFI_reserveA/reserveB'] + \
                            self.hourlyData.sumDUSD.fillna(0) / self.hourlyData['DUSD-DFI_reserveA/reserveB'].fillna(0)

        vaultsLockedDFI.index = vaultsLockedDFI.index.floor('D').astype(str) # remove time information, only date is needed
        self.dailyData['tvlVaultsDFI'] = vaultsLockedDFI[(vaultsLockedDFI!=0.0) & (vaultsLockedDFI.notnull())].groupby(level=0).first()
        print('>>>> Overall TVL calculated <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))


    def loadDailyTradingData(self):
        print('>>>> Start update trading data ...  <<<<')
        filePath = self.dataPath + 'dailyTradingResultsDEX.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_tradingData:
            dailyTradingResults = pd.read_csv(self.dataPath+'dailyTradingResultsDEX.csv',index_col=0)
            dailyTradingResults.drop(['DFIPriceUSD', 'BTCPriceUSD', 'ETHPriceUSD', 'USDTPriceUSD', 'DOGEPriceUSD', 'LTCPriceUSD', 'BCHPriceUSD', 'USDCPriceUSD'], axis=1, inplace=True)     # remove information and use coinpricelist file

            ind2Delete = self.dailyData.columns.intersection(dailyTradingResults.columns)                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(dailyTradingResults, how='outer', left_index=True, right_index=True)    # add new columns to daily table

            # calc market cap data in USD and BTC (same as in loadExtractedRichlistData to get updated price information
            # if 'circDFI' in self.dailyData.columns:
            #     print('>>>>>>>> Update market cap in loadDailyTradingData...  <<<<<<<<')
            #     self.dailyData['marketCapUSD'] = self.dailyData['circDFI']*self.dailyData['DFIPriceUSD']
            #     self.dailyData['marketCapBTC'] = self.dailyData['marketCapUSD'] / self.dailyData['BTCPriceUSD']

            self.updated_tradingData = fileInfo.stat()
            print('>>>> Trading data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

    def loadDailyBlocktimeData(self):
        print('>>>> Start update blocktime data ... <<<<')
        filePath = self.dataPath + 'BlockListStatistics.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_blocktime:
            dailyBlocktimeData = pd.read_csv(filePath, index_col=0)


            ind2Delete = self.dailyData.columns.intersection(dailyBlocktimeData.columns)                                # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(dailyBlocktimeData, how='outer', left_index=True,right_index=True)    # add new columns to daily table

            self.updated_blocktime = fileInfo.stat()
            print('>>>> Blocktime data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

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
            print('>>>> DAA data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

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
            print('>>>> Twitter data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

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
            print('>>>> Twitter data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

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
            print('>>>> Income visits data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

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
            print('>>>> Portfolio downloads data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

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
            print('>>>> DefiChain promo database loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

    def loadMNMonitorDatabase(self):
        print('>>>> Start update masternode monitor database ... <<<<')
        filePath = self.dataPath + 'masternodeMonitorData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_MNmonitor:
            monitorRawData = pd.read_csv(filePath, index_col=0)

            columns2update = ['nbMasternodes', 'nbAccounts']

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(monitorRawData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.update_MNmonitor = fileInfo.stat()
            print('>>>> MN Monitor database loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

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
            print('>>>> Analytics visits data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

    def loadDFIsignalDatabase(self):
        print('>>>> Start update DFI-signal database ... <<<<')
        filePath = self.dataPath + 'dfiSignalData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_DFIsignal:
            dfiSignalRawData = pd.read_csv(filePath, index_col=0)
            dfiSignalRawData.rename(columns={'user_count': 'DFISignal_user_count'}, inplace=True)
            columns2update = ['DFISignal_user_count','masternode_count','messages_sent','commands_received','minted_blocks']

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(dfiSignalRawData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.update_DFIsignal = fileInfo.stat()
            print('>>>> DFI-Signal database loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

    def loadDobbyDatabase(self):
        print('>>>> Start update Dobby database ... <<<<')
        filePath = self.dataPath + 'dobbyData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_DFIsignal:
            dobbyRawData = pd.read_csv(filePath, index_col=0)
            columns2update = ['user_count', 'vault_count', 'sum_messages', 'sum_collateral', 'sum_loan', 'avg_ratio']

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(dobbyRawData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.updated_dobby = fileInfo.stat()
            print('>>>> Dobby database loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

    def loadEmissionRateData(self):
        print('>>>> Start update emission rate data ... <<<<')
        filePath = self.dataPath + 'dfiEmissionData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_emissionRate:
            emissionRawData = pd.read_csv(filePath, index_col=0)
            emissionRawData.rename({'anchor': 'anchorEmission',
                                    'burned': 'burnedEmission',
                                    'community':'communityEmission',
                                    'dToken': 'dTokenEmission',
                                    'dex': 'dexEmission',
                                    'masternode': 'masternodeEmission',
                                    'total': 'totalEmission' }, axis=1, inplace=True)
            columns2update = ['anchorEmission', 'burnedEmission', 'communityEmission', 'dTokenEmission', 'dexEmission', 'masternodeEmission', 'totalEmission' ]

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(emissionRawData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.update_emissionRate = fileInfo.stat()
            print('>>>> Emission rate data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

    def loadCoinPriceList(self):
        print('>>>> Start update coin price list ... <<<<')
        filePath = self.dataPath + 'coinPriceList.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_coinPriceList:
            coinPriceListData = pd.read_csv(filePath, index_col=0)

            columns2update = ['DFIPriceUSD','BTCPriceUSD','ETHPriceUSD','USDTPriceUSD','DOGEPriceUSD','LTCPriceUSD','BCHPriceUSD','USDCPriceUSD']

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(coinPriceListData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.update_coinPriceList = fileInfo.stat()
            print('>>>> Coin price list loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

    def loadDUSDMeasureData(self):
        print('>>>> Start update dUSD measure data ... <<<<')
        filePath = self.dataPath + 'dUSDDailyData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_dUSDMeasure:
            dUSDMeasureData = pd.read_csv(filePath, index_col=0)

            columns2update = ['sellDUSDFee', 'interestDUSDLoans', 'rewardDUSDBurnBot']

            # delete existing information and add new one
            ind2Delete = self.dailyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(dUSDMeasureData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.update_dUSDMeasure = fileInfo.stat()
            print('>>>> dUSD measure data loaded from csv-file <<<< ==== Columns: '+str(len(self.dailyData.columns))+'  Rows: '+str(len(self.dailyData.index)))

    #### HOURLY DATA ####
    def loadHourlyData(self):
        self.loadHourlyDEXdata()
        self.loadDEXVolume()
        self.loadTokenCrypto()
        self.loadHourlyDEXTrades()
        self.loadDFXdata()
        self.loadVaultData()
        self.loadDFIPFuturesData()
        self.loadBSCBridgeData()
        self.loadDUSDBurnBotData()


    def loadHourlyDEXdata(self):
        print('>>>> Start update hourly DEX data ... <<<<')
        filePath = self.dataPath + 'LMPoolData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_dexHourly:
            tStart = time.time()

            hourlyDEXData = pd.read_csv(filePath, header=0,
                                        usecols=["DFIPrices", "DFIPricesBittrex", "Time", 'numberAddresses', 'reserveA', 'reserveA/reserveB',
                                               'reserveB', 'reserveB/reserveA', 'symbol', 'totalLiquidity', '24hrTrading', '30dTrading', 'APRblock', 'APRcommission'],
                                        dtype={"DFIPrices": float, "DFIPricesBittrex": float, "Time": "string",
                                                'numberAddresses': float, 'reserveA': float, 'reserveA/reserveB': float,
                                               'reserveB': float, 'reserveB/reserveA':float, 'symbol': "string", 'totalLiquidity': float, '24hrTrading': float, '30dTrading': float})

            hourlyDEXData['timeRounded'] = pd.to_datetime(hourlyDEXData.Time).dt.floor('H')
            hourlyDEXData.set_index(['timeRounded'], inplace=True)
            hourlyDEXData['reserveA_DFI'] = hourlyDEXData['reserveA'] / hourlyDEXData['DFIPrices']

            priceUSDT = hourlyDEXData[hourlyDEXData.symbol == 'USDT-DFI'].DFIPrices
            priceBTC = hourlyDEXData[hourlyDEXData.symbol == 'BTC-DFI'].DFIPrices

            dfDataCollecting = pd.DataFrame() # temporary dataframe for iterative merge => less data results in higher speed
            for poolSymbol in hourlyDEXData.symbol.dropna().unique():
                df2Add = hourlyDEXData[hourlyDEXData.symbol == poolSymbol]
                df2Add = df2Add.drop(columns=['Time', 'symbol'])

                df2Add['lockedDFI'] = df2Add['reserveB'] + df2Add['reserveA_DFI']
                df2Add['lockedUSD'] = df2Add['lockedDFI'] * priceUSDT
                df2Add['lockedBTC'] = df2Add['lockedDFI'] * priceBTC

                # calculate relative price deviations
                df2Add['relPriceDevCoingecko'] = ((df2Add['DFIPrices'] - df2Add['reserveA/reserveB'])/df2Add['DFIPrices'])
                df2Add['relPriceDevBittrex'] = ((df2Add['DFIPricesBittrex'] - df2Add['reserveA/reserveB']) / df2Add['DFIPricesBittrex'])

                # add prefix to column names for pool identification
                colNamesOrig = df2Add.columns.astype(str)
                colNamesNew = poolSymbol+'_' + colNamesOrig
                df2Add = df2Add.rename(columns=dict(zip(colNamesOrig, colNamesNew)))

                dfDataCollecting = dfDataCollecting.merge(df2Add, how='outer', left_index=True, right_index=True) # merge current ticker with already loaded ones

            ind2Delete = self.hourlyData.columns.intersection(dfDataCollecting.columns)     # columns already available in hourly data set
            self.hourlyData.drop(columns=ind2Delete, inplace=True)                          # deleten old, existing columns
            self.hourlyData = self.hourlyData.merge(dfDataCollecting, how='outer', left_index=True, right_index=True)  # add new columns to daily table

            self.hourlyData['Date'] = pd.to_datetime(self.hourlyData.index).strftime('%Y-%m-%d')
            self.updated_dexHourly = fileInfo.stat()
            print('>>>> Hourly DEX data loaded from csv-file <<<< ==== Columns: '+str(len(self.hourlyData.columns))+'  Rows: '+str(len(self.hourlyData.index))+'    Time needed: '+str(time.time()-tStart))

    def loadDEXVolume(self):
        print('>>>> Start update DEX volume data ... <<<<')
        filePath = self.dataPath + 'DEXVolumeData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_dexVolume:
            tStart = time.time()
            volumeData = pd.read_csv(filePath, index_col=0)
            volumeData['timeRounded'] = pd.to_datetime(volumeData.Time).dt.floor('H')
            volumeData.set_index(['timeRounded'], inplace=True)

            df2Add = pd.DataFrame()
            for poolSymbol in volumeData['base_name'].unique():
                temp = volumeData[volumeData['base_name']==poolSymbol][['base_volume', 'quote_volume']].sum(axis=1)
                df2Add[poolSymbol + '_'+'VolTotal'] = temp.groupby(temp.index).max()    # max operation needed for handling stock split, where old pool is still available in the API data

            # delete existing information and add new one
            colNames = df2Add.columns
            ind2Delete = self.hourlyData.columns.intersection(colNames)                                          # check if columns exist
            self.hourlyData.drop(columns=ind2Delete, inplace=True)                                                          # delete existing columns to add new ones
            self.hourlyData = self.hourlyData.merge(df2Add, how='outer', left_index=True, right_index=True)           # add new columns to daily table

            # calculate total volume after merge of data
            self.hourlyData['VolTotal'] = self.hourlyData['BTC_VolTotal']*0   # only use rows with data; BTC was the first pool and have to most data (beside ETH, USDT)
            for poolSymbol in volumeData['base_name'].unique():
                self.hourlyData['VolTotal'] = self.hourlyData['VolTotal'] + self.hourlyData[poolSymbol+'_'+'VolTotal'].fillna(0)

            self.hourlyData['VolTotalCoingecko'] = volumeData[volumeData['base_name']=='BTC']['coingeckoVolume']
            self.updated_dexVolume = fileInfo.stat()
            print('>>>> DEX volume data loaded from csv-file <<<< ==== Columns: '+str(len(self.hourlyData.columns))+'  Rows: '+str(len(self.hourlyData.index))+'    Time needed: '+str(time.time()-tStart))

    def loadHourlyDEXTrades(self):
        print('>>>> Start update hourly DEX trade data ... <<<<')
        filePath = self.dataPath + 'hourlyDEXTrades.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_hourlyDEXTrades:
            tStart = time.time()
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
            print('>>>> DEX volume data loaded from csv-file <<<< ==== Columns: '+str(len(self.hourlyData.columns))+'  Rows: '+str(len(self.hourlyData.index))+'    Time needed: '+str(time.time()-tStart))

    def loadTokenCrypto(self):
        print('>>>> Start update token data ... <<<<')
        filePath = self.dataPath + 'TokenData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_tokenCryptos:
            tStart = time.time()
            tokenData = pd.read_csv(filePath, index_col=0)
            tokenData['timeRounded'] = pd.to_datetime(tokenData.Time).dt.floor('H')
            tokenData.set_index(['timeRounded'], inplace=True)

            dfDataCollecting = pd.DataFrame() # temporary dataframe for iterative merge => less data results in higher speed
            for coinSymbol in tokenData['symbol'].unique():
                df2Add = tokenData[tokenData['symbol']==coinSymbol][['Burned', 'minted', 'Collateral']]
                df2Add['tokenDefiChain'] = df2Add['minted'] - df2Add['Burned'].fillna(0)
                df2Add['diffToken'] = df2Add['Collateral']-df2Add['minted']+df2Add['Burned'].fillna(0)

                # add prefix to column names for pool identification
                colNamesOrig = df2Add.columns.astype(str)
                colNamesNew = coinSymbol + '_' + colNamesOrig
                df2Add = df2Add.rename(columns=dict(zip(colNamesOrig, colNamesNew)))

                dfDataCollecting = dfDataCollecting.merge(df2Add, how='outer', left_index=True, right_index=True)  # merge current ticker with already loaded ones

            ind2Delete = self.hourlyData.columns.intersection(dfDataCollecting.columns)  # columns already available in hourly data set
            self.hourlyData.drop(columns=ind2Delete, inplace=True)  # deleten old, existing columns
            self.hourlyData = self.hourlyData.merge(dfDataCollecting, how='outer', left_index=True, right_index=True)  # add new columns to daily table

            self.updated_tokenCryptos = fileInfo.stat()
            print('>>>> DAT Cryptos data loaded from csv-file <<<< ==== Columns: '+str(len(self.hourlyData.columns))+'  Rows: '+str(len(self.hourlyData.index))+'    Time needed: '+str(time.time()-tStart))

    def loadDFXdata(self):
        print('>>>> Start update DFX data ... <<<<')
        filePath = self.dataPath + 'dfxData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_dfx:
            tStart = time.time()
            dfxData = pd.read_csv(filePath, index_col=0)
            dfxData['timeRounded'] = pd.to_datetime(dfxData.index).floor('H')
            dfxData.set_index(['timeRounded'], inplace=True)

            columns2update = ['dfxBuyVolume', 'dfxSellVolume']

            # delete existing information and add new one
            ind2Delete = self.hourlyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.hourlyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.hourlyData = self.hourlyData.merge(dfxData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.updated_dfx = fileInfo.stat()
            print('>>>> DFX data loaded from csv-file <<<< ==== Columns: '+str(len(self.hourlyData.columns))+'  Rows: '+str(len(self.hourlyData.index))+'    Time needed: '+str(time.time()-tStart))

    def loadVaultData(self):
        print('>>>> Start update Vault data ... <<<<')
        filePath = self.dataPath + 'vaultsData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_vaults:
            tStart = time.time()
            vaultsDataHeader = pd.read_csv(filePath, index_col=0, nrows=0).columns
            types_dict = {'burnedPayback': str, 'dexfeetokens': str, 'dfipaybacktokens': str}
            types_dict.update({col: float for col in vaultsDataHeader if col not in types_dict})
            vaultsData = pd.read_csv(filePath, index_col=0, dtype=types_dict)

            vaultsData['timeRounded'] = pd.to_datetime(vaultsData.index).floor('H')
            vaultsData.set_index(['timeRounded'], inplace=True)

            # get list of burned tocken ticker
            lastString = vaultsData['dexfeetokens'][-1]
            listTokens = re.findall("@(.+?)'", lastString)

            for tokenSymbol in listTokens:
                colString = vaultsData['dexfeetokens'][vaultsData['dexfeetokens'].str.contains('@'+tokenSymbol).fillna(False)]
                burnedToken = colString.str.split('@'+tokenSymbol, expand=True)[0].str.rsplit("'",n=1, expand=True).iloc[:,-1]           # first column contains the number at the end
                vaultsData['burned' + tokenSymbol + 'DEX'] = pd.to_numeric(burnedToken)

            burnedValues = [item for item in vaultsData.columns if "burned" in item if "DEX" in item] # list of all label names for columns2update

            vaultsData['DUSDpaidDFI'] = vaultsData['dfipaybacktokens'].apply(lambda x: float(str(x)[2:str(x).find('@')]) if isinstance(x,str) else np.nan)

            # extract burned DFI and dUSD via payback function
            temp = vaultsData['burnedPayback'].str.split(',', expand=True)
            burnedDFIPayback_Old = pd.to_numeric(temp[~temp[0].str.contains('@DFI').fillna(False)][0])                  # only number in data column
            burnedDFIPayback_New = pd.to_numeric(temp[temp[0].str.contains('@DFI').fillna(False)][0].str[2:-5])         # list of all tokens in column
            burneddUSDPayback_New = pd.to_numeric(temp[temp[1].str.contains('@DUSD').fillna(False)][1].str[2:-6])       # dUSD payback only as list available
            vaultsData['burnedPayback'] = pd.concat([burnedDFIPayback_Old, burnedDFIPayback_New])
            vaultsData['burnedPaybackDUSD'] = burneddUSDPayback_New


            sumValues = [item for item in vaultsData.columns if "sum" in item]
            liveTicker = [item[7:]+'-USD' for item in vaultsData.columns if (("sumLoan") in item) & ~(('sumLoanLiquidation') in item)]
            liveTicker += ['DFI-USD']

            columns2update = burnedValues + sumValues + liveTicker + ['nbLiquidation', 'nbLoans', 'nbVaults', 'burnedAuction', 'burnedPayback', 'burnedDFIPayback', 'burnedPaybackDUSD', 'MIN150', 'MIN175',
                                                       'MIN200', 'MIN350', 'MIN500', 'MIN1000', 'DUSDpaidDFI', 'mintedDUSDnode','burnedOverallDUSD']
            columns2update.remove('DUSD-USD')

            # delete existing information and add new one
            ind2Delete = self.hourlyData.columns.intersection(columns2update)                                                               # check if columns exist
            self.hourlyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.hourlyData = self.hourlyData.merge(vaultsData[columns2update], how='outer', left_index=True, right_index=True)            # add new columns to daily table
            self.updated_vaults = fileInfo.stat()
            print('>>>> Vaults data loaded from csv-file <<<< ==== Columns: '+str(len(self.hourlyData.columns))+'  Rows: '+str(len(self.hourlyData.index))+'    Time needed: '+str(time.time()-tStart))

    def loadDFIPFuturesData(self):
        print('>>>> Start update DFIP futures data ... <<<<')
        filePath = self.dataPath + 'DFIPFuturesData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_DFIPFutures:
            tStart = time.time()
            DFIPFuturesData = pd.read_csv(filePath, index_col=0)
            DFIPFuturesData['timeRounded'] = pd.to_datetime(DFIPFuturesData.index).floor('H')
            DFIPFuturesData.set_index(['timeRounded'], inplace=True)

            # delete existing information and add new one
            ind2Delete = self.hourlyData.columns.intersection(DFIPFuturesData.columns)                                                               # check if columns exist
            self.hourlyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.hourlyData = self.hourlyData.merge(DFIPFuturesData, how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.updated_DFIPFutures = fileInfo.stat()
            print('>>>> DFIP futures data loaded from csv-file <<<< ==== Columns: '+str(len(self.hourlyData.columns))+'  Rows: '+str(len(self.hourlyData.index))+'    Time needed: '+str(time.time()-tStart))

    def loadDUSDBurnBotData(self):
        print('>>>> Start update dUSD burn bot data ... <<<<')
        filePath = self.dataPath + 'dUSDBornBotAmounts.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_dUSDBurnBot:
            tStart = time.time()
            dUSDBurnBot = pd.read_csv(filePath, index_col=0)
            dUSDBurnBot['timeRounded'] = pd.to_datetime(dUSDBurnBot.index).tz_localize(None).floor('H')
            dUSDBurnBot.set_index(['timeRounded'], inplace=True, drop=True)

            # delete existing information and add new one
            ind2Delete = self.hourlyData.columns.intersection(dUSDBurnBot.columns)                                                               # check if columns exist
            self.hourlyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.hourlyData = self.hourlyData.merge(dUSDBurnBot, how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.updated_dUSDBurnBot = fileInfo.stat()
            print('>>>> dUSD burn bot data loaded from csv-file <<<< ==== Columns: '+str(len(self.hourlyData.columns))+'  Rows: '+str(len(self.hourlyData.index))+'    Time needed: '+str(time.time()-tStart))

    def loadBSCBridgeData(self):
        print('>>>> Start update BSC bridge data ... <<<<')
        filePath = self.dataPath + 'bscDFIBridgeData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_BSCBridge:
            tStart = time.time()
            BSCBridgeData = pd.read_csv(filePath, index_col=0)
            BSCBridgeData.index = pd.to_datetime(BSCBridgeData.index)

            # delete existing information and add new one
            ind2Delete = self.hourlyData.columns.intersection(BSCBridgeData.columns)                                                               # check if columns exist
            self.hourlyData.drop(columns=ind2Delete, inplace=True)                                                                          # delete existing columns to add new ones
            self.hourlyData = self.hourlyData.merge(BSCBridgeData, how='outer', left_index=True, right_index=True)            # add new columns to daily table

            self.updated_BSCBridge = fileInfo.stat()
            print('>>>> BSC bridge data loaded from csv-file <<<< ==== Columns: '+str(len(self.hourlyData.columns))+'  Rows: '+str(len(self.hourlyData.index))+'    Time needed: '+str(time.time()-tStart))


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
            print('>>>> Minutely DEX data loaded from csv-file <<<<'+str(len(self.minutelyData.columns)))

    #### NO TIMESERIES ####
    def loadNoTimeseriesData(self):
        self.loadLastRichlist()
        self.loadSnapshotData()
        self.loadChangelogData()
        self.loadCFPData()

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
            print('>>>>>>>>>>>>> Richlist ', file2Load[0], ' loaded <<<<<<<<<<<<<'+str(len(self.lastRichlist.columns)))

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
            print('>>>>>>>>>>>>> Snapshot data loaded <<<<<<<<<<<<<'+str(len(self.snapshotData.columns)))

    def loadChangelogData(self):
        filePath = self.dataPath + 'changelogHistory.xlsx'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.update_changelogData:
            self.changelogData = pd.read_excel(filePath, engine='openpyxl')
            self.changelogData.sort_values(by=['Date'], inplace=True, ascending=False)
            self.changelogData['Date'] = pd.to_datetime(self.changelogData['Date'], utc=True).dt.strftime('%Y-%m-%d')
            self.update_changelogData = fileInfo.stat()
            print('>>>>>>>>>>>>> Changelog data loaded <<<<<<<<<<<<<'+str(len(self.changelogData.columns)))

    def loadCFPData(self):
        filePath = self.dataPath + 'listCFPs.xlsx'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_cfpData:
            self.cfpData = pd.read_excel(filePath, engine='openpyxl')
            self.cfpData.sort_values(by=['nb'], inplace=True, ascending=True)
            self.cfpData.rename(columns={"DFI": "dfi", "nb": "#"}, inplace=True)
            self.updated_cfpData = fileInfo.stat()
            print('>>>>>>>>>>>>> CFP data loaded <<<<<<<<<<<<<'+str(len(self.cfpData.columns)))