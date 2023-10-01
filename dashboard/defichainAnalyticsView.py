import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


PFEIL_ZU = "fas fa-chevron-right mr-3"
PFEIL_OFFEN = "fas fa-chevron-down mr-3"

class defichainAnalyticsViewClass:
    def trackVisit(self):
        scriptPath = __file__
        path = scriptPath[:-36] + '/data/'
        filepath = path + 'rawDataUserVisit.csv'

        start_time = pd.Timestamp.now()
        dfUSer = pd.DataFrame(data=[start_time], columns=['TimeStamp'])
        dfUSer.to_csv(filepath, mode='a', header=False)
        print('##################### '+str(start_time))

    def getDashboardLayout(self):
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
                    dbc.NavLink("Overview", href="/general?entry=overview", className="linkstyle", id="overview"),
                    dbc.NavLink("Market Cap", href="/general?entry=marketcap", className="linkstyle", id="marketcap"),
                    dbc.NavLink("Overall TVL", href="/general?entry=overallTVL", className="linkstyle", id="overallTVL"),
                    dbc.NavLink("DFI emission", href="/general?entry=emission", className="linkstyle", id="emission"),
                    dbc.NavLink("Inflation", href="/general?entry=inflation", className="linkstyle", id="inflation"),
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
                    dbc.NavLink("Masternodes", href="/blockchain?entry=mn", className="linkstyle", id="mn"),
                    dbc.NavLink("Daily Active Addresses", href="/blockchain?entry=daa", className="linkstyle", id="daa"),
                    dbc.NavLink("Coins", href="/blockchain?entry=coins", className="linkstyle", id="coins"),
                    dbc.NavLink("Change Coins/Addresses", href="/blockchain?entry=changeCoinAdresses", className="linkstyle", id="changeCoinAdresses"),
                    dbc.NavLink("Coins/Addresses", href="/blockchain?entry=coinsAddresses", className="linkstyle", id="coinsAddresses"),
                    dbc.NavLink("Blocks", href="/blockchain?entry=blocks", className="linkstyle", id="blocks"),
                    dbc.NavLink("Block Time", href="/blockchain?entry=blocktime", className="linkstyle", id="blocktime"),
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
                    dbc.NavLink("Arbitrage", href="/dex?entry=arbitrage", className="linkstyle", id="arbitrage"),
                    dbc.NavLink("Coinprices", href="/dex?entry=coinprices", className="linkstyle", id="coinprices"),
                    dbc.NavLink("Volume", href="/dex?entry=volume", className="linkstyle", id="volume"),
                    dbc.NavLink("Volume (24hr)", href="/dex?entry=24hrVolume", className="linkstyle", id="24hrVolume"),
                    dbc.NavLink("Price Stability", href="/dex?entry=stability", className="linkstyle", id="stability"),
                    dbc.NavLink("Price Slippage", href="/dex?entry=slippage", className="linkstyle", id="slippage"),
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
                    dbc.NavLink("TVL", href="/liquidityMining?entry=tvl", className="linkstyle", id="tvl"),
                    dbc.NavLink("Liquidity Token", href="/liquidityMining?entry=liquidityToken", className="linkstyle", id="liquidityToken"),
                    dbc.NavLink("APR Rates", href="/liquidityMining?entry=apr", className="linkstyle", id="apr"),
                    dbc.NavLink("Fees", href="/liquidityMining?entry=fees", className="linkstyle", id="fees")
                ],
                id="submenu-liquidityMining-collapse",
            ),
        ]

        submenu_vaultsLoans = [
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        dbc.Col("Vaults & Loans"),
                        dbc.Col(
                            html.I(className=PFEIL_ZU, id="submenu-vaultsLoans-arrow"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                className="submenu_linkstyle",
                id="submenu-vaultsLoans",
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                [
                    dbc.NavLink("Number vaults", href="/vaultsLoans?entry=nbVaults", className="linkstyle", id="nbVaults"),
                    dbc.NavLink("TVL vaults", href="/vaultsLoans?entry=tvlVaults", className="linkstyle", id="tvlVaults"),
                    dbc.NavLink("dToken prices", href="/vaultsLoans?entry=dTokenPrices", className="linkstyle", id="dTokenPrices"),
                    dbc.NavLink("dToken premium", href="/vaultsLoans?entry=premium", className="linkstyle", id="premium"),
                    dbc.NavLink("Number dToken", href="/vaultsLoans?entry=nbDToken", className="linkstyle", id="nbDToken"),
                    dbc.NavLink("Futures Swap value", href="/vaultsLoans?entry=fsValue", className="linkstyle", id="fsValue"),
                    dbc.NavLink("Rel. part algo/circ amount", href="/vaultsLoans?entry=partAlgoCirc", className="linkstyle", id="partAlgoCirc"),
                    dbc.NavLink("Open Interest", href="/vaultsLoans?entry=interest", className="linkstyle", id="interest"),
                    dbc.NavLink("dUSD Measures", href="/vaultsLoans?entry=dUSDMeasures", className="linkstyle", id="dUSDMeasures"),
                    dbc.NavLink("DFI Burn", href="/vaultsLoans?entry=burnedDFI", className="linkstyle", id="burnedDFI"),
                    dbc.NavLink("Loan schemes", href="/vaultsLoans?entry=scheme", className="linkstyle", id="scheme"),
                ],
                id="submenu-vaultsLoans-collapse",
            ),
        ]

        submenu_bscBridge = [
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        # submenu_name is "Blockchain"
                        dbc.Col("BSC-Bridge"),
                        dbc.Col(
                            html.I(className=PFEIL_ZU, id="submenu-bscBridge-arrow"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                className="submenu_linkstyle",
                id="submenu-bscBridge",
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                [
                    dbc.NavLink("Bridge liquidity", href="/bscBridge?entry=liquidityBridge", className="linkstyle", id="liquidityBridge"),
                    dbc.NavLink("Bridge in-/outflow", href="/bscBridge?entry=inOutFlow", className="linkstyle", id="inOutFlow"),
                    dbc.NavLink("Number Bridge swaps", href="/bscBridge?entry=nbSwapsBridge", className="linkstyle", id="nbSwapsBridge"),
                ],
                id="submenu-bscBridge-collapse",
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
                    dbc.NavLink("Twitter", href="/community?entry=twitter", className="linkstyle", id="twitter"),
                    dbc.NavLink("Twitter Follower", href="/community?entry=follower", className="linkstyle", id="follower"),
                    dbc.NavLink("Reddit Members", href="/community?entry=reddit", className="linkstyle", id="reddit"),
                    dbc.NavLink("CFP List", href="/community?entry=cfp", className="linkstyle", id="cfp"),
                    dbc.NavLink("Project: DefiChain-Analytics", href="/community?entry=analytics", className="linkstyle", id="analytics"),
                    dbc.NavLink("Project: DefiChain-Income", href="/community?entry=income", className="linkstyle", id="income"),
                    dbc.NavLink("Project: Portfolio App", href="/community?entry=portfolio", className="linkstyle", id="portfolio"),
                    dbc.NavLink("Project: Masternode Monitor", href="/community?entry=mnmonitor", className="linkstyle", id="mnmonitor"),
                    dbc.NavLink("Project: DFI-Signal", href="/community?entry=dfisignal", className="linkstyle", id="dfisignal"),
                    dbc.NavLink("Project: Dobby", href="/community?entry=dobby", className="linkstyle", id="dobby"),
                    dbc.NavLink("Project: LOCK", href="/community?entry=lock", className="linkstyle", id="lock")
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
                    dbc.NavLink("Donation", href="/about?entry=donate", className="linkstyle", id="donate"),
                    dbc.NavLink("Imprint", href="/about?entry=imprint", className="linkstyle", id="imprint")
                ],
                id="submenu-about-collapse"
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

                dbc.Col([html.A(html.Div(id='idLogoSidebar'), href='https://www.defichain-analytics.com/', className='defiLink'),
                         dbc.NavLink(id='idVersion',href="/about?entry=changelog", className='defiLink')]),

                dbc.Col(),
            ],
            id="header",
            className="headerStyle",
        )

        sidebar_footer = dbc.Row([dbc.NavLink(html.Div(id='idLogoDonate'), href='/about?entry=donate')], justify="center", align="center", style={'margin-top': '40px'})

        refLink = html.Div()
            # html.Div(html.Marquee([
            #           'You want to support me? You want to get 5 DFI? Sign up (after 17th April 2022) with my ',
            #           html.A('Ref-Link', href='https://bake.io/?ref=476728', target='_blank', className='defiLink'),
            #           ' on CakeDefi and get $30 sign-up bonus in DFI after fullfilling Cakes requirements. If you are a ',
            #           html.A('Referral', href='https://bake.io/?ref=476728', target='_blank', className='defiLink'),
            #           ' of me (sign-up after 17th April 2022), I give you additional 5 DFI after you and me got the sign-up bonus. Reveal your information, send me your name, screenshot of sign-up bonus transaction and a DFI deposit address. ',
            #           html.A('Cake', href='https://bake.io/?ref=476728', target='_blank', className='defiLink'),
            #           ' is also gateway for your BTC, ETH and USDT to the DeFiChain-Wallet.']), className='refLinkMarquee')

        sidebar = html.Div(
            [
                sidebar_header,

                dbc.Collapse([html.Div(dbc.Nav(submenu_general + submenu_blockchain + submenu_dex + submenu_liquidityMining + submenu_vaultsLoans + submenu_bscBridge +
                                               submenu_token + submenu_community + submenu_about,
                              vertical=True, id='navbar-container'), className="scrollbar_sidemenu"),
                             sidebar_footer],
                    id="menuResponsiveCollapse", className="menu_collapse"),
            ],
            className="sidebarstyle",
            id="sidebar",
        )

        MainWindow = dcc.Loading([html.Div(id="page-content", className="contentstyle"),
                                  refLink,
                                  html.Div(id='hiddenDivTimestampsMenuClicked', children='0 0 0 0 0 0 0 0 0', style={'display':'none'})],
                                 type="default")
        self.trackVisit()
        self.layout = html.Div([dcc.Location(id="url"), sidebar, MainWindow])

        return self.layout