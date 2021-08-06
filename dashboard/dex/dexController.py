from .volume24hr .volumeView24hr import volume24hrViewClass
from .volume24hr.volume24hrCallbacks import volume24hrCallbacksClass

from .volume.volumeView import volumeViewClass
from .volume.volumeCallbacks import volumeCallbacksClass

from .coinprice.coinpriceView import coinpriceViewClass
from .coinprice.coinpriceCallbacks import coinpriceCallbacksClass

from .stability.stabilityView import stabilityViewClass
from .stability.stabilityCallbacks import stabilityCallbacksClass

from .slippage.slippageView import slippageViewClass
from .slippage.slippageCallbacks import slippageCallbacksClass

class dexControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize volume classes
        self.volume24hrView = volume24hrViewClass()
        self.volume24hrCallbacks = volume24hrCallbacksClass(app)       # create callbacks on top level

        # initialize volume classes
        self.volumeView = volumeViewClass()
        self.volumeCallbacks = volumeCallbacksClass(self.defichainAnalyticsModel, self.volumeView, app)

        # initialize coinprice classes
        self.coinpriceView = coinpriceViewClass()
        self.coinpriceCallbacks = coinpriceCallbacksClass(self.defichainAnalyticsModel, self.coinpriceView, app)      # create callbacks on top level

        # initialize price stability classes
        self.stabilityView = stabilityViewClass()
        self.stabilityCallbacks = stabilityCallbacksClass(self.defichainAnalyticsModel, self.stabilityView, app)

        # initialize price stability classes
        self.slippageView = slippageViewClass()
        self.slippageCallbacks = slippageCallbacksClass(self.defichainAnalyticsModel, self.slippageView, app)

    def getContent(self,entry):
        pageContent = None
        if entry in ["", "coinPrices"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            pageContent = self.coinpriceView.getCoinpriceContent()
        elif entry in ["volume"]:
            self.defichainAnalyticsModel.loadHourlyDEXTrades()
            pageContent = self.volumeView.getVolumeContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["24hrVolume"]:
            self.defichainAnalyticsModel.loadDEXVolume()
            pageContent = self.volume24hrView.getVolume24hrContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["stability"]:
            pageContent = self.stabilityView.getStabilityContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["slippage"]:
            pageContent = self.slippageView.getSlippageContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)

        return pageContent
