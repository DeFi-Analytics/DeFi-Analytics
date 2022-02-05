from dash.dependencies import Input, Output, State


class premiumCallbacksClass:
    def __init__(self, app):

        @app.callback(
            Output("modalPremiumDToken", "is_open"),
            [Input("openInfoPremiumDToken", "n_clicks"), Input("closeInfoPremiumDToken", "n_clicks")],
            [State("modalPremiumDToken", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open
