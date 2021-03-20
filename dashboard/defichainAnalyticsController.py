import os
from app import app

from defichainAnalyticsView import defichainAnalyticsViewClass
from defichainAnalyticsCallbacks import defichainAnalyticsCallbacksClass
from defichainAnalyticsModel import defichainAnalyticsModelClass

from blockchain.blockchainMenuController import blockchainControllerClass
from dex.dexController import dexControllerClass
from liquidityMining.liquidityMiningController import liquidityMiningControllerClass
from Token.tokenController import tokenControllerClass
from socialMedia.socialmediaController import socialmediaControllerClass

class defichainAnalyticsControllerClass:
    def __init__(self):
        # initialize model and first load of all data
        self.defichainAnalyticsModel = defichainAnalyticsModelClass()
        self.defichainAnalyticsModel.loadDailyData()
        self.defichainAnalyticsModel.loadHourlyData()
        self.defichainAnalyticsModel.loadMinutelyData()
        self.defichainAnalyticsModel.loadLastRichlist()

        self.blockchainController = blockchainControllerClass(app, self.defichainAnalyticsModel)
        self.dexController = dexControllerClass(app, self.defichainAnalyticsModel)
        self.liquidityMiningController = liquidityMiningControllerClass(app, self.defichainAnalyticsModel)
        self.tokenController = tokenControllerClass(app, self.defichainAnalyticsModel)
        self.socialmediaController = socialmediaControllerClass(app, self.defichainAnalyticsModel)

        self.defichainAnalyticsCallbacks = defichainAnalyticsCallbacksClass(self.blockchainController, self.dexController, self.liquidityMiningController, self.tokenController, self.socialmediaController)       # create callbacks on top level
        self.defichainAnalyticsCallbacks.register_callbacks(app)             #

        self.defichainAnalyticsView = defichainAnalyticsViewClass()                 # create main view of Dashboard
        app.layout = self.defichainAnalyticsView.layout

    def getApp(self):
        return app



