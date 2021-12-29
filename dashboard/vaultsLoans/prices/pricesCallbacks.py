from dash.dependencies import Input, Output, State


class pricesDTokenCallbacksClass:
    def __init__(self, defichainAnalyticsModel, pricesDTokenView, app):

        @app.callback(
            Output("modalPricesDToken", "is_open"),
            [Input("openInfoPricesDToken", "n_clicks"), Input("closeInfoPricesDToken", "n_clicks")],
            [State("modalPricesDToken", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

        @app.callback(Output('figurePricesDToken', 'figure'),
                      [Input('vaultsLoansPricesDtoken', 'value')])
        def selectGraph(selectedRepresentation):
            fidPrices = pricesDTokenView.createPricesDToken(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedRepresentation)
            return fidPrices
