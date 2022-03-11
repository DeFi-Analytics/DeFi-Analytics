from .fees.feesView import feesViewClass
from .fees.feesCallbacks import feesCallbacksClass

from .tvl.tvlView import tvlViewClass
from .tvl.tvlCallbacks import tvlCallbacksClass

from .liquidityToken.liquidityTokenView import liquidityTokenViewClass
from .liquidityToken.liquidityTokenCallbacks import liquidityTokenCallbacksClass

from .apr.aprView import aprViewClass
from .apr.aprCallbacks import aprCallbacksClass

class liquidityMiningControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize fees classes
        self.feesView = feesViewClass()
        self.feesCallbacks = feesCallbacksClass(self.defichainAnalyticsModel, self.feesView, app)

        # initialize tvl classes
        self.tvlView = tvlViewClass()
        self.tvlCallbacks = tvlCallbacksClass(self.defichainAnalyticsModel, self.tvlView, app)

        # initialize liquidity token classes
        self.liquidityTokenView = liquidityTokenViewClass()
        self.liquidityTokenCallbacks = liquidityTokenCallbacksClass(self.defichainAnalyticsModel, self.liquidityTokenView, app)

        # initialize apr classes
        self.aprView = aprViewClass()
        self.aprCallbacks = aprCallbacksClass(self.defichainAnalyticsModel, self.aprView, app)

    def getContent(self, entry):
        pageContent = None
        if entry in ["", "tvl"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            pageContent = self.tvlView.getTVLContent(self.defichainAnalyticsModel.hourlyData)
        elif entry in ["fees"]:
            self.defichainAnalyticsModel.loadDailyTradingData()
            pageContent = self.feesView.getFeesContent(self.defichainAnalyticsModel.dailyData)
        elif entry in ["liquidityToken"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            pageContent = self.liquidityTokenView.getLiquidityTokenContent(self.defichainAnalyticsModel.hourlyData)
        elif entry in ["apr"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            pageContent = self.aprView.getAPRContent()

        return pageContent

