from dash.dependencies import Input, Output, State


class emissionCallbacksClass:
    def __init__(self, defichainAnalyticsModel, emissionView, app):

        @app.callback(Output('figureEmission', 'figure'),
                      [Input('selectEmission', 'value')])
        def updateEmissionGraphs(selectedRepresentation):
            figFee = emissionView.createEmissionGraph(defichainAnalyticsModel.dailyData, selectedRepresentation, defichainAnalyticsModel.figBackgroundImage)
            return figFee

        @app.callback(
            Output("modalEmission", "is_open"),
            [Input("openInfoEmission", "n_clicks"), Input("closeInfoEmission", "n_clicks")],
            [State("modalEmission", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open