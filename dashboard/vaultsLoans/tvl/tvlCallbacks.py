from dash.dependencies import Input, Output, State


class tvlVaultsCallbacksClass:
    def __init__(self, defichainAnalyticsModel, tvlVaultsView, app):

        @app.callback(Output('figureTVLVaults', 'figure'),
                      [Input('defiTVLVaultsCurrency', 'value')])
        def updateTVLGraphs(selectedRepresentation):
            figFee = tvlVaultsView.createTVLGraph(defichainAnalyticsModel.hourlyData, selectedRepresentation, defichainAnalyticsModel.figBackgroundImage)
            return figFee

        @app.callback(
            Output("modalTVLVaults", "is_open"),
            [Input("openInfoTVLVaults", "n_clicks"), Input("closeInfoTVLVaults", "n_clicks")],
            [State("modalTVLVaults", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open