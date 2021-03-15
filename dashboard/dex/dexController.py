from .volume.volumeView import volumeViewClass
from .volume.volumeCallbacks import volumeCallbacksClass

class dexControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize fees classes
        self.volumeView = volumeViewClass()
        self.volumeCallbacks = volumeCallbacksClass(app)       # create callbacks on top level



    def getContent(self,entry):
        if entry in ["", "volume"]:
            return self.volumeView.getVolumeContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
