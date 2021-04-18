from dash.dependencies import Input, Output, State


class cryptoTokenCallbacksClass:
    def __init__(self, defichainAnalyticsModel, cryptoTokenView, app):

        @app.callback(Output('figureTokenCryptos', 'figure'),
                      [Input('tokenCryptosCoin', 'value')])
        def updateTVLGraphs(selectedCoin):
            figFee = cryptoTokenView.createTokenGraph(defichainAnalyticsModel.hourlyData, selectedCoin, defichainAnalyticsModel.figBackgroundImage)
            return figFee

        @app.callback(
            Output("modalToken", "is_open"),
            [Input("openInfoToken", "n_clicks"), Input("closeInfoToken", "n_clicks")],
            [State("modalToken", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open