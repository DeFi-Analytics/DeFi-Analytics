from dash.dependencies import Input, Output, State


class blocktimeCallbacksClass:
    def __init__(self, app):

        @app.callback(
            Output("modalBlocktime", "is_open"),
            [Input("openInfoBlocktime", "n_clicks"), Input("closeInfoBlocktime", "n_clicks")],
            [State("modalBlocktime", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open
