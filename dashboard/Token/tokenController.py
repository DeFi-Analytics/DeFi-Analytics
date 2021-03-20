from .cryptos.cryptoTokenView import crpytoTokenViewClass
from .cryptos.cryptoTokenCallbacks import cryptoTokenCallbacksClass


class tokenControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize volume classes
        self.cryptoTokenView = crpytoTokenViewClass()
        self.cryptoTokenCallbacks = cryptoTokenCallbacksClass(self.defichainAnalyticsModel, self.cryptoTokenView, app)       # create callbacks on top level


    def getContent(self,entry):
        pageContent = None
        if entry in ["", "cryptosDAT"]:
            self.defichainAnalyticsModel.loadTokenCrypto()
            pageContent = self.cryptoTokenView.getTokenContent()


        return pageContent
