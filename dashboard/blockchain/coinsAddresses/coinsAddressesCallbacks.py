from dash.dependencies import Input, Output, State


class coinsAddressesCallbacksClass:
    def __init__(self, defichainAnalyticsModel, coinsAddressesView, app):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.coinsAddressesView = coinsAddressesView

        @app.callback(
            Output('DFIAddSlider', 'value'),
            [Input('minDFIValueInput', 'value'),
             Input('maxDFIValueInput', 'value')])
        def updateDFISlider(minValue, maxValue):
            return [minValue, maxValue]

        @app.callback(
            [Output('minDFIValueInput', 'value'),
             Output('maxDFIValueInput', 'value'),
             Output('figCoinsAddresses', 'figure')],
            [Input('DFIAddSlider', 'value')])
        def updateMaxDFIInput(value):
            figDFIDist = coinsAddressesView.getCoinAddressFigure(defichainAnalyticsModel.lastRichlist, value[0], value[1])
            return value[0], value[1], figDFIDist

        @app.callback(
            Output("modalCoinsAddresses", "is_open"),
            [Input("openInfoCoinsAddresses", "n_clicks"), Input("closeInfoCoinsAddresses", "n_clicks")],
            [State("modalCoinsAddresses", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open






