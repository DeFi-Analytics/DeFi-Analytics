from .fees.feesView import feesViewClass
from .fees.feesCallbacks import feesCallbacksClass


class liquidityMiningControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize fees classes
        self.feesView = feesViewClass()
        self.feesCallback = feesCallbacksClass(self.defichainAnalyticsModel, self.feesView, app)


    def getContent(self, entry):
        if entry in ["fees"]:
            return self.feesView.getAddressContent(self.defichainAnalyticsModel.dailyData)
