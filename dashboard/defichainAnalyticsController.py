import os
from app import app

from defichainAnalyticsView import defichainAnalyticsViewClass
from defichainAnalyticsCallbacks import defichainAnalyticsCallbacksClass
from defichainAnalyticsModel import defichainAnalyticsModelClass

from blockchain.blockchainMenuController import blockchainControllerClass
from liquidityMining.liquidityMiningController import liquidityMiningControllerClass
from SubMenu2.SubMenu2Controller import sub2ControllerClass

class defichainAnalyticsControllerClass:
    def __init__(self):
        self.defichainAnalyticsModel = defichainAnalyticsModelClass()
        self.defichainAnalyticsModel.loadDailyData()

        self.blockchainController = blockchainControllerClass(app, self.defichainAnalyticsModel)
        self.blockchainController.registerCallbacks(app)

        self.liquidityMiningController = liquidityMiningControllerClass(app, self.defichainAnalyticsModel)
        self.submenu2Controller = sub2ControllerClass()

        self.defichainAnalyticsCallbacks = defichainAnalyticsCallbacksClass(self.blockchainController, self.liquidityMiningController ,self.submenu2Controller)       # create callbacks on top level
        self.defichainAnalyticsCallbacks.register_callbacks(app)             #

        self.defichainAnalyticsView = defichainAnalyticsViewClass()                 # create main view of Dashboard
        app.layout = self.defichainAnalyticsView.layout

    def getApp(self):
        return app



