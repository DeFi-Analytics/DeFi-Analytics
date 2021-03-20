from .twitter.twitterView import twitterViewClass


class socialmediaControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize volume classes
        self.twitterView = twitterViewClass()
        # self.cryptoTokenCallbacks = cryptoTokenCallbacksClass(self.defichainAnalyticsModel, self.cryptoTokenView, app)       # create callbacks on top level


    def getContent(self, entry):
        pageContent = None
        if entry in ["", "twitter"]:
            self.defichainAnalyticsModel.loadTwitterData()
            pageContent = self.twitterView.getTwitterContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)


        return pageContent