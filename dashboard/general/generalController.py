from .overview.overviewView import overviewViewClass
from .overview.overviewCallbacks import overviewCallbacksClass

from .marketcap.marketcapView import marketcapViewClass
from .marketcap.marketcapCallbacks import marketcapCallbacksClass

from .overallTVL.overallTVLView import overallTVLViewClass
from .overallTVL.overallTVLCallbacks import overallTVLCallbacksClass

from .emission.emissionView import emissionViewClass
from .emission.emissionCallbacks import emissionCallbacksClass

from .inflation.inflationView import inflationViewClass
from .inflation.inflationCallbacks import inflationCallbacksClass

class generalControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize overview classes
        self.overviewView = overviewViewClass()
        self.overviewCallback = overviewCallbacksClass(self.defichainAnalyticsModel, self.overviewView, app)

        # initialize marketcap classes
        self.marketcapView = marketcapViewClass()
        self.marketcapCallback = marketcapCallbacksClass(self.defichainAnalyticsModel, self.marketcapView, app)

        # initialize overallTVL classes
        self.overallTVLView = overallTVLViewClass()
        self.overallTVLCallback = overallTVLCallbacksClass(self.defichainAnalyticsModel, self.overallTVLView, app)

        # initialize emission classes
        self.emissionView = emissionViewClass()
        self.emissionCallback = emissionCallbacksClass(self.defichainAnalyticsModel, self.emissionView, app)

        # initialize inflation classes
        self.inflationView = inflationViewClass()
        self.inflationCallbacks = inflationCallbacksClass(self.defichainAnalyticsModel, self.inflationView, app)

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
        elif entry in ["emission"]:
            self.defichainAnalyticsModel.loadEmissionRateData()
            self.defichainAnalyticsModel.loadExtractedRichlistData()
            pageContent = self.emissionView.getEmissionContent()
        elif entry in ["overallTVL"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            self.defichainAnalyticsModel.loadExtractedRichlistData()
            self.defichainAnalyticsModel.loadDailyTradingData()
            self.defichainAnalyticsModel.loadVaultData()
            self.defichainAnalyticsModel.calcOverallTVLdata()
            pageContent = self.overallTVLView.getOverallTVLContent()
        elif entry in ["inflation"]:
            self.defichainAnalyticsModel.loadEmissionRateData()
            self.defichainAnalyticsModel.loadDailyBlocktimeData()
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.inflationView.getInflationContent()

        return pageContent
