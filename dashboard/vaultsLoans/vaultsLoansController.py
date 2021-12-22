
from .nbVaults.nbVaultsView import nbVaultsViewClass
#from .fees.feesCallbacks import feesCallbacksClass

class vaultsLoansControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize daa classes
        self.nbVaultsView = nbVaultsViewClass()
        # self.daaCallbacks = daaCallbacksClass(app)

    def getContent(self, entry):
        pageContent = None
        if entry in ["", "nbVaults"]:
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.nbVaultsView.getnbVaultsContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)

        return pageContent