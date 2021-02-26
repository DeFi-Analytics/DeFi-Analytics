import dash_html_components as html
from .fees.feesView import feesViewClass
# from .addresses.addressesCallbacks import addressesCallbacksClass

class liquidityMiningControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize fees classes
        self.feesView = feesViewClass()
        # self.addressesCallbacks = addressesCallbacksClass()       # create callbacks on top level
        # self.addressesCallbacks.register_callbacks(app)


    def getContent(self,entry):
        if entry in ["", "fees"]:
            return self.feesView.getAddressContent(self.defichainAnalyticsModel.dailyData)