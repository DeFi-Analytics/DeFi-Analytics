from dash.dependencies import Input, Output, State


class masternodesCallbacksClass:
    def __init__(self, defichainAnalyticsModel, mnView, app):
        @app.callback(Output('masternodesGraphic', 'figure'),
                      [Input('mnRepresentation', 'value')])
        def updateTVLGraphs(selectedRepresentation):
            figMN = mnView.createMasternodesGraph(defichainAnalyticsModel.dailyData, selectedRepresentation, defichainAnalyticsModel.figBackgroundImage)
            return figMN

        @app.callback(
            Output("modalMN", "is_open"),
            [Input("openInfoMN", "n_clicks"), Input("closeInfoMN", "n_clicks")],
            [State("modalMN", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open
