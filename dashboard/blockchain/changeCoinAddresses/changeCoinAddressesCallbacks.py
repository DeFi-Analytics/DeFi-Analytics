from dash.dependencies import Input, Output, State


class changeCoinAddressesCallbacksClass:
    def __init__(self):
        None


    def register_callbacks(self, app):
        # this function is used to toggle the is_open property of each Collapse
        print('######################')
        # @app.callback(
        #     Output("hidden", "content"),
        #     [Input("openInfoChangeCoinAddresses", "n_clicks")],
        #     State('modalChangeCoinAddresses', 'is_open')
        # )
        # def toggle_modal(n1, is_open):
        #     print('#################### Callback reached')
        #     if n1 :
        #         return not is_open
        #     return is_open

        @app.callback(
            Output("modalChangeCoinAddresses", "is_open"),
            [Input("openInfoChangeCoinAddresses", "n_clicks"), Input("closeInfoChangeCoinAddresses", "n_clicks")],
            [State("modalChangeCoinAddresses", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open