from dash.dependencies import Input, Output, State


class ratioAlgoLoansCallbacksClass:
    def __init__(self, defichainAnalyticsModel, ratioAlgoLoansView, app):

        @app.callback(
            Output("modalAlgoRatioLoans", "is_open"),
            [Input("openInfoAlgoRatioLoans", "n_clicks"), Input("closeInfoAlgoRatioLoans", "n_clicks")],
            [State("modalAlgoRatioLoans", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

        @app.callback(Output('figureAlgoRatioLoans', 'figure'),
                      [Input('vaultsLoansAlgoRatioLoans', 'value')])
        def selectGraph(selectedRepresentation):
            figRatioAlgoLoan = ratioAlgoLoansView.createAlgoRatioLoans(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedRepresentation)
            return figRatioAlgoLoan

