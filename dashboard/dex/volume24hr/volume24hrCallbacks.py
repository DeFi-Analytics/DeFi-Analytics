from dash.dependencies import Input, Output, State


class volume24hrCallbacksClass:
    def __init__(self, app):

        @app.callback(
            Output("modalVolume24hr", "is_open"),
            [Input("openInfoVolume24hr", "n_clicks"), Input("closeInfoVolume24hr", "n_clicks")],
            [State("modalVolume24hr", "is_open")],)
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open