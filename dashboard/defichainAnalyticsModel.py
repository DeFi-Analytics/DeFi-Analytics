import os
import glob
import pathlib
import re
import base64

import pandas as pd


class defichainAnalyticsModelClass:
    def __init__(self):
        workDir = os.path.abspath(os.getcwd())
        self.dataPath = workDir[:-9] + '/data/'

        # data for controller/views
        self.dailyData = pd.DataFrame()
        self.hourlyData = pd.DataFrame()
        self.lastRichlist = None

        # last update of csv-files
        self.updated_extractedRichlist = None
        self.updated_tradingData = None
        self.updated_blocktime = None
        self.updated_dexHourly = None
        self.updated_daa = None
        self.updated_LastRichlist = None
        self.updated_dexVolume = None

        # background image for figures
        with open(workDir + "/assets/logo-defi-analytics_grey.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        self.figBackgroundImage = "data:image/png;base64," + encoded_string         # Add the prefix that plotly will want when using the string as source

    #### DAILY DATA #####
    def loadDailyData(self):
        self.loadHourlyDEXdata()
        self.loadDEXVolume()
        self.loadExtractedRichlistData()
        self.loadDailyTradingData()
        self.loadDailyBlocktimeData()
        self.loadDAAData()

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
            lmCoins['BTC_pool'] = self.hourlyData.groupby('Date')['BTC-DFI_reserveB'].first()
            lmCoins['ETH_pool'] = self.hourlyData.groupby('Date')['ETH-DFI_reserveB'].first()
            lmCoins['USDT_pool'] = self.hourlyData.groupby('Date')['USDT-DFI_reserveB'].first()
            lmCoins['DOGE_pool'] = self.hourlyData.groupby('Date')['DOGE-DFI_reserveB'].first()
            lmCoins['LTC_pool'] = self.hourlyData.groupby('Date')['LTC-DFI_reserveB'].first()
            lmCoins['overall'] = lmCoins['BTC_pool'] + lmCoins['ETH_pool'] + lmCoins['USDT_pool'] + lmCoins['DOGE_pool'].fillna(0) + lmCoins['LTC_pool'].fillna(0)
            self.dailyData['lmDFI'] = lmCoins['overall']

            # total amount of addresses and DFI
            self.dailyData['nbOverall'] = self.dailyData['nbMnId'] + self.dailyData['nbOtherId']
            self.dailyData['totalDFI'] = self.dailyData['fundDFI'] + self.dailyData['mnDFI'] + self.dailyData['otherDFI'] + \
                                       self.dailyData['foundationDFI'].fillna(0) + self.dailyData['lmDFI'].fillna(0)

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
        filePath = self.dataPath + 'dailyTradingResultsDEX.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_tradingData:
            dailyTradingResults = pd.read_csv(self.dataPath+'dailyTradingResultsDEX.csv',index_col=0)

            ind2Delete = self.dailyData.columns.intersection(dailyTradingResults.columns)                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete existing columns to add new ones
            self.dailyData = self.dailyData.merge(dailyTradingResults, how='outer', left_index=True, right_index=True)    # add new columns to daily table

            self.updated_tradingData = fileInfo.stat()
            print('>>>> Trading data loaded from csv-file <<<<')

    def loadDailyBlocktimeData(self):
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
            print('>>>> Blocktime data loaded from csv-file <<<<')

    #### HOURLY DATA ####
    def loadHourlyDEXdata(self):
        filePath = self.dataPath + 'LMPoolData.csv'
        fileInfo = pathlib.Path(filePath)
        if fileInfo.stat() != self.updated_dexHourly:
            hourlyDEXData = pd.read_csv(filePath, index_col=0)
            hourlyDEXData['timeRounded'] = pd.to_datetime(hourlyDEXData.Time).dt.floor('H')
            hourlyDEXData.set_index(['timeRounded'], inplace=True)
            hourlyDEXData['reserveA_DFI'] = hourlyDEXData['reserveA'] / hourlyDEXData['DFIPrices']

            for poolSymbol in hourlyDEXData.symbol.unique():
                df2Add = hourlyDEXData[hourlyDEXData.symbol == poolSymbol]
                df2Add = df2Add.drop(columns=['Time', 'symbol'])

                # calculate locked DFI and corresponding values
                df2Add = df2Add.assign(lockedDFI=df2Add['reserveB'] + df2Add['reserveA_DFI'])
                df2Add = df2Add.assign(lockedUSD=df2Add['lockedDFI']*hourlyDEXData[hourlyDEXData.symbol == 'USDT-DFI'].DFIPrices)
                df2Add = df2Add.assign(lockedBTC=df2Add['lockedDFI'] * hourlyDEXData[hourlyDEXData.symbol == 'BTC-DFI'].DFIPrices)

                # add prefix to column names for pool identification
                colNamesOrig = df2Add.columns.astype(str)
                colNamesNew = poolSymbol+'_' + colNamesOrig
                df2Add = df2Add.rename(columns=dict(zip(colNamesOrig, colNamesNew)))

                # delete existing information and add new one
                ind2Delete = self.hourlyData.columns.intersection(colNamesNew)                                          # check if columns exist
                self.hourlyData.drop(columns=ind2Delete, inplace=True)                                                          # delete existing columns to add new ones
                self.hourlyData = self.hourlyData.merge(df2Add, how='outer', left_index=True, right_index=True)           # add new columns to daily table

            self.hourlyData['Date'] = pd.to_datetime(hourlyDEXData[hourlyDEXData.symbol=='BTC-DFI'].index).strftime('%Y-%m-%d')
            self.updated_dexHourly = fileInfo.stat()
            print('>>>> Hourly DEX data loaded from csv-file <<<<')

    def loadDEXVolume(self):
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

            self.updated_dexVolume = fileInfo.stat()
            print('>>>> DEX volume data loaded from csv-file <<<<')


    #### MINUTELY DATA ####
    def loadShortTermDEXPrice(self):
        ShortTermDEXPrice = pd.read_csv(self.dataPath+'LMPoolData_ShortTerm.csv',index_col=0)
        # self.dailyData = self.dailyData.merge(ShortTermDEXPrice, how='outer')

    #### load last Richlist ####
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