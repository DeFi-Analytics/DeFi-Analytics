
from .nbVaults.nbVaultsView import nbVaultsViewClass
from .nbVaults.nbVaultsCallbacks import nbVaultsCallbacksClass

from .tvl.tvlView import tvlVaultsViewClass
from .tvl.tvlCallbacks import tvlVaultsCallbacksClass

from .prices.pricesView import pricesDTokenViewClass
from .prices.pricesCallbacks import pricesDTokenCallbacksClass

from .premium.premiumView import premiumDTokenViewClass
from .premium.premiumCallbacks import premiumCallbacksClass

from .nbDToken.nbDTokenView import nbDTokenViewClass
from .nbDToken.nbDTokenCallbacks import nbDTokenCallbacksClass

from .ratioAlgoLoans.ratioAlgoLoansView import ratioAlgoLoansViewClass
from .ratioAlgoLoans.ratioAlgoLoansCallbacks import  ratioAlgoLoansCallbacksClass

from .interest.interestView import interestViewClass
from .interest.interestCallbacks import interestCallbacksClass

from .burnedDFI.burnedDFIView import burnedDFIViewClass
from .burnedDFI.burnedDFICallbacks import burnedDFICallbacksClass

from .scheme.schemeView import schemeViewClass
from .scheme.schemeCallbacks import schemeCallbacksClass

from .dUSDMeasures.dUSDMeasuresView import dUSDMeasuresViewClass

class vaultsLoansControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize nbVaults classes
        self.nbVaultsView = nbVaultsViewClass()
        self.nbVaultsCallbacks = nbVaultsCallbacksClass(app)

        # initialize tvlVaults classes
        self.tvlVaultsView = tvlVaultsViewClass()
        self.tvlVaultsCallbacksClass = tvlVaultsCallbacksClass(self.defichainAnalyticsModel, self.tvlVaultsView, app)

        # initialize prices classes
        self.pricesDTokenView = pricesDTokenViewClass()
        self.pricesDTokenCallbacks = pricesDTokenCallbacksClass(self.defichainAnalyticsModel, self.pricesDTokenView, app)

        # initialize premium classes
        self.premiumDTokenView = premiumDTokenViewClass()
        self.premiumDTokenCallbacks = premiumCallbacksClass(app)

        # initialize nb Token classes
        self.nbDTokenView = nbDTokenViewClass()
        self.nbDTokenCallbacks = nbDTokenCallbacksClass(self.defichainAnalyticsModel, self.nbDTokenView, app)

        # initialize ratio classes
        self.ratioAlgoLoansView = ratioAlgoLoansViewClass()
        self.ratioAlgoLoansCallbacks = ratioAlgoLoansCallbacksClass(self.defichainAnalyticsModel, self.ratioAlgoLoansView, app)

        # initialize interest classes
        self.interestView = interestViewClass()
        self.interestCallbacks = interestCallbacksClass(self.defichainAnalyticsModel, self.interestView, app)

        # initialize burned DFI classes
        self.burnedDFIView = burnedDFIViewClass()
        self.burnedDFICallbacks = burnedDFICallbacksClass(app)

        # initialize scheme classes
        self.schemeView = schemeViewClass()
        self.schemeCallbacks = schemeCallbacksClass(self.defichainAnalyticsModel, self.schemeView, app)

        # initialize dUSD measures classes
        self.dUSDMeasuresView = dUSDMeasuresViewClass()
        # self.schemeCallbacks = schemeCallbacksClass(self.defichainAnalyticsModel, self.schemeView, app)

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
            self.defichainAnalyticsModel.loadDFIPFuturesData()
            pageContent = self.nbDTokenView.getnbDTokenContent()
        elif entry == 'partAlgoCirc':
            self.defichainAnalyticsModel.loadVaultData()
            self.defichainAnalyticsModel.loadDFIPFuturesData()
            pageContent = self.ratioAlgoLoansView.getRatioAlgoLoansContent()
        elif entry == 'interest':
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.interestView.getInterestContent()
        elif entry == 'burnedDFI':
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.burnedDFIView.getBurnedDFIContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry == 'scheme':
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.schemeView.getSchemeContent()
        elif entry == 'premium':
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.premiumDTokenView.getPremiumDTokenContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry == 'dUSDMeasures':
            # self.defichainAnalyticsModel.loadHourlyDEXdata()
            # self.defichainAnalyticsModel.loadVaultData()
            pageContent = self.dUSDMeasuresView.getdUSDMeasuresContent(self.defichainAnalyticsModel.hourlyData, self.defichainAnalyticsModel.figBackgroundImage)

        return pageContent