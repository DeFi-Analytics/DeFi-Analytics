import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from urllib.parse import urlparse, parse_qs

PFEIL_ZU = "fas fa-chevron-right mr-3"
PFEIL_OFFEN = "fas fa-chevron-down mr-3"

class defichainAnalyticsCallbacksClass:
    def __init__(self, defichainAnalyticsModel, generalController, blockchainController, dexController, liquidityMiningController, tokenController, communityController, aboutController):
        self.defichainAnalyticsModel = defichainAnalyticsModel
        self.generalController = generalController
        self.blockchainController = blockchainController
        self.dexController = dexController
        self.liquidityMiningController = liquidityMiningController
        self.tokenController = tokenController
        self.communityController = communityController
        self.aboutController = aboutController

    def register_callbacks(self, app):

        #define the inputs for the menu_button handler
        sidebar_toggle_menu_button_inputs = [     Input("sidebarResponsiveExpandButton", 'n_clicks_timestamp'),
                                           Input('overview', 'n_clicks_timestamp'),
                                           Input('addresses', 'n_clicks_timestamp'),
                                           Input('daa', 'n_clicks_timestamp'),
                                           Input('coins', 'n_clicks_timestamp'),
                                           Input('changeCoinAdresses', 'n_clicks_timestamp'),
                                           Input('coinsAddresses', 'n_clicks_timestamp'),
                                           Input('blocktime', 'n_clicks_timestamp'),
                                           Input('transactions', 'n_clicks_timestamp'),
                                           Input('coinPrices', 'n_clicks_timestamp'),
                                           Input('volume', 'n_clicks_timestamp'),
                                           Input('liquidityToken', 'n_clicks_timestamp'),
                                           Input('tvl', 'n_clicks_timestamp'),
                                           # Input('coinsLocked', 'n_clicks_timestamp'),
                                           Input('fees', 'n_clicks_timestamp'),
                                           Input('cryptosDAT', 'n_clicks_timestamp'),
                                           Input('twitter', 'n_clicks_timestamp'),
                                           Input('changelog', 'n_clicks_timestamp'),
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

        # # this function is used to toggle the is_open property of each Collapse
        # def toggle_collapse(n, pathname, is_open, menu_name):
        #     if pathname is not None:
        #         # only if clicked, change arrow (first load, does not change the arrow)
        #         if n:
        #             #check if we are in the correct callback
        #             print(pathname,' ',menu_name)
        #             # if pathname==menu_name:
        #             if is_open:
        #                     # if menu is open (and will close), close the arrow
        #                     className = PFEIL_ZU
        #                     return False, className
        #             else:
        #                     # if menu is closed (and will open), open the arrow
        #                     className = PFEIL_OFFEN
        #                     return True, className
        #
        #
        #         #if no click happened, check if urlpath and menu_name are equal.
        #         if pathname==menu_name:
        #             #if equal, open menu
        #             return True, PFEIL_OFFEN
        #         else:
        #             #if not equal, check if we are in general menu callback
        #             if (menu_name == '/general'):
        #                 #if in general menu callback, check if path is empty
        #                 if pathname!='/':
        #                     #if path empty => close general_menu
        #                     return False, PFEIL_ZU
        #                 #else open the general menu
        #                 else:
        #                     return True, PFEIL_OFFEN
        #             else:
        #                 #if not in general menu callback, just close the menu
        #                 return False, PFEIL_ZU
        #



        # # toggle general menu
        # @app.callback([Output("submenu-general-collapse", "is_open"), Output("submenu-general-arrow", "className")],
        #               [Input("submenu-general", "n_clicks"), Input("url", "pathname")], [State("submenu-general-collapse", "is_open")])
        # def toggleGeneralMenu(n, pathname, isOpen):
        #     return toggle_collapse(n, pathname, isOpen, '/general')
        #
        # # toggle blockchain menu
        # @app.callback([Output("submenu-blockchain-collapse", "is_open"),Output("submenu-blockchain-arrow", "className")],
        #               [Input("submenu-blockchain", "n_clicks"), Input("url", "pathname")], [State("submenu-blockchain-collapse", "is_open")])
        # def toggleBlockchainMenu(n,pathname, isOpen):
        #     return toggle_collapse(n,pathname, isOpen, '/blockchain')
        #
        # # toggle dex menu
        # @app.callback(
        #     [Output("submenu-dex-collapse", "is_open"), Output("submenu-dex-arrow", "className")],
        #     [Input("submenu-dex", "n_clicks"), Input("url", "pathname")], [State("submenu-dex-collapse", "is_open")])
        # def toggleDEXMenu(n,pathname, isOpen):
        #     return toggle_collapse(n,pathname, isOpen, '/dex')
        #
        # # toggle liquidityMining menu
        # @app.callback([Output("submenu-liquidityMining-collapse", "is_open"), Output("submenu-liquidityMining-arrow", "className")],
        #               [Input("submenu-liquidityMining", "n_clicks"), Input("url", "pathname")], [State("submenu-liquidityMining-collapse", "is_open")])
        # def toggleLiquidityMiningMenu(n,pathname, isOpen):
        #     return toggle_collapse(n, pathname,isOpen, '/liquidityMining')
        #
        # # toggle token menu
        # @app.callback(
        #     [Output("submenu-token-collapse", "is_open"), Output("submenu-token-arrow", "className")],
        #     [Input("submenu-token", "n_clicks"), Input("url", "pathname")], [State("submenu-token-collapse", "is_open")])
        # def toggleTokenMenu(n,pathname, isOpen):
        #     return toggle_collapse(n,pathname, isOpen, '/token')
        #
        # # toggle community menu
        # @app.callback([Output("submenu-community-collapse", "is_open"), Output("submenu-community-arrow", "className")],
        #               [Input("submenu-community", "n_clicks"), Input("url", "pathname")], [State("submenu-community-collapse", "is_open")])
        # def toggleCommunityMenu(n,pathname, isOpen):
        #     return toggle_collapse(n,pathname, isOpen, '/community')
        #
        # # toggle about menu
        # @app.callback([Output("submenu-about-collapse", "is_open"), Output("submenu-about-arrow", "className")],
        #               [Input("submenu-about", "n_clicks"), Input("url", "pathname")], [State("submenu-about-collapse", "is_open")])
        # def toggleCommunityMenu(n, pathname, isOpen):
        #     return toggle_collapse(n, pathname, isOpen, '/about')

        sidebar_subMenu_Input_Array=[
            Input("submenu-general", "n_clicks_timestamp"),
            Input("submenu-blockchain", "n_clicks_timestamp"),
            Input("submenu-dex", "n_clicks_timestamp"),
            Input("submenu-liquidityMining", "n_clicks_timestamp"),
            Input("submenu-token", "n_clicks_timestamp"),
            Input("submenu-community", "n_clicks_timestamp"),
            Input("submenu-about", "n_clicks_timestamp"),
            Input("url", "pathname")
        ]
        sidebar_menu_Status_Array=[
            State("submenu-general-collapse", "is_open"),
            State("submenu-blockchain-collapse", "is_open"),
            State("submenu-dex-collapse", "is_open"),
            State("submenu-liquidityMining-collapse", "is_open"),
            State("submenu-token-collapse", "is_open"),
            State("submenu-community-collapse", "is_open"),
            State("submenu-about-collapse", "is_open")
        ]
        sidebar_menu_Output_Array=[
            Output("submenu-general-collapse", "is_open"),
            Output("submenu-blockchain-collapse", "is_open"),
            Output("submenu-dex-collapse", "is_open"),
            Output("submenu-liquidityMining-collapse", "is_open"),
            Output("submenu-token-collapse", "is_open"),
            Output("submenu-community-collapse", "is_open"),
            Output("submenu-about-collapse", "is_open"),
            Output("submenu-general-arrow", "className"),
            Output("submenu-blockchain-arrow", "className"),
            Output("submenu-dex-arrow", "className"),
            Output("submenu-liquidityMining-arrow", "className"),
            Output("submenu-token-arrow", "className"),
            Output("submenu-community-arrow", "className"),
            Output("submenu-about-arrow", "className")
        ]

        @app.callback(sidebar_menu_Output_Array, sidebar_subMenu_Input_Array, sidebar_menu_Status_Array)
        def toggle_collapse(*inArray):
            timestamp_array = []
            urlPath = ""
            n_clicked = False
            urlPath=inArray[7]
            timestamp_array=inArray[0:7]
            n_clicked = any(inArray[0:7])
            timestamp_array = [0 if entry is None else entry for entry in timestamp_array]

            status_Array = inArray[8:]
            status_Array = [False if entry is None else entry for entry in status_Array]



            #if there had been a click-event
            if(n_clicked):
                outArray = status_Array
                outArray[timestamp_array.index(max(timestamp_array))] = not outArray[timestamp_array.index(max(timestamp_array))]
                outArrowArray = [PFEIL_OFFEN if entry else PFEIL_ZU for entry in outArray]
                sidebar_menu_Output_Array=outArray+outArrowArray
            #     #get the clicked submenu
            #     currentlyClickedSubmenu_index = sidebar_subMenu_Input_Array.index(max(timestamp_array))
            #     for item in sidebar_menu_Status_Array:
            #         if(item.index == currentlyClickedSubmenu_index):
            #             sidebar_menu_Output_Array.append(not item)
            #             if(item):
            #                 sidebar_menu_Output_Array.append(PFEIL_ZU)
            #             else:
            #                 sidebar_menu_Output_Array.append(PFEIL_OFFEN)
            #         else:
            #             sidebar_menu_Output_Array.append(item)
            #             if (item):
            #                 sidebar_menu_Output_Array.append(PFEIL_OFFEN)
            #             else:
            #                 sidebar_menu_Output_Array.append(PFEIL_ZU)
            # #if there has been an URL event
            else:
                sidebar_menu_Output_Array = [False,
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
                                             PFEIL_ZU
                                             ]
                if urlPath in ['/', '/general']:
                    sidebar_menu_Output_Array[0] = True
                    sidebar_menu_Output_Array[7] = PFEIL_OFFEN
                elif urlPath in ['/blockchain']:
                    sidebar_menu_Output_Array[1] = True
                    sidebar_menu_Output_Array[8] = PFEIL_OFFEN
                elif urlPath in ['/dex']:
                    sidebar_menu_Output_Array[2] = True
                    sidebar_menu_Output_Array[9] = PFEIL_OFFEN
                elif urlPath in ['/liquidityMining']:
                    sidebar_menu_Output_Array[3] = True
                    sidebar_menu_Output_Array[10] = PFEIL_OFFEN
                elif urlPath in ['/token']:
                    sidebar_menu_Output_Array[4] = True
                    sidebar_menu_Output_Array[11] = PFEIL_OFFEN
                elif urlPath in ['/community']:
                    sidebar_menu_Output_Array[5] = True
                    sidebar_menu_Output_Array[12] = PFEIL_OFFEN
                elif urlPath in ['/about']:
                    sidebar_menu_Output_Array[6] = True
                    sidebar_menu_Output_Array[13] = PFEIL_OFFEN

            return sidebar_menu_Output_Array

        sidebar_link_name_array = ['overview',
                                   'addresses',
                                   'daa',
                                   'coins',
                                   'changeCoinAdresses',
                                   'coinsAddresses',
                                   'blocktime',
                                   'transactions',
                                   'coinPrices',
                                   'volume',
                                   'liquidityToken',
                                   'tvl',
                                   # 'coinsLocked',
                                   'fees',
                                   'cryptosDAT',
                                   'twitter',
                                   'changelog',
                                   'cakereview',
                                   'imprint']
        # define callback sidebar_link_state output array
        sidebar_active_link_array_output = [Output('overview', 'className'),
                                            Output('addresses', 'className'),
                                            Output('daa', 'className'),
                                            Output('coins', 'className'),
                                            Output('changeCoinAdresses', 'className'),
                                            Output('coinsAddresses', 'className'),
                                            Output('blocktime', 'className'),
                                            Output('transactions', 'className'),
                                            Output('coinPrices', 'className'),
                                            Output('volume', 'className'),
                                            Output('liquidityToken', 'className'),
                                            Output('tvl', 'className'),
                                            #Output('coinsLocked', 'className'),
                                            Output('fees', 'className'),
                                            Output('cryptosDAT', 'className'),
                                            Output('twitter', 'className'),
                                            Output('changelog', 'className'),
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
                    if urlPath != '':
                        selectedEntry = 'overview'
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

