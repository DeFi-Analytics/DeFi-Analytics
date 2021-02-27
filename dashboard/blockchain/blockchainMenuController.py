import dash_html_components as html
from .addresses.addressesView import addressesViewClass
from .addresses.addressesCallbacks import addressesCallbacksClass

from .blocktime.blocktimeView import blocktimeViewClass

class blockchainControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize addresses classes
        self.addressesView = addressesViewClass()
        self.addressesCallbacks = addressesCallbacksClass()       # create callbacks on top level
        self.addressesCallbacks.register_callbacks(app)

        # initialize blocktime classes
        self.blocktimeView = blocktimeViewClass()

    def getContent(self, entry):
        if entry in ["", "addresses"]:
            self.defichainAnalyticsModel.loadExtractedRichlistData()
            pageContent = self.addressesView.getAddressContent(self.defichainAnalyticsModel.dailyData)
        elif entry in ["blocktime"]:
            self.defichainAnalyticsModel.loadDailyBlocktimeData()
            pageContent = self.blocktimeView.getBlocktimeContent(self.defichainAnalyticsModel.dailyData)


        return pageContent