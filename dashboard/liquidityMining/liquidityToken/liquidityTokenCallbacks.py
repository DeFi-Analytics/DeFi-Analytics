from dash.dependencies import Input, Output, State


class liquidityTokenCallbacksClass:
    def __init__(self, defichainAnalyticsModel, ltView, app):

        @app.callback(Output('figureLiquidityToken', 'figure'),
                      [Input('LTSelection', 'value')])
        def updateTVLGraphs(selectedCoin):
            figFee = ltView.createLiquidityTokenGraph(defichainAnalyticsModel.hourlyData, selectedCoin, defichainAnalyticsModel.figBackgroundImage)
            return figFee

        @app.callback(
            Output("modalLT", "is_open"),
            [Input("openInfoLT", "n_clicks"), Input("closeInfoLT", "n_clicks")],
            [State("modalLT", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open