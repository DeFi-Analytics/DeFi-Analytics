from .imprint.imprintView import imprintViewClass
from .cakereview.cakereviewView import cakereviewViewClass
from .changelog.changelogView import changelogViewClass


class aboutControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize overview classes
        self.imprintView = imprintViewClass()
        self.cakereviewView = cakereviewViewClass()
        self.changelogView = changelogViewClass()


    def getContent(self, entry):
        pageContent = None

        if entry in ['', 'changelog']:
            pageContent = self.changelogView.getChangelogContent(self.defichainAnalyticsModel.changelogData)
        elif entry in ['cakereview']:
            pageContent = self.cakereviewView.getCakereviewContent()
        elif entry in ["imprint"]:
            pageContent = self.imprintView.getImprintContent()


        return pageContent
