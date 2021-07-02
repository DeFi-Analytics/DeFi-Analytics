from .volume.volumeView import volumeViewClass
from .volume.volumeCallbacks import volumeCallbacksClass

from .coinprice.coinpriceView import coinpriceViewClass
from .coinprice.coinpriceCallbacks import coinpriceCallbacksClass

from .stability.stabilityView import stabilityViewClass
from .stability.stabilityCallbacks import stabilityCallbacksClass

class dexControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize volume classes
        self.volumeView = volumeViewClass()
        self.volumeCallbacks = volumeCallbacksClass(app)       # create callbacks on top level

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
            pageContent = self.volumeView.getVolumeContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["stability"]:
            # self.defichainAnalyticsModel.loadDEXVolume()
            pageContent = self.stabilityView.getStabilityContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)

        return pageContent
