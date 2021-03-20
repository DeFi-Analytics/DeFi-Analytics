import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import os
import base64

PFEIL_ZU = "fas fa-chevron-right mr-3"
PFEIL_OFFEN = "fas fa-chevron-down mr-3"

class defichainAnalyticsViewClass:
    def __init__(self):


        #define submenu_blockchain
        submenu_blockchain = [
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        #submenu_name is "Blockchain"
                        dbc.Col("Blockchain"),
                        dbc.Col(
                            html.I(className=PFEIL_ZU, id="submenu-blockchain-arrow"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                className="submenu_linkstyle",
                id="submenu-blockchain",
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                [
                    dbc.NavLink("Addresses", href="/blockchain?entry=addresses", className="linkstyle", id="addresses"),
                    dbc.NavLink("DAA", href="/blockchain?entry=daa", className="linkstyle", id="daa"),
                    dbc.NavLink("Coins", href="/blockchain?entry=coin", className="linkstyle", id="coins"),
                    dbc.NavLink("Change Coins/Addresses", href="/blockchain?entry=changeCoinAdresses", className="linkstyle", id="change"),
                    dbc.NavLink("Coins/Addresses", href="/blockchain?entry=coinsAddresses", className="linkstyle", id="coinsAddresses"),
                    dbc.NavLink("Block Time", href="/blockchain?entry=blocktime", className="linkstyle", id="blockTime"),
                    dbc.NavLink("Transactions", href="/blockchain?entry=transactions", className="linkstyle", id="transactions")
                ],
                id="submenu-blockchain-collapse",
            ),
        ]

        submenu_dex = [
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        # submenu_name is "Blockchain"
                        dbc.Col("DEX"),
                        dbc.Col(
                            html.I(className=PFEIL_ZU, id="submenu-dex-arrow"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                className="submenu_linkstyle",
                id="submenu-dex",
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                [
                    dbc.NavLink("Coinprices", href="/blockchain?entry=coinprices", className="linkstyle", id="coinPrices"),
                    dbc.NavLink("Volume", href="/blockchain?entry=volume", className="linkstyle", id="volume"),
                ],
                id="submenu-dex-collapse",
            ),
        ]

        submenu_liquidityMining = [
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        dbc.Col("Liquidity Mining"),
                        dbc.Col(
                            html.I(className=PFEIL_ZU, id="submenu-liquidityMining-arrow"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                className="submenu_linkstyle",
                id="submenu-liquidityMining",
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                [
                    dbc.NavLink("Liquidity Token", href="/liquidityMining?entry=liquidityToken", className="linkstyle", id="liquidityToken"),
                    dbc.NavLink("TVL", href="/liquidityMining?entry=tvl", className="linkstyle", id="tvl"),
                    #dbc.NavLink("Coins locked", href="/liquidityMining?entry=coinsLocked", className="linkstyle", id="coinsLocked"),
                    dbc.NavLink("Fees", href="/liquidityMining?entry=fees", className="linkstyle", id="fees")
                ],
                id="submenu-liquidityMining-collapse",
            ),
        ]

        submenu_token = [
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        # submenu_name is "Blockchain"
                        dbc.Col("Token"),
                        dbc.Col(
                            html.I(className=PFEIL_ZU, id="submenu-token-arrow"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                className="submenu_linkstyle",
                id="submenu-token",
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                [
                    dbc.NavLink("Cryptos-DAT", href="/blockchain?entry=cryptosDAT", className="linkstyle",
                                id="cryptosDAT")
                ],
                id="submenu-token-collapse",
            ),
        ]


        workDir = os.path.abspath(os.getcwd())
        image_filename = workDir + '/assets/'+'logo-defi-analytics.png'
        encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')


        sidebar = html.Div(
            [

                html.Img(src='data:image/png;base64,{}'.format(encoded_image),
                         className="logo_sidebar"),
                dbc.Col(
                    html.Button(
                        # use the Bootstrap navbar-toggler classes to style the toggle
                        html.Span(className="navbar-toggler-icon"),
                        className="navbar-toggler",
                        # the navbar-toggler classes don't set color, so we do it here
                        style={
                            "color": "rgba(0,0,0,.5)",
                            "border-color": "rgba(0,0,0,.1)",
                        },
                        id="toggle",
                    ),
                    # the column containing the toggle will be only as wide as the
                    # toggle, resulting in the toggle being right aligned
                    width="auto",
                    # vertically align the toggle in the center
                    align="center",
                ),
                dbc.Collapse(
                    html.Div(dbc.Nav(submenu_blockchain + submenu_dex + submenu_liquidityMining + submenu_token,
                            vertical=True, id='navbar-container'), className="scrollbar_sidemenu"),
                    id="menu_collapse", className="menu_collapse")

            ],
            className="sidebarstyle",
            id="sidebar",
        )

        MainWindow = dcc.Loading(html.Div(id="page-content", className="contentstyle"), type="default")
        self.layout = html.Div([dcc.Location(id="url"), sidebar, MainWindow])
