import os
import pandas as pd

class defichainAnalyticsModelClass:
    def __init__(self):
        workDir = os.path.abspath(os.getcwd())
        self.dataPath = workDir[:-9] + '/data/'
        self.dailyData = pd.DataFrame(columns=columnsExtractedRichlist)
        self.lmData = None

    def loadDailyData(self):
        self.loadExtractedRichlistData()
        self.loadDailyTradingResults()

    def loadExtractedRichlistData(self):
        extractedRichlist = pd.read_csv(self.dataPath+'extractedDFIdata.csv',index_col=0)

        ind2Delete = self.dailyData.columns.intersection(extractedRichlist.columns)                                 # check if columns exist
        self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete exisiting columns to add new ones
        self.dailyData = self.dailyData.merge(extractedRichlist, how='outer',left_index=True,right_index=True)      # add new columns to daily table

        self.dailyData['nbOverall'] =self.dailyData['nbMnId'] +self.dailyData['nbOtherId'] +1

    def loadDailyTradingResults(self):
        dailyTradingResults = pd.read_csv(self.dataPath+'dailyTradingResultsDEX.csv',index_col=0)

        ind2Delete = self.dailyData.columns.intersection(dailyTradingResults.columns)                               # check if columns exist
        self.dailyData.drop(columns=ind2Delete, inplace=True)                                                       # delete exisiting columns to add new ones
        self.dailyData = self.dailyData.merge(dailyTradingResults, how='outer',left_index=True,right_index=True)    # add new columns to daily table


    def loadShortTermDEXPrice(self):
        ShortTermDEXPrice = pd.read_csv(self.dataPath+'LMPoolData_ShortTerm.csv',index_col=0)
        self.dailyData = self.dailyData.merge(ShortTermDEXPrice, how='outer')