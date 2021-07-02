from .volume24hr .volumeView24hr import volume24hrViewClass
from .volume24hr.volume24hrCallbacks import volume24hrCallbacksClass

from .coinprice.coinpriceView import coinpriceViewClass
from .coinprice.coinpriceCallbacks import coinpriceCallbacksClass

from .stability.stabilityView import stabilityViewClass
from .stability.stabilityCallbacks import stabilityCallbacksClass

class dexControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize volume classes
        self.volume24hrView = volume24hrViewClass()
        self.volume24hrCallbacks = volume24hrCallbacksClass(app)       # create callbacks on top level

        # initialize coinprice classes
        self.coinpriceView = coinpriceViewClass()
        self.coinpriceCallbacks = coinpriceCallbacksClass(self.defichainAnalyticsModel, self.coinpriceView, app)      # create callbacks on top level

        # initialize price stability classes
        self.stabilityView = stabilityViewClass()
        self.stabilityCallbacks = stabilityCallbacksClass(self.defichainAnalyticsModel, self.stabilityView, app)

    def getContent(self,entry):
        pageContent = None
        if entry in ["", "coinPrices"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            pageContent = self.coinpriceView.getCoinpriceContent()
        elif entry in ["24hrVolume"]:
            self.defichainAnalyticsModel.loadDEXVolume()
            pageContent = self.volume24hrView.getVolume24hrContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["stability"]:
            # self.defichainAnalyticsModel.loadDEXVolume()
            pageContent = self.stabilityView.getStabilityContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)

        return pageContent
