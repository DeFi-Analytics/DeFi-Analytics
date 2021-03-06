from dash.dependencies import Input, Output, State


class coinpriceCallbacksClass:
    def __init__(self, defichainAnalyticsModel, coinpriceView, app):


        @app.callback(Output('figureCoinpriceLongterm', 'figure'),
                      [Input('dexCoinprice600s', 'n_intervals'),
                       Input('dexCoinpriceCoin', 'value'),
                       Input('dexCoinpriceReference', 'value'), ])
        def updateHourlyCoinpriceGraph(nInt, selectedCoin, selectedReference):
            defichainAnalyticsModel.loadHourlyDEXdata()
            figHourlyGraph = coinpriceView.createPriceGraph(defichainAnalyticsModel.hourlyData, selectedCoin, selectedReference, 'Long', defichainAnalyticsModel.figBackgroundImage)
            return figHourlyGraph

        @app.callback(Output('figureCoinpriceShortterm', 'figure'),
                      [Input('dexCoinprice60s', 'n_intervals'),
                       Input('dexCoinpriceCoin', 'value'),
                       Input('dexCoinpriceReference', 'value'), ])
        def updateMinutelyCoinpriceGraph(nInt, selectedCoin, selectedReference):
            defichainAnalyticsModel.loadMinutelyDEXdata()
            figHourlyGraph = coinpriceView.createPriceGraph(defichainAnalyticsModel.minutelyData, selectedCoin, selectedReference, 'Short', defichainAnalyticsModel.figBackgroundImage)
            return figHourlyGraph

        @app.callback(
            Output("modalCoinprice", "is_open"),
            [Input("openInfoCoinprice", "n_clicks"), Input("closeInfoCoinprice", "n_clicks")],
            [State("modalCoinprice", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open