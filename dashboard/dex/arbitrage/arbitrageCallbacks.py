from dash.dependencies import Input, Output, State


class arbitrageCallbacksClass:
    def __init__(self, defichainAnalyticsModel, coinpriceView, app):


        @app.callback(Output('figureArbitrageLongterm', 'figure'),
                      [Input('dexArbitrage600s', 'n_intervals'),
                       Input('dexArbitrageCoin', 'value'),
                       Input('dexArbitrageReference', 'value'), ])
        def updateHourlyCoinpriceGraph(nInt, selectedCoin, selectedReference):
            defichainAnalyticsModel.loadHourlyDEXdata()
            figHourlyGraph = coinpriceView.createPriceGraph(defichainAnalyticsModel.hourlyData, selectedCoin, selectedReference, 'Long', defichainAnalyticsModel.figBackgroundImage)
            return figHourlyGraph

        @app.callback(Output('figureArbitrageShortterm', 'figure'),
                      [Input('dexArbitrage60s', 'n_intervals'),
                       Input('dexArbitrageCoin', 'value'),
                       Input('dexArbitrageReference', 'value'), ])
        def updateMinutelyCoinpriceGraph(nInt, selectedCoin, selectedReference):
            defichainAnalyticsModel.loadMinutelyDEXdata()
            figHourlyGraph = coinpriceView.createPriceGraph(defichainAnalyticsModel.minutelyData, selectedCoin, selectedReference, 'Short', defichainAnalyticsModel.figBackgroundImage)
            return figHourlyGraph

        @app.callback(
            Output("modalArbitrage", "is_open"),
            [Input("openInfoArbitrage", "n_clicks"), Input("closeInfoArbitrage", "n_clicks")],
            [State("modalArbitrage", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open