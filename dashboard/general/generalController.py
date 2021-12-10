from .overview.overviewView import overviewViewClass
from .overview.overviewCallbacks import overviewCallbacksClass

from .marketcap.marketcapView import marketcapViewClass
from .marketcap.marketcapCallbacks import marketcapCallbacksClass

from .overallTVL.overallTVLView import overallTVLViewClass
from .overallTVL.overallTVLCallbacks import overallTVLCallbacksClass

class generalControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize overview classes
        self.overviewView = overviewViewClass()
        self.overviewCallback = overviewCallbacksClass(self.defichainAnalyticsModel, self.overviewView, app)

        # initialize marketcap classes
        self.marketcapView = marketcapViewClass()
        self.marketcapCallback = marketcapCallbacksClass(self.defichainAnalyticsModel, self.marketcapView, app)

        # initialize marketcap classes
        self.overallTVLView = overallTVLViewClass()
        self.overallTVLCallback = overallTVLCallbacksClass(self.defichainAnalyticsModel, self.overallTVLView, app)

    def getContent(self, entry):
        pageContent = None
        if entry in ['', "overview"]:
            self.defichainAnalyticsModel.loadSnapshotData()
            pageContent = self.overviewView.getOverviewContent(self.defichainAnalyticsModel.snapshotData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["marketcap"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            self.defichainAnalyticsModel.loadDailyTradingData()
            self.defichainAnalyticsModel.loadExtractedRichlistData()
            pageContent = self.marketcapView.getMarketcapContent(self.defichainAnalyticsModel.dailyData,  self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["overallTVL"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            self.defichainAnalyticsModel.loadExtractedRichlistData()
            self.defichainAnalyticsModel.loadDailyTradingData()
            self.defichainAnalyticsModel.calcOverallTVLdata()
            pageContent = self.overallTVLView.getOverallTVLContent()

        return pageContent
