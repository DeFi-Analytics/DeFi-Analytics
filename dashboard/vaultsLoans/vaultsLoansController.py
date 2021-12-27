
from .nbVaults.nbVaultsView import nbVaultsViewClass
from .nbVaults.nbVaultsCallbacks import nbVaultsCallbacksClass

from .tvl.tvlView import tvlVaultsViewClass
from .tvl.tvlCallbacks import tvlVaultsCallbacksClass

class vaultsLoansControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize nbVaults classes
        self.nbVaultsView = nbVaultsViewClass()
        self.nbVaultsCallbacks = nbVaultsCallbacksClass(app)

        # initialize tvlVaults classes
        self.tvlVaultsView = tvlVaultsViewClass()
        self.tvlVaultsCallbacksClass = tvlVaultsCallbacksClass(self.defichainAnalyticsModel, self.tvlVaultsView, app)


    def getContent(self, entry):
        pageContent = None
        if entry in ["", "nbVaults"]:
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.nbVaultsView.getnbVaultsContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry == 'tvlVaults':
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.tvlVaultsView.getTVLContent(self.defichainAnalyticsModel.hourlyData)

        return pageContent