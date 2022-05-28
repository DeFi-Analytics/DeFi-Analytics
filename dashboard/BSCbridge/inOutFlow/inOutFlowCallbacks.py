from dash.dependencies import Input, Output, State


class inOutFlowCallbacksClass:
    def __init__(self, defichainAnalyticsModel, inOutFlowView, app):

        @app.callback(Output('figureBSCInOutFlow', 'figure'),
                      [Input('BSCInOutFlowSelection', 'value')])
        def updateInOutFlowGraph(selectedGraph):
            figBSCInOutFlow = inOutFlowView.createBSCInOutFlowFig(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedGraph)
            return figBSCInOutFlow

        @app.callback(
            Output("modalBSCInOutFlow", "is_open"),
            [Input("openInfoBSCInOutFlow", "n_clicks"), Input("closeInfoBSCInOutFlow", "n_clicks")],
            [State("modalBSCInOutFlow", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:                    # needed for close button
                return not is_open
            return is_open
