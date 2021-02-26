import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from urllib.parse import urlparse, parse_qs

class defichainAnalyticsCallbacksClass:
    def __init__(self, blockchainController, liquidityMiningController, submenu2Controller):
        self.blockchainController = blockchainController
        self.submenu2Controller = submenu2Controller
        self.liquidityMiningController = liquidityMiningController

    def register_callbacks(self, app):
        # this function is used to toggle the is_open property of each Collapse
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open


        # this function applies the "open" class to rotate the chevron
        def set_navitem_class(is_open):
            if is_open:
                return "open"
            return ""


        for i in [1, 2]:
            app.callback(
                Output(f"submenu-{i}-collapse", "is_open"),
                [Input(f"submenu-{i}", "n_clicks")],
                [State(f"submenu-{i}-collapse", "is_open")],
            )(toggle_collapse)

            app.callback(
                Output(f"submenu-{i}", "className"),
                [Input(f"submenu-{i}-collapse", "is_open")],
            )(set_navitem_class)

        # toggle blockchain menu
        @app.callback(Output("submenu-blockchain-collapse", "is_open"),[Input("submenu-blockchain", "n_clicks")],[State("submenu-blockchain-collapse", "is_open")])
        def toggleBlockchainMenu(n,isOpen):
            return toggle_collapse(n,isOpen)

        # toggle liquidityMining menu
        @app.callback(Output("submenu-liquidityMining-collapse", "is_open"),[Input("submenu-liquidityMining", "n_clicks")],[State("submenu-liquidityMining-collapse", "is_open")])
        def toggleLiquidityMiningMenu(n,isOpen):
            return toggle_collapse(n,isOpen)

        @app.callback(Output("page-content", "children"), [Input("url", "href")])
        def render_page_content(hrefPath):
            if hrefPath is not None:
                completeURL = urlparse(hrefPath)
                URLqueryEntries = parse_qs(completeURL.query)
                urlPath = completeURL.path
                if 'entry' in URLqueryEntries:
                    selectedEntry = URLqueryEntries['entry'][0]
                else:
                    selectedEntry = ''
            else:
                urlPath = '/'
                selectedEntry = ''

            if urlPath in ["/", "/blockchain"]:
                return self.blockchainController.getContent(selectedEntry)
            elif urlPath in ["/liquidityMining"]:
                return self.liquidityMiningController.getContent(selectedEntry)
            elif urlPath in ["/page-2/1", "/page-2/2"]:
                return self.submenu2Controller.getContent(urlPath)

            # If the user tries to reach a different page, return a 404 message
            return dbc.Jumbotron(
                [
                    html.H1("404: Not found", className="text-danger"),
                    html.Hr(),
                    html.P(f"The pathname {urlPath} was not recognised..."),
                ]
            )