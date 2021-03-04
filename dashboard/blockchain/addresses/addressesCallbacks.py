from dash.dependencies import Input, Output, State

class addressesCallbacksClass:

    @staticmethod
    def register_callbacks(app):
        @app.callback(
            Output("modalAddresses", "is_open"),
            [Input("openInfoAddresses", "n_clicks"), Input("closeInfoAddresses", "n_clicks")],
            [State("modalAddresses", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open