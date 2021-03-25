from dash.dependencies import Input, Output, State
import pandas as pd

class overviewCallbacksClass:
    def __init__(self, defichainAnalyticsModel, overviewView, app):

        @app.callback(
            Output("modalOverview", "is_open"),
            [Input("openInfoOverview", "n_clicks"), Input("closeInfoOverview", "n_clicks")],
            [State("modalOverview", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

        @app.callback([Output('dfiCountdownBlocks', 'children'),
                       Output('dfiCountdownDuration', 'children'),
                       Output('dfiCountdownTime', 'children')],
                      [Input('overviewUpdateCountdown', 'n_intervals')])
        def updateCountdown(nInt):
            defichainAnalyticsModel.loadSnapshotData()

            blocksLeft = str("{:,.0f}".format(defichainAnalyticsModel.snapshotData['blocksLeft'].values[0]))

            tempDuration = pd.Timedelta(defichainAnalyticsModel.snapshotData['duration'].values[0])
            durationLeft = str(tempDuration)

            eta = defichainAnalyticsModel.snapshotData['etaEvent'].dt.strftime("%d-%m-%Y, %H:%M:%S")
            return blocksLeft, durationLeft, eta
