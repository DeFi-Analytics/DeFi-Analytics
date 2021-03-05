from dash.dependencies import Input, Output, State


class transactionsCallbacksClass:

    @staticmethod
    def register_callbacks(app):
        @app.callback(
            Output("modalTransactions", "is_open"),
            [Input("openInfoTransactions", "n_clicks"), Input("closeInfoTransactions", "n_clicks")],
            [State("modalTransactions", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:                    # needed for close button
                return not is_open
            return is_open