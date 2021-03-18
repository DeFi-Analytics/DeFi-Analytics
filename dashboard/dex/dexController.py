from .volume.volumeView import volumeViewClass
from .volume.volumeCallbacks import volumeCallbacksClass

from .coinprice.coinpriceView import coinpriceViewClass
from .coinprice.coinpriceCallbacks import coinpriceCallbacksClass

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

    def getContent(self,entry):
        pageContent = None
        if entry in ["", "volume"]:
            self.defichainAnalyticsModel.loadDEXVolume()
            pageContent = self.volumeView.getVolumeContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["coinprices"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            pageContent = self.coinpriceView.getCoinpriceContent()

        return pageContent
