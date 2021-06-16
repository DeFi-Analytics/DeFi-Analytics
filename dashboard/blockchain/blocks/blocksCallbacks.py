from dash.dependencies import Input, Output, State


class blocksCallbacksClass:
    def __init__(self, app):
        @app.callback(
            Output("modalBlocks", "is_open"),
            [Input("openInfoBlocks", "n_clicks"), Input("closeInfoBlocks", "n_clicks")],
            [State("modalBlocks", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open
