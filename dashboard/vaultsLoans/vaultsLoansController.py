
from .nbVaults.nbVaultsView import nbVaultsViewClass
from .nbVaults.nbVaultsCallbacks import nbVaultsCallbacksClass

from .tvl.tvlView import tvlVaultsViewClass
from .tvl.tvlCallbacks import tvlVaultsCallbacksClass

from .prices.pricesView import pricesDTokenViewClass
from .prices.pricesCallbacks import pricesDTokenCallbacksClass

from .nbDToken.nbDTokenView import nbDTokenViewClass
from .nbDToken.nbDTokenCallbacks import nbDTokenCallbacksClass

from .interest.interestView import interestViewClass
from .interest.interestCallbacks import interestCallbacksClass

from .burnedDFI.burnedDFIView import burnedDFIViewClass
from .burnedDFI.burnedDFICallbacks import burnedDFICallbacksClass

class vaultsLoansControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize nbVaults classes
        self.nbVaultsView = nbVaultsViewClass()
        self.nbVaultsCallbacks = nbVaultsCallbacksClass(app)

        # initialize tvlVaults classes
        self.tvlVaultsView = tvlVaultsViewClass()
        self.tvlVaultsCallbacksClass = tvlVaultsCallbacksClass(self.defichainAnalyticsModel, self.tvlVaultsView, app)

        # initialize tvlVaults classes
        self.pricesDTokenView = pricesDTokenViewClass()
        self.pricesDTokenCallbacks = pricesDTokenCallbacksClass(self.defichainAnalyticsModel, self.pricesDTokenView, app)

        # initialize tvlVaults classes
        self.nbDTokenView = nbDTokenViewClass()
        self.nbDTokenCallbacks = nbDTokenCallbacksClass(self.defichainAnalyticsModel, self.nbDTokenView, app)

        # initialize interest classes
        self.interestView = interestViewClass()
        self.interestCallbacks = interestCallbacksClass(self.defichainAnalyticsModel, self.interestView, app)

        # initialize burned DFI classes
        self.burnedDFIView = burnedDFIViewClass()
        self.burnedDFICallbacks = burnedDFICallbacksClass(app)

    def getContent(self, entry):
        pageContent = None
        if entry in ["", "nbVaults"]:
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.nbVaultsView.getnbVaultsContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry == 'tvlVaults':
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.tvlVaultsView.getTVLContent()
        elif entry == 'dTokenPrices':
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.pricesDTokenView.getPricesDTokenContent()
        elif entry == 'nbDToken':
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.nbDTokenView.getnbDTokenContent()
        elif entry == 'interest':
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.interestView.getInterestContent()
        elif entry in ["", "burnedDFI"]:
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.burnedDFIView.getBurnedDFIContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)

        return pageContent