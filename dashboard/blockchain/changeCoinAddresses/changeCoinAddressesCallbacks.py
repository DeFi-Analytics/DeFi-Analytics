from dash.dependencies import Input, Output, State


class changeCoinAddressesCallbacksClass:
    def __init__(self, app):

        @app.callback(
            Output("modalChangeCoinAddresses", "is_open"),
            [Input("openInfoChangeCoinAddresses", "n_clicks"), Input("closeInfoChangeCoinAddresses", "n_clicks")],
            [State("modalChangeCoinAddresses", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open
