# from .overview.overviewView import overviewViewClass
# from .overview.overviewCallbacks import overviewCallbacksClass

from .liquidity.liquidityView import liquidityViewClass
from .liquidity.liquidityCallbacks import liquiditiyCallbacksClass

class bscbridgeControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize liquidity classes
        self.liquidityView = liquidityViewClass()
        self.liquiditiyCallbacks = liquiditiyCallbacksClass( app)

    def getContent(self, entry):
        pageContent = None
        if entry in ['', "liquidityBridge"]:
            self.defichainAnalyticsModel.loadBSCBridgeData()
            pageContent = self.liquidityView.getLiquidityContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)

        return pageContent
