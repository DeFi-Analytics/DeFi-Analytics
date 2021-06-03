from dash.dependencies import Input, Output, State
import pandas as pd

class stabilityCallbacksClass:
    def __init__(self, defichainAnalyticsModel, stabilityView, app):

        @app.callback([Output('stabilityPoolLastUpdate', 'children'),
                       Output('stabilityPoolCoinA', 'children'),
                       Output('stabilityPoolCoinB', 'children')],
                      [Input('stabilityPoolSelection', 'value')])
        def updateUsedDataInfos(selectedPool):
            lastUpdate = pd.to_datetime(defichainAnalyticsModel.hourlyData[selectedPool + '-DFI_reserveB'].dropna().index.values[-1]).strftime('%Y-%m-%d %H:%M')
            coinA = "{:,.1f}".format(defichainAnalyticsModel.hourlyData[selectedPool+'-DFI_reserveA'].dropna().iloc[-1])+' '+selectedPool
            coinB = "{:,.0f}".format(defichainAnalyticsModel.hourlyData[selectedPool + '-DFI_reserveB'].dropna().iloc[-1]) + ' DFI'
            return lastUpdate, coinA, coinB

        @app.callback([Output('figureStabilityDFI', 'figure'),
                       Output('stabilityChangePriceOutput', 'children')],
                      [Input('stabilityChangePriceInput', 'value'),
                       Input('stabilityPoolSelection', 'value')])
        def updateFigStabilityDFI(ratioChangeInput, selectedPool):
            figStabilityDFI, nbDFIneeded = stabilityView.createStabilityDFIGraph(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedPool, ratioChangeInput)
            return figStabilityDFI, "{:,.0f}".format(nbDFIneeded)


        # @app.callback(Output('figureTVL', 'figure'),
        #               [Input('defiTVLCurrency', 'value')])
        # def updateTVLGraphs(selectedRepresentation):
        #     figFee = tvlView.createTVLGraph(defichainAnalyticsModel.hourlyData, selectedRepresentation, defichainAnalyticsModel.figBackgroundImage)
        #     return figFee

        # @app.callback(
        #     Output("modalTVL", "is_open"),
        #     [Input("openInfoTVL", "n_clicks"), Input("closeInfoTVL", "n_clicks")],
        #     [State("modalTVL", "is_open")],)
        # def toggle_modal(n1, n2, is_open):
        #     if n1 or n2:
        #         return not is_open
        #     return is_open