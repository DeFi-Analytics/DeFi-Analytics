from dash.dependencies import Input, Output, State


class coinCallbacksClass:
    def __init__(self, app):

        @app.callback(
            Output("modalCoin", "is_open"),
            [Input("openInfoCoin", "n_clicks"), Input("closeInfoCoin", "n_clicks")],
            [State("modalCoin", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

