from dash.dependencies import Input, Output, State


class volumeCallbacksClass:
    def __init__(self, app):

        @app.callback(
            Output("modalVolume", "is_open"),
            [Input("openInfoVolume", "n_clicks"), Input("closeInfoVolume", "n_clicks")],
            [State("modalVolume", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open