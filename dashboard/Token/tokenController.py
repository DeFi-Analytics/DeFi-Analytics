# from .volume.volumeView import volumeViewClass
# from .volume.volumeCallbacks import volumeCallbacksClass



class tokenControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize volume classes
        # self.volumeView = volumeViewClass()
        # self.volumeCallbacks = volumeCallbacksClass(app)       # create callbacks on top level


    def getContent(self,entry):
        pageContent = None
        # if entry in ["", "volume"]:
        #     self.defichainAnalyticsModel.loadDEXVolume()
        #     pageContent = self.volumeView.getVolumeContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)


        return pageContent