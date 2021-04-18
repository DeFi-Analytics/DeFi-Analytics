from dash.dependencies import Input, Output, State


class tvlCallbacksClass:
    def __init__(self, defichainAnalyticsModel, tvlView, app):

        @app.callback(Output('figureTVL', 'figure'),
                      [Input('defiTVLCurrency', 'value')])
        def updateTVLGraphs(selectedRepresentation):
            figFee = tvlView.createTVLGraph(defichainAnalyticsModel.hourlyData, selectedRepresentation, defichainAnalyticsModel.figBackgroundImage)
            return figFee

        @app.callback(
            Output("modalTVL", "is_open"),
            [Input("openInfoTVL", "n_clicks"), Input("closeInfoTVL", "n_clicks")],
            [State("modalTVL", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open