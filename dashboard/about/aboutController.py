from .imprint.imprintView import imprintViewClass


class aboutControllerClass:
    def __init__(self, app, defichainAnalyticsModel):
        self.defichainAnalyticsModel = defichainAnalyticsModel

        # initialize overview classes
        self.imprintView = imprintViewClass()



    def getContent(self, entry):
        pageContent = None
        if entry in ['', "imprint"]:
            pageContent = self.imprintView.getImprintContent()


        return pageContent
