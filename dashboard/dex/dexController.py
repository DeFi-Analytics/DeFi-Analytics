import dash_html_components as html
# from .addresses.addressesView import addressesViewClass
# from .addresses.addressesCallbacks import addressesCallbacksClass

from .volume.volumeView import volumeViewClass


class dexControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize fees classes
        self.volumeView = volumeViewClass()
        # self.addressesCallbacks = addressesCallbacksClass()       # create callbacks on top level



    def getContent(self,entry):
        if entry in ["", "volume"]:
            return self.volumeView.getVolumeContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
