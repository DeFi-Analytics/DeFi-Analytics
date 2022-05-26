# from .overview.overviewView import overviewViewClass
# from .overview.overviewCallbacks import overviewCallbacksClass

from .liquidity.liquidityView import liquidityViewClass
from .liquidity.liquidityCallbacks import liquiditiyCallbacksClass

from .nbBridgeSwaps.nbBridgeSwapsView import nbBridgeSwapsViewClass
from .nbBridgeSwaps.nbBridgeSwapsCallbacks import nbBridgeSwapsCallbacksClass

class bscbridgeControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize liquidity classes
        self.liquidityView = liquidityViewClass()
        self.liquiditiyCallbacks = liquiditiyCallbacksClass( app)

        # initialize nbSwaps classes
        self.nbBridgeSwapsView = nbBridgeSwapsViewClass()
        self.nbBridgeSwapsCallbacks = nbBridgeSwapsCallbacksClass(self.defichainAnalyticsModel, self.nbBridgeSwapsView, app)


    def getContent(self, entry):
        pageContent = None
        if entry in ['', "liquidityBridge"]:
            self.defichainAnalyticsModel.loadBSCBridgeData()
            pageContent = self.liquidityView.getLiquidityContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["nbSwapsBridge"]:
            self.defichainAnalyticsModel.loadBSCBridgeData()
            pageContent = self.nbBridgeSwapsView.getNbBrideSwapsContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)


        return pageContent
