from dash.dependencies import Input, Output, State


class inflationCallbacksClass:
    def __init__(self, defichainAnalyticsModel, inflationView, app):

        @app.callback(Output('figureInflation', 'figure'),
                      [Input('inflationSelection', 'value')])
        def updateVolumeGraph(selectedGraph):
            figInflation = inflationView.createInflationGraph(defichainAnalyticsModel.dailyData, defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedGraph)
            return figInflation

        @app.callback(
            Output("modalInflation", "is_open"),
            [Input("openInfoInflation", "n_clicks"), Input("closeInfoInflation", "n_clicks")],
            [State("modalInflation", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:                    # needed for close button
                return not is_open
            return is_open
