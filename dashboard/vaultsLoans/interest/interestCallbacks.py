from dash.dependencies import Input, Output, State


class interestCallbacksClass:
    def __init__(self, defichainAnalyticsModel, interestView, app):

        @app.callback(
            Output("modalInterest", "is_open"),
            [Input("openInfoInterest", "n_clicks"), Input("closeInfoInterest", "n_clicks")],
            [State("modalInterest", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

        @app.callback(Output('figureInterest', 'figure'),
                      [Input('vaultsLoansInterest', 'value')])
        def selectGraph(selectedRepresentation):
            fidInterest = interestView.createInterest(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedRepresentation)
            return fidInterest