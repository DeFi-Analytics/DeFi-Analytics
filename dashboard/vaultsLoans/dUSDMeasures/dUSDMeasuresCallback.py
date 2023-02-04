from dash.dependencies import Input, Output, State

class dUSDMeasuresCallbacksClass:
    def __init__(self, defichainAnalyticsModel, dUSDMeasuresView, app):

        @app.callback(Output('figureDUSDBurn', 'figure'),
                      [Input('dUSDBurnTimeSelection', 'value')])
        def updateDUSDBurnGraph(selectedGraph):
            figDUSDBurn = dUSDMeasuresView.createDUSDBurnFig(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedGraph)
            return figDUSDBurn

        @app.callback(
            Output("modaldUSDMeasures", "is_open"),
            [Input("openInfodUSDMeasures", "n_clicks"), Input("closeInfodUSDMeasures", "n_clicks")],
            [State("modaldUSDMeasures", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open