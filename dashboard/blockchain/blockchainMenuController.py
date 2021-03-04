import dash_html_components as html
from .addresses.addressesView import addressesViewClass
from .addresses.addressesCallbacks import addressesCallbacksClass

from .daa.daaView import daaViewClass
from .daa.daaCallbacks import  daaCallbacksClass

from .coin.coinView import coinViewClass
from .coin.coinCallbacks import coinCallbacksClass

from .blocktime.blocktimeView import blocktimeViewClass
from .blocktime.blocktimeCallbacks import blocktimeCallbacksClass

from .changeCoinAddresses.changeCoinAddressesView import changeCoinAddressesViewClass
from .changeCoinAddresses.changeCoinAddressesCallbacks import changeCoinAddressesCallbacksClass



class blockchainControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize addresses classes
        self.addressesView = addressesViewClass()
        self.addressesCallbacks = addressesCallbacksClass()       # create callbacks on top level

        # initialize daa classes
        self.daaView = daaViewClass()
        self.daaCallbacks = daaCallbacksClass()

        # initialize coin classes
        self.coinView = coinViewClass()
        self.coinCallbacks = coinCallbacksClass()

        # initialize blocktime classes
        self.blocktimeView = blocktimeViewClass()
        self.blocktimeCallbacks = blocktimeCallbacksClass()

        # initialize change classes
        self.changeCoinAddressesView = changeCoinAddressesViewClass()
        self.changeCoinAddressesCallbacks = changeCoinAddressesCallbacksClass()       # create callbacks on top level

    def getContent(self, entry):
        pageContent = None
        if entry in ["", "addresses"]:
            self.defichainAnalyticsModel.loadExtractedRichlistData()
            pageContent = self.addressesView.getAddressContent(self.defichainAnalyticsModel.dailyData)
        elif entry in ["daa"]:
            self.defichainAnalyticsModel.loadExtractedRichlistData()
            pageContent = self.daaView.getDAAContent(self.defichainAnalyticsModel.dailyData)
        elif entry in ["coin"]:
            self.defichainAnalyticsModel.loadHourlyDEXdata()
            self.defichainAnalyticsModel.loadExtractedRichlistData()
            pageContent = self.coinView.getCoinContent(self.defichainAnalyticsModel.dailyData)
        elif entry in ["changeCoinAdresses"]:
            self.defichainAnalyticsModel.loadExtractedRichlistData()
            pageContent = self.changeCoinAddressesView.getChangeCoinsAddressesContent(self.defichainAnalyticsModel.dailyData)
        elif entry in ["blocktime"]:
            self.defichainAnalyticsModel.loadDailyBlocktimeData()
            pageContent = self.blocktimeView.getBlocktimeContent(self.defichainAnalyticsModel.dailyData)

        return pageContent

    def registerCallbacks(self, app):
        self.addressesCallbacks.register_callbacks(self.app)
        self.daaCallbacks.register_callbacks(self.app)
        self.coinCallbacks.register_callbacks(self.app)
        self.changeCoinAddressesCallbacks.register_callbacks(self.app)
        self.blocktimeCallbacks.register_callbacks(self.app)
