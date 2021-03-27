from .overview.overviewView import overviewViewClass
from .overview.overviewCallbacks import overviewCallbacksClass

class generalControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize overview classes
        self.overviewView = overviewViewClass()
        self.overviewCallback = overviewCallbacksClass(self.defichainAnalyticsModel, self.overviewView, app)



    def getContent(self, entry):
        pageContent = None
        if entry in ['', "overview"]:
            self.defichainAnalyticsModel.loadSnapshotData()
            pageContent = self.overviewView.getOverviewContent(self.defichainAnalyticsModel.snapshotData,  self.defichainAnalyticsModel.figBackgroundImage)


        return pageContent
