import os
import pandas as pd
import pathlib

class defichainAnalyticsModelClass:
    def __init__(self):
        workDir = os.path.abspath(os.getcwd())
        self.dataPath = workDir[:-9] + '/data/'
        self.dailyData = pd.DataFrame()
        self.hourlyData = pd.DataFrame()

        # last update of csv-files
        self.updated_extractedRichlist = None
        self.updated_tradingData = None
        self.updated_blocktime = None
        self.updated_dexHourly = None

    #### DAILY DATA #####
    def loadDailyData(self):
        self.loadHourlyDEXdata()
        self.loadExtractedRichlistData()
        self.loadDailyTradingData()
        self.loadDailyBlocktimeData()

    def loadExtractedRichlistData(self):
        filePath = self.dataPath + 'extractedDFIdata.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_extractedRichlist:
            extractedRichlist = pd.read_csv(filePath, index_col=0)

            ind2Delete = self.dailyData.columns.intersection(extractedRichlist.columns)                                 # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(extractedRichlist, how='outer', left_index=True, right_index=True)      # add new columns to daily table

            # extracting DFI in Liquidity-Mining
            lmCoins = pd.DataFrame(index=self.dailyData.index)
            lmCoins['BTC_pool'] = self.hourlyData[self.hourlyData.symbol == 'BTC-DFI'].groupby('date')['reserveB'].first()
            lmCoins['ETH_pool'] = self.hourlyData[self.hourlyData.symbol == 'ETH-DFI'].groupby('date')['reserveB'].first()
            lmCoins['USDT_pool'] = self.hourlyData[self.hourlyData.symbol == 'USDT-DFI'].groupby('date')['reserveB'].first()
            lmCoins['DOGE_pool'] = self.hourlyData[self.hourlyData.symbol == 'DOGE-DFI'].groupby('date')['reserveB'].first()
            lmCoins['LTC_pool'] = self.hourlyData[self.hourlyData.symbol == 'LTC-DFI'].groupby('date')['reserveB'].first()
            lmCoins['overall'] = lmCoins['BTC_pool'] + lmCoins['ETH_pool'] + lmCoins['USDT_pool'] + lmCoins['DOGE_pool'].fillna(0) + lmCoins['LTC_pool'].fillna(0)
            self.dailyData['lmDFI'] = lmCoins['overall']

            # total amount of addresses and DFI
            self.dailyData['nbOverall'] = self.dailyData['nbMnId'] + self.dailyData['nbOtherId']
            self.dailyData['totalDFI'] = self.dailyData['fundDFI'] + self.dailyData['mnDFI'] + self.dailyData['otherDFI'] + \
                                       self.dailyData['foundationDFI'].fillna(0) + self.dailyData['lmDFI'].fillna(0)

            self.updated_extractedRichlist = fileInfo.stat()
            print('>>>> Richlist data loaded from csv-file <<<<')

    def loadDailyTradingData(self):
        filePath = self.dataPath + 'dailyTradingResultsDEX.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_tradingData:
            dailyTradingResults = pd.read_csv(self.dataPath+'dailyTradingResultsDEX.csv',index_col=0)

            ind2Delete = self.dailyData.columns.intersection(dailyTradingResults.columns)                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete exisiting columns to add new ones
            self.dailyData = self.dailyData.merge(dailyTradingResults, how='outer',left_index=True,right_index=True)    # add new columns to daily table

            self.updated_tradingData = fileInfo.stat()
            print('>>>> Trading data loaded from csv-file <<<<')

    def loadDailyBlocktimeData(self):
        filePath = self.dataPath + 'BlockListStatistics.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_blocktime:
            dailyBlocktimeData = pd.read_csv(filePath, index_col=0)
            dailyBlocktimeData['tps'] = dailyBlocktimeData['txCount'] / (24 * 60 * 60)

            ind2Delete = self.dailyData.columns.intersection(dailyBlocktimeData.columns)                                # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete exisiting columns to add new ones
            self.dailyData = self.dailyData.merge(dailyBlocktimeData, how='outer', left_index=True,right_index=True)    # add new columns to daily table

            self.updated_blocktime = fileInfo.stat()
            print('>>>> Blocktime data loaded from csv-file <<<<')

    def loadHourlyDEXdata(self):
        filePath = self.dataPath + 'LMPoolData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_dexHourly:
            self.hourlyData = pd.read_csv(filePath, index_col=0)
            self.hourlyData['date'] = pd.to_datetime(self.hourlyData.Time).dt.strftime('%Y-%m-%d')

            self.updated_dexHourly = fileInfo.stat()
            print('>>>> Hourly DEX data loaded from csv-file <<<<')

    #### MINUTELY DATA ####
    def loadShortTermDEXPrice(self):
        ShortTermDEXPrice = pd.read_csv(self.dataPath+'LMPoolData_ShortTerm.csv',index_col=0)
        # self.dailyData = self.dailyData.merge(ShortTermDEXPrice, how='outer')