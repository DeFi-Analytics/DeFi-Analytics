from dash.dependencies import Input, Output, State


class aprCallbacksClass:
    def __init__(self, defichainAnalyticsModel, aprView, app):

        @app.callback(Output('figureAPRRate', 'figure'),
                      [Input('APRSelection', 'value')])
        def updateAPRGraph(selectedCoin):
            figAPR = aprView.createAPRGraph(defichainAnalyticsModel.hourlyData, selectedCoin, defichainAnalyticsModel.figBackgroundImage)
            return figAPR

        @app.callback(
            Output("modalAPR", "is_open"),
            [Input("openInfoAPR", "n_clicks"), Input("closeInfoAPR", "n_clicks")],
            [State("modalAPR", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open