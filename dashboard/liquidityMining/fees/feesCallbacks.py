from dash.dependencies import Input, Output, State


class feesCallbacksClass:
    def __init__(self, defichainAnalyticsModel, feesView, app):

        @app.callback(Output('lmPaidFees', 'figure'),
                      [Input('feeRepresentation', 'value')])
        def updateTradingFeeGraphs(selectedRepresentation):
            defichainAnalyticsModel.loadDailyTradingData()
            figFee = feesView.createFeesGraph(defichainAnalyticsModel.dailyData, selectedRepresentation, defichainAnalyticsModel.figBackgroundImage)
            return figFee

        @app.callback(Output('lmPaidCoinFees', 'figure'),
                      [Input('feeNativeCoin', 'value')])
        def updateTradingFeeCoinGraphs(selectedCoin):
            defichainAnalyticsModel.loadDailyTradingData()
            figFee = feesView.createFeesCoinFigure(defichainAnalyticsModel.dailyData, selectedCoin, defichainAnalyticsModel.figBackgroundImage)
            return figFee

        @app.callback(
            Output("modalFees", "is_open"),
            [Input("openInfoFees", "n_clicks"), Input("closeInfoFees", "n_clicks")],
            [State("modalFees", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open