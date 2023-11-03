from dash.dependencies import Input, Output, State

class feesCallbacksClass:
    def __init__(self, defichainAnalyticsModel, feesView, app):

        @app.callback(Output('figureDMCfees', 'figure'),
                      [Input('defiDMCfees', 'value')])
        def updateDUSDBurnGraph(selectedGraph):
            figDMCFees = feesView.createFeesGraph(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedGraph)
            return figDMCFees

        @app.callback(
            Output("modalDMCfees", "is_open"),
            [Input("openInfoDMCfees", "n_clicks"), Input("closeInfoDMCfees", "n_clicks")],
            [State("modalDMCfees", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open