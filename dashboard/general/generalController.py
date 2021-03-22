from .overview.overviewView import overviewViewClass

class generalControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize overview classes
        self.overviewView = overviewViewClass()
        #self.feesCallback = feesCallbacksClass(self.defichainAnalyticsModel, self.feesView, app)



    def getContent(self, entry):
        pageContent = None
        if entry in ['', "overview"]:
            self.defichainAnalyticsModel.loadSnapshotData()
            pageContent = self.overviewView.getOverviewContent(self.defichainAnalyticsModel.snapshotData,  self.defichainAnalyticsModel.figBackgroundImage)


        return pageContent
