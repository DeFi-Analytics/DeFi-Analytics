from dash.dependencies import Input, Output, State


class nbDTokenCallbacksClass:
    def __init__(self, defichainAnalyticsModel, nbDTokenView, app):

        @app.callback(
            Output("modalNbDToken", "is_open"),
            [Input("openInfoNbDToken", "n_clicks"), Input("closeInfoNbDToken", "n_clicks")],
            [State("modalNbDToken", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

        @app.callback(Output('figureNbDToken', 'figure'),
                      [Input('vaultsLoansNbDtoken', 'value')])
        def selectGraph(selectedRepresentation):
            fidNbDToken = nbDTokenView.createNbDToken(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedRepresentation)
            return fidNbDToken