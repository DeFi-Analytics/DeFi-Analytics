import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from urllib.parse import urlparse, parse_qs

PFEIL_ZU = "fas fa-chevron-right mr-3"
PFEIL_OFFEN = "fas fa-chevron-down mr-3"

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

        # this function is used to toggle the is_open property of each Collapse
        def toggle_collapse(n, is_open):
            # only if clicked, change arrow (first load, does not change the arrow)
            if n:
                if is_open:
                    # if menu is open (and will close), close the arrow
                    className = PFEIL_ZU
                else:
                    # if menu is closed (and will open), open the arrow
                    className = PFEIL_OFFEN
                # toggle is_open and return with arrow
                return not is_open, className
            # if it is initial, just give a closed arrow
            return is_open, PFEIL_ZU


        # toggle blockchain menu
        @app.callback([Output("submenu-blockchain-collapse", "is_open"),Output("submenu-blockchain-arrow", "className")],
                      [Input("submenu-blockchain", "n_clicks")], [State("submenu-blockchain-collapse", "is_open")])
        def toggleBlockchainMenu(n,isOpen):
            return toggle_collapse(n,isOpen)

        # toggle liquidityMining menu
        @app.callback([Output("submenu-liquidityMining-collapse", "is_open"), Output("submenu-liquidityMining-arrow", "className")],
                      [Input("submenu-liquidityMining", "n_clicks")], [State("submenu-liquidityMining-collapse", "is_open")])
        def toggleLiquidityMiningMenu(n,isOpen):
            return toggle_collapse(n,isOpen)

        # set active link
        @app.callback([Output('addresses', 'className'), Output('daa', 'className'), Output('fees', 'className')],
                       [Input('addresses', 'n_clicks_timestamp'), Input('daa', 'n_clicks_timestamp'), Input('fees', 'n_clicks_timestamp')])
        def addresses_state1(n_addy, n_daa, n_fees):
            if n_daa==None: n_daa=0;
            if n_fees==None: n_fees=0;
            if n_addy==None: n_addy=0;

            if (n_addy > n_daa and n_addy > n_fees):
                return 'activelink', 'linkstyle', 'linkstyle'
            elif n_daa>n_addy and n_daa>n_fees:
                return 'linkstyle' , 'activelink', 'linkstyle'
            elif n_fees>n_addy and n_fees>n_daa:
                return 'linkstyle', 'linkstyle', 'activelink'
            else:
                return 'activelink', 'linkstyle', 'linkstyle'

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