from dash.dependencies import Input, Output, State


class dfxCallbacksClass:
    def __init__(self, defichainAnalyticsModel, dfxView, app):

        @app.callback(Output('figureDFXdata', 'figure'),
                      [Input('dfxSelectGraph', 'value')])
        def selectGraph(selectedRepresentation):
            fidDFX = dfxView.createDFXFigure(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, selectedRepresentation)
            return fidDFX
