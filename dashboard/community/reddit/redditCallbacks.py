from dash.dependencies import Input, Output, State


class redditCallbacksClass:
    def __init__(self, defichainAnalyticsModel, redditView, app):

        @app.callback(Output('figureRedditMember', 'figure'),
                      [Input('communityRedditMemberSelection', 'value')])
        def updateMembersGraphs(selectedGraph):
            figMembers = None
            if selectedGraph == 'nbAbsolute':
                figMembers = redditView.createRedditMemberGraph(defichainAnalyticsModel.dailyData, defichainAnalyticsModel.figBackgroundImage)
            elif selectedGraph == 'absDailyDiff':
                figMembers = redditView.createDiffRedditMemberGraph(defichainAnalyticsModel.dailyData, defichainAnalyticsModel.figBackgroundImage, 'absolute')
            elif selectedGraph == 'relDailyDiff':
                figMembers = redditView.createDiffRedditMemberGraph(defichainAnalyticsModel.dailyData, defichainAnalyticsModel.figBackgroundImage, 'relative')
            return figMembers

        @app.callback(
            Output("modalRedditMember", "is_open"),
            [Input("openInfoRedditMember", "n_clicks"), Input("closeInfoRedditMember", "n_clicks")],
            [State("modalRedditMember", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open