from .fees.feesView import feesViewClass
from .fees.feesCallbacks import feesCallbacksClass

from .token.tokenView import tokenViewClass
from .token.tokenCallbacks import tokenCallbacksClass

class dmcControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize fees classes
        self.feesView = feesViewClass()
        self.feesCallbacks = feesCallbacksClass(self.defichainAnalyticsModel, self.feesView, app)

        # initialize token classes
        self.tokenView = tokenViewClass()
        self.tokenCallbacks = tokenCallbacksClass(self.defichainAnalyticsModel, self.tokenView, app)

    def getContent(self, entry):
        pageContent = None
        if entry in ["", "dmcFees"]:
            self.defichainAnalyticsModel.loadDMCFeesData()
            pageContent = self.feesView.getFeesContent()
        elif entry == 'dmcToken':
            self.defichainAnalyticsModel.loadDMCTokenData

            colNames = self.defichainAnalyticsModel.hourlyData.columns
            availableToken = colNames.str.contains('DMCtoken_DVM') & ~colNames.str.contains('v1') & ~colNames.str.contains('DFI') & ~colNames.str.contains('dUSD') & ~colNames.str.contains('BURN')
            listAvailableTokens = ['DFI', 'DUSD'] + colNames[availableToken].sort_values().str[13:].to_list()
            pageContent = self.tokenView.getTokensContent(listAvailableTokens)

        return pageContent