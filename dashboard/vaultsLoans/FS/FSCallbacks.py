from dash.dependencies import Input, Output, State


class fsValueCallbacksClass:
    def __init__(self, defichainAnalyticsModel, fsValueView, app):

        @app.callback(Output('figureFSValue', 'figure'),
                      [Input('defiFSValueDToken', 'value')])
        def updateFSValueGraph(selectedRepresentation):
            figValue = fsValueView.createFSValueGraph(defichainAnalyticsModel.hourlyData, selectedRepresentation, defichainAnalyticsModel.figBackgroundImage)
            return figValue

        @app.callback(
            Output("modalFSValue", "is_open"),
            [Input("openInfoFSValue", "n_clicks"), Input("closeInfoFSValue", "n_clicks")],
            [State("modalFSValue", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open