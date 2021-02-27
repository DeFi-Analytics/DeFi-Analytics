import os
import pandas as pd
import pathlib

class defichainAnalyticsModelClass:
    def __init__(self):
        workDir = os.path.abspath(os.getcwd())
        self.dataPath = workDir[:-9] + '/data/'
        self.dailyData = pd.DataFrame()

        # last update of csv-files
        self.updated_extractedRichlist = None
        self.updated_tradingData = None
        self.updated_blocktime = None


    #### DAILY DATA #####
    def loadDailyData(self):
        self.loadExtractedRichlistData()
        self.loadDailyTradingData()
        self.loadDailyBlocktimeData()

    def loadExtractedRichlistData(self):
        dataPath = self.dataPath + 'extractedDFIdata.csv'
        fileInfo = pathlib.Path(dataPath)
        if fileInfo.stat() != self.updated_extractedRichlist:
            extractedRichlist = pd.read_csv(self.dataPath+'extractedDFIdata.csv',index_col=0)

            ind2Delete = self.dailyData.columns.intersection(extractedRichlist.columns)                                 # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete exisiting columns to add new ones
            self.dailyData = self.dailyData.merge(extractedRichlist, how='outer',left_index=True,right_index=True)      # add new columns to daily table

            self.dailyData['nbOverall'] =self.dailyData['nbMnId'] +self.dailyData['nbOtherId'] +1

            self.updated_extractedRichlist = fileInfo.stat()
            print('>>>> Richlist data loaded from csv-file <<<<')

    def loadDailyTradingData(self):
        dataPath = self.dataPath + 'dailyTradingResultsDEX.csv'
        fileInfo = pathlib.Path(dataPath)
        if fileInfo.stat() != self.updated_tradingData:
            dailyTradingResults = pd.read_csv(self.dataPath+'dailyTradingResultsDEX.csv',index_col=0)

            ind2Delete = self.dailyData.columns.intersection(dailyTradingResults.columns)                               # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete exisiting columns to add new ones
            self.dailyData = self.dailyData.merge(dailyTradingResults, how='outer',left_index=True,right_index=True)    # add new columns to daily table

            self.updated_tradingData = fileInfo.stat()
            print('>>>> Trading data loaded from csv-file <<<<')

    def loadDailyBlocktimeData(self):
        dataPath = self.dataPath + 'BlockListStatistics.csv'
        fileInfo = pathlib.Path(dataPath)
        if fileInfo.stat() != self.updated_blocktime:
            dailyBlocktimeData = pd.read_csv(dataPath, index_col=0)
            dailyBlocktimeData['tps'] = dailyBlocktimeData['txCount'] / (24 * 60 * 60)

            ind2Delete = self.dailyData.columns.intersection(dailyBlocktimeData.columns)                                # check if columns exist
            self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete exisiting columns to add new ones
            self.dailyData = self.dailyData.merge(dailyBlocktimeData, how='outer', left_index=True,right_index=True)    # add new columns to daily table

            self.updated_blocktime = fileInfo.stat()
            print('>>>> Blocktime data loaded from csv-file <<<<')



    #### MINUTELY DATA ####
    def loadShortTermDEXPrice(self):
        ShortTermDEXPrice = pd.read_csv(self.dataPath+'LMPoolData_ShortTerm.csv',index_col=0)
        # self.dailyData = self.dailyData.merge(ShortTermDEXPrice, how='outer')