from dash.dependencies import Input, Output, State


class dfiSignalCallbacksClass:
    def __init__(self, defichainAnalyticsModel, dfiSignalView, app):

        @app.callback(Output('figureDFISignal', 'figure'),
                      [Input('dfiSignalSelectGraph', 'value')])
        def selectGraph(selectedRepresentation):
            fidDFISignal = dfiSignalView.createUserMNCount(defichainAnalyticsModel.dailyData, defichainAnalyticsModel.figBackgroundImage, selectedRepresentation)
            return fidDFISignal
