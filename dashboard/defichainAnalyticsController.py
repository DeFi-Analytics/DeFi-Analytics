import os
from app import app

from defichainAnalyticsView import defichainAnalyticsViewClass
from defichainAnalyticsCallbacks import defichainAnalyticsCallbacksClass
from defichainAnalyticsModel import defichainAnalyticsModelClass

from general.generalController import generalControllerClass
from blockchain.blockchainMenuController import blockchainControllerClass
from dex.dexController import dexControllerClass
from liquidityMining.liquidityMiningController import liquidityMiningControllerClass
from vaultsLoans.vaultsLoansController import vaultsLoansControllerClass
from Token.tokenController import tokenControllerClass
from community.communityController import communityControllerClass
from about.aboutController import aboutControllerClass

class defichainAnalyticsControllerClass:
    def __init__(self):
        # initialize model and first load of all data
        self.defichainAnalyticsModel = defichainAnalyticsModelClass()
        self.defichainAnalyticsModel.loadMinutelyData()
        self.defichainAnalyticsModel.loadHourlyData()
        self.defichainAnalyticsModel.loadDailyData()


        self.defichainAnalyticsModel.loadNoTimeseriesData()

        self.generalController = generalControllerClass(app, self.defichainAnalyticsModel)
        self.blockchainController = blockchainControllerClass(app, self.defichainAnalyticsModel)
        self.dexController = dexControllerClass(app, self.defichainAnalyticsModel)
        self.liquidityMiningController = liquidityMiningControllerClass(app, self.defichainAnalyticsModel)
        self.vaultsLoansController = vaultsLoansControllerClass(app, self.defichainAnalyticsModel)
        self.tokenController = tokenControllerClass(app, self.defichainAnalyticsModel)
        self.communityController = communityControllerClass(app, self.defichainAnalyticsModel)
        self.aboutController = aboutControllerClass(app, self.defichainAnalyticsModel)

        self.defichainAnalyticsCallbacks = defichainAnalyticsCallbacksClass(self.defichainAnalyticsModel, self.generalController, self.blockchainController,
                                                                            self.dexController, self.liquidityMiningController, self.vaultsLoansController,
                                                                            self.tokenController, self.communityController, self.aboutController)       # create callbacks on top level
        self.defichainAnalyticsCallbacks.register_callbacks(app)             #

        self.defichainAnalyticsView = defichainAnalyticsViewClass()                 # create main view of Dashboard

        app.layout = self.defichainAnalyticsView.getDashboardLayout

    def getApp(self):
        return app



