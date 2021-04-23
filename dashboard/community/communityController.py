from .twitter.twitterView import twitterViewClass
from .twitter.twitterCallbacks import twitterCallbacksClass

from .follower.followerView import followerViewClass
from .follower.followerCallbacks import followerCallbacksClass

class communityControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize volume classes
        self.twitterView = twitterViewClass()
        self.twitterCallbacks = twitterCallbacksClass(app)       # create callbacks on top level

        # initialize volume classes
        self.followerView = followerViewClass()
        self.followerCallbacks = followerCallbacksClass(self.defichainAnalyticsModel, self.followerView, app)       # create callbacks on top level

    def getContent(self, entry):
        pageContent = None
        if entry in ["", "twitter"]:
            self.defichainAnalyticsModel.loadTwitterData()
            pageContent = self.twitterView.getTwitterContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["follower"]:
            self.defichainAnalyticsModel.loadTwitterFollowerData()
            pageContent = self.followerView.getTwitterFollowerContent()

        return pageContent