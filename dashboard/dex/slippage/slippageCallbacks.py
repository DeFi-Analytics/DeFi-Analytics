from dash.dependencies import Input, Output, State
import pandas as pd

class slippageCallbacksClass:
    def __init__(self, defichainAnalyticsModel, stabilityView, app):

        @app.callback([Output('slippagePoolLastUpdate', 'children'),
                       Output('slippagePoolCoinA', 'children'),
                       Output('slippagePoolCoinB', 'children')],
                      [Input('slippagePoolSelection', 'value')])
        def updateUsedDataInfos(selectedPool):
            lastUpdate = pd.to_datetime(defichainAnalyticsModel.hourlyData[selectedPool + '-DFI_reserveB'].dropna().index.values[-1]).strftime('%Y-%m-%d %H:%M')
            coinA = "{:,.1f}".format(defichainAnalyticsModel.hourlyData[selectedPool+'-DFI_reserveA'].dropna().iloc[-1])+' '+selectedPool
            coinB = "{:,.0f}".format(defichainAnalyticsModel.hourlyData[selectedPool + '-DFI_reserveB'].dropna().iloc[-1]) + ' DFI'
            return lastUpdate, coinA, coinB

        # @app.callback([Output('figureStabilityDFI', 'figure'),
        #                Output('stabilityChangePriceOutput', 'children')],
        #               [Input('stabilityChangePriceInput', 'value'),
        #                Input('stabilityPoolSelection', 'value')])
        # def updateFigStabilityDFI(ratioChangeInput, selectedPool):
        #     figStabilityDFI, nbDFIneeded = stabilityView.createStabilityDFIGraph(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedPool, ratioChangeInput)
        #     return figStabilityDFI, "{:,.0f}DFI".format(nbDFIneeded)
        #
        # @app.callback([Output('figureStabilityPrice', 'figure'),
        #                Output('stabilityChangeDFIOutput', 'children')],
        #               [Input('stabilityChangeDFIInput', 'value'),
        #                Input('stabilityPoolSelection', 'value')])
        # def updateFigStabilityDFI(DFIChangeInput, selectedPool):
        #     figStabilityDFI, nbDFIneeded = stabilityView.createDFIRatioGraph(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedPool, DFIChangeInput)
        #     return figStabilityDFI, "{:,.2f}%".format(nbDFIneeded)
        #
        # @app.callback(
        #     Output("modalStability", "is_open"),
        #     [Input("openInfoStability", "n_clicks"), Input("closeInfoStability", "n_clicks")],
        #     [State("modalStability", "is_open")],)
        # def toggle_modal(n1, n2, is_open):
        #     if n1 or n2:
        #         return not is_open
        #     return is_open