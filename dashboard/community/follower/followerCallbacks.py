from dash.dependencies import Input, Output, State


class followerCallbacksClass:
    def __init__(self, defichainAnalyticsModel, followerView, app):

        @app.callback(Output('figureTwitterFollower', 'figure'),
                      [Input('communityFollowerSelection', 'value')])
        def updateTVLGraphs(selectedGraph):
            figFollower = None
            if selectedGraph == 'nbAbsolute':
                figFollower = followerView.createFollowerGraph(defichainAnalyticsModel.dailyData, defichainAnalyticsModel.figBackgroundImage)
            elif selectedGraph == 'dailyDiff':
                figFollower = followerView.createDiffFollowerGraph(defichainAnalyticsModel.dailyData, defichainAnalyticsModel.figBackgroundImage)
            return figFollower

        @app.callback(
            Output("modalTwitterFollower", "is_open"),
            [Input("openInfoTwitterFollower", "n_clicks"), Input("closeInfoTwitterFollower", "n_clicks")],
            [State("modalTwitterFollower", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open