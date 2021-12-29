from dash.dependencies import Input, Output, State


class pricesDTokenCallbacksClass:
    def __init__(self, defichainAnalyticsModel, pricesDTokenView, app):

        @app.callback(Output('figurePricesDToken', 'figure'),
                      [Input('vaultsLoansPricesDtoken', 'value')])
        def selectGraph(selectedRepresentation):
            fidPrices = pricesDTokenView.createPricesDToken(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedRepresentation)
            return fidPrices
