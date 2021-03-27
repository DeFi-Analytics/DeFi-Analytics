from dash.dependencies import Input, Output, State


class twitterCallbacksClass:
    def __init__(self, app):

        @app.callback(
            Output("modalTwitter", "is_open"),
            [Input("openInfoTwitter", "n_clicks"), Input("closeInfoTwitter", "n_clicks")],
            [State("modalTwitter", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open
