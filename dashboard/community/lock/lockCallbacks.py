from dash.dependencies import Input, Output, State


class lockCallbacksClass:
    def __init__(self, defichainAnalyticsModel, lockView, app):

        @app.callback(Output('figureLOCKdata', 'figure'),
                      [Input('lockSelectService', 'value'),
                       Input('lockSelectGraph', 'value')])
        def selectGraph(lockSelectService, lockSelectGraph):
            figLOCK = lockView.createLOCKFigure(defichainAnalyticsModel.hourlyData, defichainAnalyticsModel.figBackgroundImage, lockSelectService, lockSelectGraph)
            return figLOCK
