from dash.dependencies import Input, Output, State


class dobbyCallbacksClass:
    def __init__(self, defichainAnalyticsModel, dobbyView, app):

        @app.callback(Output('figureDobbydata', 'figure'),
                      [Input('dobbySelectGraph', 'value')])
        def selectGraph(selectedRepresentation):
            fidDobby = dobbyView.createDobbyFigure(defichainAnalyticsModel.dailyData, defichainAnalyticsModel.figBackgroundImage, selectedRepresentation)
            return fidDobby
