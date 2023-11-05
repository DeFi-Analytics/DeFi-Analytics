from dash.dependencies import Input, Output, State

class tokenCallbacksClass:
    def __init__(self, defichainAnalyticsModel, tokenView, app):

        @app.callback(Output('figureDMCtoken', 'figure'),
                      [Input('defiDMCtoken', 'value')])
        def updateDUSDBurnGraph(selectedGraph):
            figDMCFees = tokenView.createTokensGraph(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedGraph)
            return figDMCFees

        @app.callback(
            Output("modalDMCtoken", "is_open"),
            [Input("openInfoDMCtoken", "n_clicks"), Input("closeInfoDMCtoken", "n_clicks")],
            [State("modalDMCtoken", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open