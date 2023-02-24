from .twitter.twitterView import twitterViewClass
from .twitter.twitterCallbacks import twitterCallbacksClass

from .follower.followerView import followerViewClass
from .follower.followerCallbacks import followerCallbacksClass

from .reddit.redditView import redditViewClass
from .reddit.redditCallbacks import redditCallbacksClass

from .analytics.analyticsView import analyticsViewClass

from .income.incomeView import incomeViewClass

from .portfolio.portfolioView import portfolioViewClass

from .mnMonitor.mnMonitorView import mnMonitorViewClass

from .dfx.dfxViews import dfxViewClass
from .dfx.dfxCallbacks import dfxCallbacksClass

from .dfiSignal.dfiSignalView import dfiSignalViewClass
from .dfiSignal.dfiSignalCallbacks import dfiSignalCallbacksClass

from .dobby.dobbyViews import dobbyViewClass
from .dobby.dobbyCallbacks import dobbyCallbacksClass

from .cfp.cfpView import cfpViewClass
from .cfp.cfpCallbacks import cfpCallbacksClass

from .lock.lockViews import lockViewClass
from .lock.lockCallbacks import lockCallbacksClass



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

        # initialize reddit members classes
        self.redditView = redditViewClass()
        self.redditCallbacks = redditCallbacksClass(self.defichainAnalyticsModel, self.redditView, app)

        # initialize visits analytics classes
        self.analyticsView = analyticsViewClass()

        # initialize visits income classes
        self.incomeView = incomeViewClass()

        # initialize portfolio downloads classes
        self.portfolioView = portfolioViewClass()

        # initialize MN monitor classes
        self.mnMonitorView = mnMonitorViewClass()

        # initialize DFX classes
        self.dfxView = dfxViewClass()
        self.dfxCallbacks = dfxCallbacksClass(self.defichainAnalyticsModel, self.dfxView, app)

        # initialize DFI-signal class
        self.dfiSignalView = dfiSignalViewClass()
        self.dfiSignalCallbacks = dfiSignalCallbacksClass(self.defichainAnalyticsModel, self.dfiSignalView, app)

        # initialize dobby classes
        self.dobbyView = dobbyViewClass()
        self.dobbyCallbacks = dobbyCallbacksClass(self.defichainAnalyticsModel, self.dobbyView, app)

        # initialize cfp classes
        self.cfpView = cfpViewClass()
        self.cfpViewCallbacks = cfpCallbacksClass(self.defichainAnalyticsModel, self.cfpView, app)

        # initialize LOCK classes
        self.lockView = lockViewClass()
        self.lockCallbacks = lockCallbacksClass(self.defichainAnalyticsModel, self.lockView, app)

    def getContent(self, entry):
        pageContent = None
        if entry in ["", "twitter"]:
            self.defichainAnalyticsModel.loadTwitterData()
            pageContent = self.twitterView.getTwitterContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["follower"]:
            self.defichainAnalyticsModel.loadTwitterFollowerData()
            pageContent = self.followerView.getTwitterFollowerContent()
        elif entry in ["reddit"]:
            self.defichainAnalyticsModel.loadRedditMemberData()
            pageContent = self.redditView.getRedditMembersContent()
        elif entry in ['cfp']:
            self.defichainAnalyticsModel.loadCFPData()
            pageContent = self.cfpView.getCFPContent()
        elif entry in ["analytics"]:
            self.defichainAnalyticsModel.loadAnalyticsVisitsData()
            pageContent = self.analyticsView.getAnalyticsContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["income"]:
            self.defichainAnalyticsModel.loadIncomeVisitsData()
            pageContent = self.incomeView.getIncomeContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["portfolio"]:
            self.defichainAnalyticsModel.loadPortfolioDownloads()
            pageContent = self.portfolioView.getPortfolioContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["mnmonitor"]:
            self.defichainAnalyticsModel.loadMNMonitorDatabase()
            pageContent = self.mnMonitorView.getmnMonitorContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["dfx"]:
            self.defichainAnalyticsModel.loadDFXdata()
            pageContent = self.dfxView.getDFXContent()
        elif entry in ["dfisignal"]:
            self.defichainAnalyticsModel.loadDFIsignalDatabase()
            pageContent = self.dfiSignalView.getDFISignalContent(self.defichainAnalyticsModel.dailyData, self.defichainAnalyticsModel.figBackgroundImage)
        elif entry in ["dobby"]:
            self.defichainAnalyticsModel.loadDobbyDatabase()
            pageContent = self.dobbyView.getDobbyContent()
        elif entry in ["lock"]:
            self.defichainAnalyticsModel.loadLOCKdata()
            pageContent = self.lockView.getLOCKContent()

        return pageContent