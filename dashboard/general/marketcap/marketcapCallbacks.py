from dash.dependencies import Input, Output, State


class marketcapCallbacksClass:
    def __init__(self, defichainAnalyticsModel, marketcapView, app):

        @app.callback(Output('figureMarketcap', 'figure'),
                      [Input('marketCapCurrencySelection', 'value')])
        def updateMarketcapGraph(selectedRepresentation):
            figMarketcap = marketcapView.createMarketCapFig(defichainAnalyticsModel.dailyData, selectedRepresentation, defichainAnalyticsModel.figBackgroundImage)
            return figMarketcap

        @app.callback(
            Output("modalMarketcap", "is_open"),
            [Input("openInfoMarketcap", "n_clicks"), Input("closeInfoMarketcap", "n_clicks")],
            [State("modalMarketcap", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open