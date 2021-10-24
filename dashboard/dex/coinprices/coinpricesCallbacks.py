from dash.dependencies import Input, Output, State


class coinpricesCallbacksClass:
    def __init__(self, defichainAnalyticsModel, coinpricesView, app):

        @app.callback(Output('figureCoinprices', 'figure'),
                      [Input('dexCoinpriceCoin', 'value')])
        def updateVolumeGraph(selectedCoin, ):
            figVolume = coinpricesView.createPriceGraph(defichainAnalyticsModel.hourlyData, selectedCoin, defichainAnalyticsModel.figBackgroundImage)
            return figVolume

        @app.callback(
            Output("modalCoinprices", "is_open"),
            [Input("openInfoCoinprices", "n_clicks"), Input("closeInfoCoinprices", "n_clicks")],
            [State("modalCoinprices", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open