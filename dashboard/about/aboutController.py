from .imprint.imprintView import imprintViewClass
from .changelog.changelogView import changelogViewClass
from .donate.donateView import donateViewClass
from .donate.donateCallbacks import donateCallbacksClass


class aboutControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize overview classes
        self.imprintView = imprintViewClass()
        self.changelogView = changelogViewClass()

        self.donateView = donateViewClass()
        self.donateCallbacks = donateCallbacksClass(app)

    def getContent(self, entry):
        pageContent = None

        if entry in ['', 'changelog']:
            pageContent = self.changelogView.getChangelogContent(self.defichainAnalyticsModel.changelogData)
        elif entry in ["imprint"]:
            pageContent = self.imprintView.getImprintContent()
        elif entry in ["donate"]:
            pageContent = self.donateView.getDonateContent()

        return pageContent
