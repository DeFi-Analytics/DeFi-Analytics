from .twitter.twitterView import twitterViewClass
from .twitter.twitterCallbacks import twitterCallbacksClass

from .follower.followerView import followerViewClass
from .follower.followerCallbacks import followerCallbacksClass

from .analytics.analyticsView import analyticsViewClass

from .income.incomeView import incomeViewClass

from .portfolio.portfolioView import portfolioViewClass

from .promo.promoView import promoViewClass
from .promo.promoCallbacks import promoCallbacksClass

from .mnMonitor.mnMonitorView import mnMonitorViewClass

from .dfx.dfxViews import dfxViewClass
from .dfx.dfxCallbacks import dfxCallbacksClass

class communityControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.app = app

        # initialize twitter classes
        self.twitterView = twitterViewClass()
        self.twitterCallbacks = twitterCallbacksClass(app)       # create callbacks on top level

        # initialize twitter follower classes
        self.followerView = followerViewClass()
        self.followerCallbacks = followerCallbacksClass(self.defichainAnalyticsModel, self.followerView, app)       # create callbacks on top level

        # initialize visits analytics classes
        self.analyticsView = analyticsViewClass()

        # initialize visits income classes
        self.incomeView = incomeViewClass()

        # initialize portfolio downloads classes
        self.portfolioView = portfolioViewClass()

        # initialize defichain promo classes
        self.promoView = promoViewClass()
        self.promoCallbacks = promoCallbacksClass(self.defichainAnalyticsModel, self.promoView, app)

        # initialize MN monitor classes
        self.mnMonitorView = mnMonitorViewClass()

        # initialize defichain promo classes
        self.dfxView = dfxViewClass()
        self.dfxCallbacks = dfxCallbacksClass(self.defichainAnalyticsModel, self.dfxView, app)

    def getContent(self, entry):
        pageContent = None
        if entry in ["", "twitter"]:
            self.defichainAnalyticsModel.loadTwitterData()
            pageContent = self.twitterView.getTwitterContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["follower"]:
            self.defichainAnalyticsModel.loadTwitterFollowerData()
            pageContent = self.followerView.getTwitterFollowerContent()
        elif entry in ["analytics"]:
            self.defichainAnalyticsModel.loadAnalyticsVisitsData()
            pageContent = self.analyticsView.getAnalyticsContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["income"]:
            self.defichainAnalyticsModel.loadIncomeVisitsData()
            pageContent = self.incomeView.getIncomeContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["portfolio"]:
            self.defichainAnalyticsModel.loadPortfolioDownloads()
            pageContent = self.portfolioView.getPortfolioContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["promo"]:
            self.defichainAnalyticsModel.loadPromoDatabase()
            pageContent = self.promoView.getPromoContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["mnmonitor"]:
            self.defichainAnalyticsModel.loadMNMonitorDatabase()
            pageContent = self.mnMonitorView.getmnMonitorContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["dfx"]:
            self.defichainAnalyticsModel.loadDFXdata()
            pageContent = self.dfxView.getDFXContent()

        return pageContent