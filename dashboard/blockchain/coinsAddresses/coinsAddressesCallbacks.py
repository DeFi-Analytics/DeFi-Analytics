from dash.dependencies import Input, Output, State


class coinsAddressesCallbacksClass:
    def __init__(self, defichainAnalyticsModel, coinsAddressesView, app):

        @app.callback(
            Output('DFIAddSlider', 'value'),
            [Input('minDFIValueInput', 'value'),
             Input('maxDFIValueInput', 'value')])
        def updateDFISlider(minValue, maxValue):
            return [minValue, maxValue]

        @app.callback(
            [Output('minDFIValueInput', 'value'),
             Output('maxDFIValueInput', 'value'),
             Output('figureCoinsAddresses', 'figure')],
            [Input('DFIAddSlider', 'value')])
        def updateMaxDFIInput(value):
            try:
                minDFI = float(value[0])
                maxDFI = float(value[1])
            except:
                minDFI = 0
                maxDFI = 100000
            figDFIDist = coinsAddressesView.getCoinAddressFigure(defichainAnalyticsModel.lastRichlist, minDFI, maxDFI, defichainAnalyticsModel.figBackgroundImage)
            return minDFI, maxDFI, figDFIDist

        @app.callback(
            Output("modalCoinsAddresses", "is_open"),
            [Input("openInfoCoinsAddresses", "n_clicks"), Input("closeInfoCoinsAddresses", "n_clicks")],
            [State("modalCoinsAddresses", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open






