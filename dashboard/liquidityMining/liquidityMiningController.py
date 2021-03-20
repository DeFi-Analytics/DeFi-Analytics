from .fees.feesView import feesViewClass
from .fees.feesCallbacks import feesCallbacksClass

from .tvl.tvlView import tvlViewClass
from .tvl.tvlCallbacks import tvlCallbacksClass

from .liquidityToken.liquidityTokenView import liquidityTokenViewClass
from .liquidityToken.liquidityTokenCallbacks import liquidityTokenCallbacksClass

class liquidityMiningControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize fees classes
        self.feesView = feesViewClass()
        self.feesCallback = feesCallbacksClass(self.defichainAnalyticsModel, self.feesView, app)

        # initialize tvl classes
        self.tvlView = tvlViewClass()
        self.tvlCallbacksClass = tvlCallbacksClass(self.defichainAnalyticsModel, self.tvlView, app)

        # initialize liquidity token classes
        self.liquidityTokenView = liquidityTokenViewClass()
        self.liquidityTokenCallbacksClass = liquidityTokenCallbacksClass(self.defichainAnalyticsModel, self.liquidityTokenView, app)

    def getContent(self, entry):
        pageContent = None
        if entry in ["fees"]:
            self.defichainAnalyticsModel.loadDailyTradingData()
            pageContent = self.feesView.getFeesContent(self.defichainAnalyticsModel.dailyData)
        elif entry in ["tvl"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            pageContent = self.tvlView.getTVLContent(self.defichainAnalyticsModel.hourlyData)
        elif entry in ["liquidityToken"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            pageContent = self.liquidityTokenView.getLiquidityTokenContent(self.defichainAnalyticsModel.hourlyData)

        return pageContent

