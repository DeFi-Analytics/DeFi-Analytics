from dash.dependencies import Input, Output, State


class overallTVLCallbacksClass:
    def __init__(self, defichainAnalyticsModel, overallTVLView, app):

        @app.callback(Output('figureOverallTVL', 'figure'),
                      [Input('defiOverallTVLCurrency', 'value')])
        def updateOverallTVLGraphs(selectedRepresentation):
            figOverallTVL = overallTVLView.createOverallTVLGraph(defichainAnalyticsModel.dailyData, selectedRepresentation, defichainAnalyticsModel.figBackgroundImage)
            return figOverallTVL

        @app.callback(
            Output("modalOverallTVL", "is_open"),
            [Input("openInfoOverallTVL", "n_clicks"), Input("closeInfoOverallTVL", "n_clicks")],
            [State("modalOverallTVL", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open