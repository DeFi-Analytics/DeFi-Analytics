from dash.dependencies import Input, Output, State


class nbVaultsCallbacksClass:
    def __init__(self, app):

        @app.callback(
            Output("modalNbVaults", "is_open"),
            [Input("openInfoNbVaults", "n_clicks"), Input("closeInfoNbVaults", "n_clicks")],
            [State("modalNbVaults", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open
