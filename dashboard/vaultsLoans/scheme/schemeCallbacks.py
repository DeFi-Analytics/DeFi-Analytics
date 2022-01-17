from dash.dependencies import Input, Output, State


class schemeCallbacksClass:
    def __init__(self, defichainAnalyticsModel, schemeView, app):

        @app.callback(Output('figureScheme', 'figure'),
                      [Input('coinsSchemeGraphic', 'value')])
        def updateSchemeGraph(selectedRepresentation):
            figScheme = schemeView.createSchemeFigure(defichainAnalyticsModel.hourlyData, selectedRepresentation, defichainAnalyticsModel.figBackgroundImage)
            return figScheme

        @app.callback(
            Output("modalScheme", "is_open"),
            [Input("openInfoScheme", "n_clicks"), Input("closeSchemeCoin", "n_clicks")],
            [State("modalScheme", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

