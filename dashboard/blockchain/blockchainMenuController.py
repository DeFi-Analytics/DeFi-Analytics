import dash_html_components as html
from .addresses.addressesView import addressesViewClass
from .addresses.addressesCallbacks import addressesCallbacksClass

class blockchainControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize addresses classes
        self.addressesView = addressesViewClass()
        self.addressesCallbacks = addressesCallbacksClass()       # create callbacks on top level
        self.addressesCallbacks.register_callbacks(app)


    def getContent(self,entry):
        if entry in ["", "addresses"]:
            return self.addressesView.getAddressContent(self.defichainAnalyticsModel.dailyData)
        elif entry == "/page-1/2":
            return html.P("This is the content of page 1.2. Yay!")