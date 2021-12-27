import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from urllib.parse import urlparse, parse_qs

PFEIL_ZU = "fas fa-chevron-right mr-3"
PFEIL_OFFEN = "fas fa-chevron-down mr-3"

class defichainAnalyticsCallbacksClass:
    def __init__(self, defichainAnalyticsModel, generalController, blockchainController, dexController, liquidityMiningController, vaultsLoansController,
                 tokenController, communityController, aboutController):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.generalController = generalController
        self.blockchainController = blockchainController
        self.dexController = dexController
        self.liquidityMiningController = liquidityMiningController
        self.vaultsLoansController = vaultsLoansController
        self.tokenController = tokenController
        self.communityController = communityController
        self.aboutController = aboutController

    def register_callbacks(self, app):

        #define the inputs for the menu_button handler
        sidebar_toggle_menu_button_inputs = [Input("sidebarResponsiveExpandButton", 'n_clicks_timestamp'),
                                             Input('overview', 'n_clicks_timestamp'),
                                             Input('marketcap', 'n_clicks_timestamp'),
                                             Input('overallTVL', 'n_clicks_timestamp'),
                                             Input('addresses', 'n_clicks_timestamp'),
                                             Input('mn', 'n_clicks_timestamp'),
                                             Input('daa', 'n_clicks_timestamp'),
                                             Input('coins', 'n_clicks_timestamp'),
                                             Input('changeCoinAdresses', 'n_clicks_timestamp'),
                                             Input('coinsAddresses', 'n_clicks_timestamp'),
                                             Input('blocks', 'n_clicks_timestamp'),
                                             Input('blocktime', 'n_clicks_timestamp'),
                                             Input('transactions', 'n_clicks_timestamp'),
                                             Input('arbitrage', 'n_clicks_timestamp'),
                                             Input('coinprices', 'n_clicks_timestamp'),
                                             Input('volume', 'n_clicks_timestamp'),
                                             Input('24hrVolume', 'n_clicks_timestamp'),
                                             Input('stability', 'n_clicks_timestamp'),
                                             Input('slippage', 'n_clicks_timestamp'),
                                             Input('liquidityToken', 'n_clicks_timestamp'),
                                             Input('tvl', 'n_clicks_timestamp'),
                                             # Input('coinsLocked', 'n_clicks_timestamp'),
                                             Input('fees', 'n_clicks_timestamp'),
                                             Input('nbVaults', 'n_clicks_timestamp'),
                                             Input('tvlVaults', 'n_clicks_timestamp'),
                                             Input('cryptosDAT', 'n_clicks_timestamp'),
                                             Input('twitter', 'n_clicks_timestamp'),
                                             Input('follower', 'n_clicks_timestamp'),
                                             Input('analytics', 'n_clicks_timestamp'),
                                             Input('income', 'n_clicks_timestamp'),
                                             Input('portfolio', 'n_clicks_timestamp'),
                                             Input('promo', 'n_clicks_timestamp'),
                                             Input('mnmonitor', 'n_clicks_timestamp'),
                                             Input('dfx', 'n_clicks_timestamp'),
                                             Input('dfisignal', 'n_clicks_timestamp'),
                                             Input('changelog', 'n_clicks_timestamp'),
                                             Input('donate', 'n_clicks_timestamp'),
                                             Input('cakereview', 'n_clicks_timestamp'),
                                             Input('imprint', 'n_clicks_timestamp')]

        sidebar_toggle_menu_button_states = [State("menuResponsiveCollapse", "is_open")]
        # this function is used to toggle the is_open property of each Collapse of the menu_button
        @app.callback(
            Output("menuResponsiveCollapse", "is_open"),
            sidebar_toggle_menu_button_inputs,
            sidebar_toggle_menu_button_states,
        )
        def toggle_menu_collapse(*args):
            if args[0]:
                #returns on click of menu_button or link a false (link-click menu was opened already) and closes the menu
                return not args[-1]
            return args[-1]



        sidebar_subMenu_Input_Array=[
            Input("submenu-general", "n_clicks_timestamp"),
            Input("submenu-blockchain", "n_clicks_timestamp"),
            Input("submenu-dex", "n_clicks_timestamp"),
            Input("submenu-liquidityMining", "n_clicks_timestamp"),
            Input("submenu-vaultsLoans", "n_clicks_timestamp"),
            Input("submenu-token", "n_clicks_timestamp"),
            Input("submenu-community", "n_clicks_timestamp"),
            Input("submenu-about", "n_clicks_timestamp"),
            Input("url", "pathname"),
            Input("hiddenDivTimestampsMenuClicked", "children")
        ]
        sidebar_menu_Status_Array=[
            State("submenu-general-collapse", "is_open"),
            State("submenu-blockchain-collapse", "is_open"),
            State("submenu-dex-collapse", "is_open"),
            State("submenu-liquidityMining-collapse", "is_open"),
            State("submenu-vaultsLoans-collapse", "is_open"),
            State("submenu-token-collapse", "is_open"),
            State("submenu-community-collapse", "is_open"),
            State("submenu-about-collapse", "is_open")
        ]
        sidebar_menu_Output_Array=[
            Output("submenu-general-collapse", "is_open"),
            Output("submenu-blockchain-collapse", "is_open"),
            Output("submenu-dex-collapse", "is_open"),
            Output("submenu-liquidityMining-collapse", "is_open"),
            Output("submenu-vaultsLoans-collapse", "is_open"),
            Output("submenu-token-collapse", "is_open"),
            Output("submenu-community-collapse", "is_open"),
            Output("submenu-about-collapse", "is_open"),
            Output("submenu-general-arrow", "className"),
            Output("submenu-blockchain-arrow", "className"),
            Output("submenu-dex-arrow", "className"),
            Output("submenu-liquidityMining-arrow", "className"),
            Output("submenu-vaultsLoans-arrow", "className"),
            Output("submenu-token-arrow", "className"),
            Output("submenu-community-arrow", "className"),
            Output("submenu-about-arrow", "className"),
            Output("hiddenDivTimestampsMenuClicked", "children")
        ]

        @app.callback(sidebar_menu_Output_Array, sidebar_subMenu_Input_Array, sidebar_menu_Status_Array)
        def toggle_collapse(*inArray):
            urlPath=inArray[8]
            strTimestampFromDiv=inArray[9]

            # new timestamps
            timestamp_array=inArray[0:8]
            timestamp_array = [0 if entry is None else entry for entry in timestamp_array]
            strTimestampForDiv = ' '.join(str(entry) for entry in timestamp_array)

            # old timestamps
            timestamp_oldArrayString = strTimestampFromDiv.split()                      # generate list of strings from string
            timestamp_oldArray = [int(entry) for entry in timestamp_oldArrayString]     # convert string entries to int entries

            n_clicked = not(timestamp_oldArray == timestamp_array)                      # compare old and new timestamp list, true if different (clicked)
            urlLoadPage = not any(timestamp_oldArray)                                   # check if all old timestamp entries are 0 => page initially loaded

            status_Array = inArray[10:]
            status_Array = [False if entry is None else entry for entry in status_Array]

           #if there had been a click-event
            if(n_clicked):
                outArray = status_Array
                outArray[timestamp_array.index(max(timestamp_array))] = not outArray[timestamp_array.index(max(timestamp_array))]
                outArrowArray = [PFEIL_OFFEN if entry else PFEIL_ZU for entry in outArray]
                sidebar_menu_Output_Array=outArray+outArrowArray+[strTimestampForDiv]

            elif (urlLoadPage):
                sidebar_menu_Output_Array = [False,
                                             False,
                                             False,
                                             False,
                                             False,
                                             False,
                                             False,
                                             False,
                                             PFEIL_ZU,
                                             PFEIL_ZU,
                                             PFEIL_ZU,
                                             PFEIL_ZU,
                                             PFEIL_ZU,
                                             PFEIL_ZU,
                                             PFEIL_ZU,
                                             PFEIL_ZU,
                                             strTimestampForDiv]
                if urlPath in ['/', '/general']:
                    sidebar_menu_Output_Array[0] = True
                    sidebar_menu_Output_Array[8] = PFEIL_OFFEN
                elif urlPath in ['/blockchain']:
                    sidebar_menu_Output_Array[1] = True
                    sidebar_menu_Output_Array[9] = PFEIL_OFFEN
                elif urlPath in ['/dex']:
                    sidebar_menu_Output_Array[2] = True
                    sidebar_menu_Output_Array[10] = PFEIL_OFFEN
                elif urlPath in ['/liquidityMining']:
                    sidebar_menu_Output_Array[3] = True
                    sidebar_menu_Output_Array[11] = PFEIL_OFFEN
                elif urlPath in ['/vaultsLoans']:
                    sidebar_menu_Output_Array[4] = True
                    sidebar_menu_Output_Array[12] = PFEIL_OFFEN
                elif urlPath in ['/token']:
                    sidebar_menu_Output_Array[5] = True
                    sidebar_menu_Output_Array[13] = PFEIL_OFFEN
                elif urlPath in ['/community']:
                    sidebar_menu_Output_Array[6] = True
                    sidebar_menu_Output_Array[14] = PFEIL_OFFEN
                elif urlPath in ['/about']:
                    sidebar_menu_Output_Array[7] = True
                    sidebar_menu_Output_Array[15] = PFEIL_OFFEN
            else:
                outArray = status_Array
                outArrowArray = [PFEIL_OFFEN if entry else PFEIL_ZU for entry in outArray]
                sidebar_menu_Output_Array = outArray+outArrowArray+[strTimestampForDiv]

            return sidebar_menu_Output_Array

        sidebar_link_name_array = ['overview',
                                   'marketcap',
                                   'overallTVL',
                                   'addresses',
                                   'mn',
                                   'daa',
                                   'coins',
                                   'changeCoinAdresses',
                                   'coinsAddresses',
                                   'blocks',
                                   'blocktime',
                                   'transactions',
                                   'arbitrage',
                                   'coinprices',
                                   'volume',
                                   '24hrVolume',
                                   'stability',
                                   'slippage',
                                   'liquidityToken',
                                   'tvl',
                                   # 'coinsLocked',
                                   'fees',
                                   'nbVaults',
                                   'tvlVaults',
                                   'cryptosDAT',
                                   'twitter',
                                   'follower',
                                   'analytics',
                                   'income',
                                   'portfolio',
                                   'promo',
                                   'mnmonitor',
                                   'dfx',
                                   'dfisignal',
                                   'changelog',
                                   'donate',
                                   'cakereview',
                                   'imprint']
        # define callback sidebar_link_state output array
        sidebar_active_link_array_output = [Output('overview', 'className'),
                                            Output('marketcap', 'className'),
                                            Output('overallTVL', 'className'),
                                            Output('addresses', 'className'),
                                            Output('mn', 'className'),
                                            Output('daa', 'className'),
                                            Output('coins', 'className'),
                                            Output('changeCoinAdresses', 'className'),
                                            Output('coinsAddresses', 'className'),
                                            Output('blocks', 'className'),
                                            Output('blocktime', 'className'),
                                            Output('transactions', 'className'),
                                            Output('arbitrage', 'className'),
                                            Output('coinprices', 'className'),
                                            Output('volume', 'className'),
                                            Output('24hrVolume', 'className'),
                                            Output('stability', 'className'),
                                            Output('slippage', 'className'),
                                            Output('liquidityToken', 'className'),
                                            Output('tvl', 'className'),
                                            #Output('coinsLocked', 'className'),
                                            Output('fees', 'className'),
                                            Output('nbVaults', 'className'),
                                            Output('tvlVaults', 'className'),
                                            Output('cryptosDAT', 'className'),
                                            Output('twitter', 'className'),
                                            Output('follower', 'className'),
                                            Output('analytics', 'className'),
                                            Output('income', 'className'),
                                            Output('portfolio', 'className'),
                                            Output('promo', 'className'),
                                            Output('mnmonitor', 'className'),
                                            Output('dfx', 'className'),
                                            Output('dfisignal', 'className'),
                                            Output('changelog', 'className'),
                                            Output('donate', 'className'),
                                            Output('cakereview', 'className'),
                                            Output('imprint', 'className')
                                            ]

        # set active links of sidebar, when url changes
        @app.callback(sidebar_active_link_array_output,
                      [Input("url", "href")])
        def sidebar_link_state(hrefPath):
            return_array = []
            #parse url
            if hrefPath is not None:
                completeURL = urlparse(hrefPath)
                URLqueryEntries = parse_qs(completeURL.query)
                urlPath = completeURL.path
                if 'entry' in URLqueryEntries:
                    selectedEntry = URLqueryEntries['entry'][0]
                else:
                    #if it is the initial access to the main html and no path is given, the overview shall be selected
                    if urlPath in ['/','/general']:
                        selectedEntry = 'overview'
                    elif urlPath == '/blockchain':
                        selectedEntry = 'addresses'
                    elif urlPath == '/dex':
                        selectedEntry = 'coinPrices'
                    elif urlPath == '/liquidityMining':
                        selectedEntry = 'tvl'
                    elif urlPath == '/vaultsLoans':
                        selectedEntry = 'nbVaults'
                    elif urlPath == '/token':
                        selectedEntry = 'cryptosDAT'
                    elif urlPath == '/community':
                        selectedEntry = 'twitter'
                    elif urlPath == '/about':
                        selectedEntry = 'changelog'
                    else:
                        selectedEntry = ''
            else:
                selectedEntry = ''

            #for each check of the link_name_array
            for item in sidebar_link_name_array:
                if(item ==selectedEntry):
                    #add a activeLink classname to the return array if the item equals the selectedEntry
                    return_array.append('sidebarActivelink')
                else:
                    #add a normal linkstyle if the item is not equally
                    return_array.append('sidebarLinkstyle')

            return return_array


        # callback, listening on URL and returns the URL-related content and idVersion
        @app.callback([Output("page-content", "children"),
                       Output("idVersion", "children")], [Input("url", "href")])
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

            if urlPath in ["/", "/general"]:
                pageContent = self.generalController.getContent(selectedEntry)
            elif urlPath in ["/blockchain"]:
                pageContent = self.blockchainController.getContent(selectedEntry)
            elif urlPath in ["/dex"]:
                pageContent = self.dexController.getContent(selectedEntry)
            elif urlPath in ["/liquidityMining"]:
                pageContent = self.liquidityMiningController.getContent(selectedEntry)
            elif urlPath in ["/vaultsLoans"]:
                pageContent = self.vaultsLoansController.getContent(selectedEntry)
            elif urlPath in ["/token"]:
                pageContent = self.tokenController.getContent(selectedEntry)
            elif urlPath in ["/community"]:
                pageContent = self.communityController.getContent(selectedEntry)
            elif urlPath in ['/about']:
                pageContent = self.aboutController.getContent(selectedEntry)
            # If the user tries to reach a different page, return a 404 message
            else:
                pageContent = dbc.Jumbotron([html.H1("404: Not found", className="text-danger"),
                                             html.Hr(),
                                             html.P(f"The pathname {urlPath} was not recognised..."),])

            # check changelog data and update version information
            self.defichainAnalyticsModel.loadChangelogData()
            versionContent = 'Version ' + self.defichainAnalyticsModel.changelogData.Version.values[0]

            return pageContent, versionContent

