import dash_html_components as html
from .addresses.addressesView import addressesViewClass
from .addresses.addressesCallbacks import addressesCallbacksClass

from .daa.daaView import daaViewClass
from .daa.daaCallbacks import  daaCallbacksClass

from .coin.coinView import coinViewClass
from .coin.coinCallbacks import coinCallbacksClass

from .changeCoinAddresses.changeCoinAddressesView import changeCoinAddressesViewClass
from .changeCoinAddresses.changeCoinAddressesCallbacks import changeCoinAddressesCallbacksClass

from .coinsAddresses.coinsAddressesView import coinsAddressesViewClass
from .coinsAddresses.coinsAddressesCallbacks import coinsAddressesCallbacksClass

from .blocktime.blocktimeView import blocktimeViewClass
from .blocktime.blocktimeCallbacks import blocktimeCallbacksClass

from .transactions.transactionsView import transactionsViewClass
from .transactions.transactionsCallback import transactionsCallbacksClass



class blockchainControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize addresses classes
        self.addressesView = addressesViewClass()
        self.addressesCallbacks = addressesCallbacksClass(app)       # create callbacks on top level

        # initialize daa classes
        self.daaView = daaViewClass()
        self.daaCallbacks = daaCallbacksClass(app)

        # initialize coin classes
        self.coinView = coinViewClass()
        self.coinCallbacks = coinCallbacksClass(app)

        # initialize change classes
        self.changeCoinAddressesView = changeCoinAddressesViewClass()
        self.changeCoinAddressesCallbacks = changeCoinAddressesCallbacksClass(app)      # create callbacks on top level

        # initialize coins per addresses classes
        self.coinsAddressesView = coinsAddressesViewClass()
        self.coinsAddressesCallbacks = coinsAddressesCallbacksClass(self.defichainAnalyticsModel, self.coinsAddressesView, app)

        # initialize blocktime classes
        self.blocktimeView = blocktimeViewClass()
        self.blocktimeCallbacks = blocktimeCallbacksClass(app)

        # initialize transactions classes
        self.transactionsView = transactionsViewClass()
        self.transactionsCallbacks = transactionsCallbacksClass(app)

    def getContent(self, entry):
        pageContent = None
        if entry in ["", "addresses"]:
            self.defichainAnalyticsModel.loadExtractedRichlistData()
            pageContent = self.addressesView.getAddressContent(self.defichainAnalyticsModel.dailyData)
        elif entry in ["daa"]:
            self.defichainAnalyticsModel.loadDAAData()
            pageContent = self.daaView.getDAAContent(self.defichainAnalyticsModel.dailyData)
        elif entry in ["coin"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            self.defichainAnalyticsModel.loadExtractedRichlistData()
            pageContent = self.coinView.getCoinContent(self.defichainAnalyticsModel.dailyData)
        elif entry in ["changeCoinAdresses"]:
            self.defichainAnalyticsModel.loadExtractedRichlistData()
            pageContent = self.changeCoinAddressesView.getChangeCoinsAddressesContent(self.defichainAnalyticsModel.dailyData)
        elif entry in ["coinsAddresses"]:
            self.defichainAnalyticsModel.loadLastRichlist()
            pageContent = self.coinsAddressesView.getCoinsAddressesContent(self.defichainAnalyticsModel.lastRichlist)
        elif entry in ["blocktime"]:
            self.defichainAnalyticsModel.loadDailyBlocktimeData()
            pageContent = self.blocktimeView.getBlocktimeContent(self.defichainAnalyticsModel.dailyData)
        elif entry in ["transactions"]:
            self.defichainAnalyticsModel.loadDailyBlocktimeData()
            pageContent = self.transactionsView.getTransactionsContent(self.defichainAnalyticsModel.dailyData)

        return pageContent


