import dash_html_components as html
# from .addresses.addressesView import addressesViewClass
# from .addresses.addressesCallbacks import addressesCallbacksClass

class blockchainControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize fees classes
        # self.addressesView = addressesViewClass()
        # self.addressesCallbacks = addressesCallbacksClass()       # create callbacks on top level
        # self.addressesCallbacks.register_callbacks(app)


    def getContent(self,entry):
        if entry in ["", "fees"]:
            # return self.coinpricesView.getAddressContent(self.defichainAnalyticsModel.dailyData)
