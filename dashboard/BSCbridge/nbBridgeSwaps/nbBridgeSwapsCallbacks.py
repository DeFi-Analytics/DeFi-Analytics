from dash.dependencies import Input, Output, State


class nbBridgeSwapsCallbacksClass:
    def __init__(self, defichainAnalyticsModel, nbBridgeSwapsbView, app):

        @app.callback(Output('figureBSCnbSwaps', 'figure'),
                      [Input('BSCnbSwapsSelection', 'value')])
        def updateNbBridgeSwapsGraph(selectedGraph):
            figBSCnbSwaps = nbBridgeSwapsbView.createBSCNbSwapsFig(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedGraph)
            return figBSCnbSwaps

        @app.callback(
            Output("modalBSCnbSwaps", "is_open"),
            [Input("openInfoBSCnbSwaps", "n_clicks"), Input("closeInfoBSCnbSwaps", "n_clicks")],
            [State("modalBSCnbSwaps", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:                    # needed for close button
                return not is_open
            return is_open
