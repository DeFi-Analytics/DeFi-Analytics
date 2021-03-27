from .imprint.imprintView import imprintViewClass
from .cakereview.cakereviewView import cakereviewViewClass


class aboutControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize overview classes
        self.imprintView = imprintViewClass()
        self.cakereviewView = cakereviewViewClass()


    def getContent(self, entry):
        pageContent = None
        if entry in ['', "imprint"]:
            pageContent = self.imprintView.getImprintContent()
        elif entry in ['cakereview']:
            pageContent = self.cakereviewView.getCakereviewContent()


        return pageContent
