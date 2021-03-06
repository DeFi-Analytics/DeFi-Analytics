from dash.dependencies import Input, Output, State


class daaCallbacksClass:
    def __init__(self, app):
        @app.callback(
            Output("modalDAA", "is_open"),
            [Input("openInfoDAA", "n_clicks"), Input("closeInfoDAA", "n_clicks")],
            [State("modalDAA", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open
