from dash.dependencies import Input, Output, State
import pandas as pd

class slippageCallbacksClass:
    def __init__(self, defichainAnalyticsModel, slippageView, app):

        @app.callback([Output('slippagePoolLastUpdate', 'children'),
                       Output('slippagePoolCoinA', 'children'),
                       Output('slippagePoolCoinB', 'children')],
                      [Input('slippagePoolSelection', 'value')])
        def updateUsedDataInfos(selectedPool):
            lastUpdate = pd.to_datetime(defichainAnalyticsModel.hourlyData[selectedPool + '-DFI_reserveB'].dropna().index.values[-1]).strftime('%Y-%m-%d %H:%M')
            coinA = "{:,.1f}".format(defichainAnalyticsModel.hourlyData[selectedPool+'-DFI_reserveA'].dropna().iloc[-1])+' '+selectedPool
            coinB = "{:,.0f}".format(defichainAnalyticsModel.hourlyData[selectedPool + '-DFI_reserveB'].dropna().iloc[-1]) + ' DFI'
            return lastUpdate, coinA, coinB

        @app.callback([Output('figureSlippage', 'figure'),
                       Output('slippageSwappedDFI', 'children'),
                       Output('slippageSwappedCoinB', 'children'),
                       Output('slippageStartPrice', 'children'),
                       Output('slippageMeanPrice', 'children'),
                       Output('slippageEndPrice', 'children'),
                       ],
                      [Input('slippageCoinAmount', 'value'),
                       Input('slippageOrderSelection', 'value'),
                       Input('slippagePoolSelection', 'value')])
        def updateFigSlippageDFI(coins2sell, selectedOrder, selectedPool):
            figSlippage, swappedDFI, swappedCoinB, startPrice, meanPrice, endPrice = slippageView.createSlippageGraph(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedPool, selectedOrder, coins2sell)
            return figSlippage, swappedDFI, swappedCoinB, startPrice, meanPrice, endPrice

        @app.callback(
            Output("modalSlippage", "is_open"),
            [Input("openInfoSlippage", "n_clicks"), Input("closeInfoSlippage", "n_clicks")],
            [State("modalSlippage", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open