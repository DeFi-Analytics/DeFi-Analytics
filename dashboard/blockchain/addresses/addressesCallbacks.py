import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State


class addressesCallbacksClass:
    def __init__(self):
        None


    def register_callbacks(self, app):
        # this function is used to toggle the is_open property of each Collapse
        @app.callback(
            Output("output", "children"),
            Input("input1", "value"),
        )
        def update_output(input1):
            return input1