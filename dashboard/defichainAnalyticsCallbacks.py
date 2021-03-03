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


        #define callback sidebar_link_state input array
        sidebar_active_link_array_input = [Input('addresses', 'n_clicks_timestamp'),
                                           Input('daa', 'n_clicks_timestamp'),
                                           Input('fees', 'n_clicks_timestamp')]
        # define callback sidebar_link_state output array
        sidebar_active_link_array_output = [Output('addresses', 'className'),
                                            Output('daa', 'className'),
                                            Output('fees', 'className')]

        # set active links of sidebar
        @app.callback(sidebar_active_link_array_output,
                      sidebar_active_link_array_input)
        def submenu_link_state(*args):
            #change None-values to 0 to be able to compare with timestamp
            timestamp_array = []
            for item in args:
                if item is None:
                    timestamp_array.append(0)
                else:
                    timestamp_array.append(item)

            #fill return array with style information
            active_link = max(timestamp_array)
            return_array =[]
            for item in timestamp_array:
                if active_link == 0:
                    #this is necessary for the first pageload without any clicks
                    return_array.append('linkstyle')
                else:
                    if item == active_link:
                        return_array.append('activelink')
                    else:
                        return_array.append('linkstyle')

            return return_array


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