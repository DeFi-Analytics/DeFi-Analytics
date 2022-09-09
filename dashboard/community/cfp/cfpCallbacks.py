from dash.dependencies import Input, Output


class cfpCallbacksClass:
    def __init__(self, defichainAnalyticsModel, cfpView, app):

        @app.callback(Output('cfpDataTable', 'children'),
                      [Input('sortCFPColumnSelection', 'value'),
                       Input('sortCFPDirectionSelection', 'value')])
        def updateFigSlippageDFI(sortCFPColumnSelection, sortCFPDirectionSelection):
            cfpDataTable = cfpView.createCFPTable(defichainAnalyticsModel.cfpData, sortCFPColumnSelection, sortCFPDirectionSelection)
            return cfpDataTable