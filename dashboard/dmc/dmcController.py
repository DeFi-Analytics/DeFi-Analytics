from .fees.feesView import feesViewClass
from .fees.feesCallbacks import feesCallbacksClass

class dmcControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize tvlVaults classes
        self.feesView = feesViewClass()
        self.feesCallbacksClass = feesCallbacksClass(self.defichainAnalyticsModel, self.feesView, app)



    def getContent(self, entry):
        pageContent = None
        if entry in ["", "dmcFees"]:
            self.defichainAnalyticsModel.loadDMCFeesData()
            pageContent = self.feesView.getFeesContent()
        # elif entry == 'token':
            # self.defichainAnalyticsModel.loadHourlyDEXdata()
            # self.defichainAnalyticsModel.loadVaultData()
            # pageContent = self.tvlVaultsView.getTVLContent()

        return pageContent