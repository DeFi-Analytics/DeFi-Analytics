from .fees.feesView import feesViewClass
from .fees.feesCallbacks import feesCallbacksClass

from .tvl.tvlView import tvlViewClass

class liquidityMiningControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize fees classes
        self.feesView = feesViewClass()
        self.feesCallback = feesCallbacksClass(self.defichainAnalyticsModel, self.feesView, app)

        # initialize tvl classes
        self.tvlView = tvlViewClass()
        # self.feesCallback = feesCallbacksClass(self.defichainAnalyticsModel, self.feesView, app)

    def getContent(self, entry):
        pageContent = None
        if entry in ["fees"]:
            self.defichainAnalyticsModel.loadDailyTradingData()
            pageContent = self.feesView.getFeesContent(self.defichainAnalyticsModel.dailyData)
        if entry in ["tvl"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            pageContent = self.tvlView.getTVLContent(self.defichainAnalyticsModel.hourlyData)

        return pageContent