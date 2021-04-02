import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import os
import base64

PFEIL_ZU = "fas fa-chevron-right mr-3"
PFEIL_OFFEN = "fas fa-chevron-down mr-3"

class defichainAnalyticsViewClass:
    def __init__(self):

        submenu_general = [
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        # submenu_name is "Blockchain"
                        dbc.Col("General"),
                        dbc.Col(
                            html.I(className=PFEIL_ZU, id="submenu-general-arrow"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                className="submenu_linkstyle",
                id="submenu-general",
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                [
                    dbc.NavLink("Overview", href="/general?entry=overview", className="linkstyle",
                                id="overview")
                ],
                id="submenu-general-collapse",
            ),
        ]

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
                    dbc.NavLink("Coinprices", href="/dex?entry=coinprices", className="linkstyle", id="coinPrices"),
                    dbc.NavLink("Volume", href="/dex?entry=volume", className="linkstyle", id="volume"),
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
                    dbc.NavLink("Cryptos-DAT", href="/token?entry=cryptosDAT", className="linkstyle",
                                id="cryptosDAT")
                ],
                id="submenu-token-collapse",
            ),
        ]

        submenu_community = [
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        # submenu_name is "Blockchain"
                        dbc.Col("Community"),
                        dbc.Col(
                            html.I(className=PFEIL_ZU, id="submenu-community-arrow"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                className="submenu_linkstyle",
                id="submenu-community",
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                [
                    dbc.NavLink("Twitter", href="/community?entry=twitter", className="linkstyle",
                                id="twitter")
                ],
                id="submenu-community-collapse",
            ),
        ]

        submenu_about = [
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        # submenu_name is "Blockchain"
                        dbc.Col("About"),
                        dbc.Col(
                            html.I(className=PFEIL_ZU, id="submenu-about-arrow"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                className="submenu_linkstyle",
                id="submenu-about",
                style={'margin-top': '20px'}
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                [
                    dbc.NavLink("Changelog", href="/about?entry=changelog", className="linkstyle", id="changelog"),
                    dbc.NavLink("CakeDefi-Review", href="/about?entry=cakereview", className="linkstyle", id="cakereview"),
                    dbc.NavLink("Imprint", href="/about?entry=imprint", className="linkstyle", id="imprint")
                ],
                id="submenu-about-collapse",
            ),
        ]

        sidebar_header = dbc.Row(
            [
                dbc.Col(
                    html.Button(
                        title="Menu",
                        id="sidebarResponsiveExpandButton",
                        className="sidebar_button"
                    ),

                ),

                dbc.Col([html.Div(id='idLogoSidebar'),
                         html.Div(id='idVersion')]),

                dbc.Col(),
            ],
            id="header",
            className="headerStyle",
        )

        refLink = html.Div(html.Marquee(['Special ',
                      html.A('Cake', href='https://app.cakedefi.com/?ref=476728', target='_blank'),
                      ' offer: Sign-up Bonus of $20 in DFI (after deposit of $50). You and me get $10 additional in DFI if you use my ',
                      html.A('Ref-Link', href='https://app.cakedefi.com/?ref=476728', target='_blank'),
                      '. Cake is also gateway for your BTC, ETH and USDT to the DeFiChain-Wallet. ',
                      html.A('Offer', href='https://app.cakedefi.com/?ref=476728', target='_blank'),
                      ' Condition: DFI are staking for at least 180 days and generate revenue of ~37% APY.']), className='refLinkMarquee')

        sidebar = html.Div(
            [
                sidebar_header,

                dbc.Collapse(
                    html.Div(dbc.Nav(submenu_general + submenu_blockchain + submenu_dex + submenu_liquidityMining + submenu_token + submenu_community + submenu_about,
                            vertical=True, id='navbar-container'), className="scrollbar_sidemenu"),
                    id="menuResponsiveCollapse", className="menu_collapse")

            ],
            className="sidebarstyle",
            id="sidebar",
        )

        MainWindow = dcc.Loading([html.Div(id="page-content", className="contentstyle"),refLink], type="default")
        self.layout = html.Div([dcc.Location(id="url"), sidebar, MainWindow])
