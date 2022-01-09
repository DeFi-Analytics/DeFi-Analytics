from dash.dependencies import Input, Output, State


class burnedDFICallbacksClass:
    def __init__(self, app):

        @app.callback(
            Output("modalBurnedDFI", "is_open"),
            [Input("openInfoBurnedDFI", "n_clicks"), Input("closeInfoBurnedDFI", "n_clicks")],
            [State("modalBurnedDFI", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open
