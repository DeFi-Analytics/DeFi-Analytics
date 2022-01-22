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
                    #dbc.NavLink("Coins locked", href="/liquidityMining?entry=coinsLocked", className="linkstyle", id="coinsLocked"),
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
                    dbc.NavLink("Number dToken", href="/vaultsLoans?entry=nbDToken", className="linkstyle", id="nbDToken"),
                    dbc.NavLink("Open Interest", href="/vaultsLoans?entry=interest", className="linkstyle", id="interest"),
                    dbc.NavLink("DFI Burn", href="/vaultsLoans?entry=burnedDFI", className="linkstyle", id="burnedDFI"),
                    dbc.NavLink("Loan schemes", href="/vaultsLoans?entry=scheme", className="linkstyle", id="scheme"),
                ],
                id="submenu-vaultsLoans-collapse",
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
                    dbc.NavLink("Project: DefiChain-Analytics", href="/community?entry=analytics", className="linkstyle", id="analytics"),
                    dbc.NavLink("Project: DefiChain-Income", href="/community?entry=income", className="linkstyle", id="income"),
                    dbc.NavLink("Project: Portfolio App", href="/community?entry=portfolio", className="linkstyle", id="portfolio"),
                    dbc.NavLink("Project: Defichain-Promo", href="/community?entry=promo", className="linkstyle", id="promo"),
                    dbc.NavLink("Project: Masternode Monitor", href="/community?entry=mnmonitor", className="linkstyle", id="mnmonitor"),
                    dbc.NavLink("Project: DFX", href="/community?entry=dfx", className="linkstyle", id="dfx"),
                    dbc.NavLink("Project: DFI-Signal", href="/community?entry=dfisignal", className="linkstyle", id="dfisignal"),
                    dbc.NavLink("Project: Dobby", href="/community?entry=dobby", className="linkstyle", id="dobby")
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
                    dbc.NavLink("CakeDefi-Review", href="/about?entry=cakereview", className="linkstyle", id="cakereview"),
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

        refLink = html.Div(html.Marquee([
                      'You want to stake DFI, but don\'t have the needed 20,000 DFI as a collateral? Then try out the Staking-Service of ',
                      html.A('Cake', href='https://app.cakedefi.com/?ref=476728', target='_blank', className='defiLink'),
                      '. With the auto-invest functionality of the rewards you can reach >30% APY. Current special ',
                      html.A('Cake', href='https://app.cakedefi.com/?ref=476728', target='_blank', className='defiLink'),
                      ' offer: Sign-up Bonus of $20 in DFI (after deposit of $50). You and me get $10 additional in DFI if you use my ',
                      html.A('Ref-Link', href='https://app.cakedefi.com/?ref=476728', target='_blank', className='defiLink'),
                      '. Cake is also gateway for your BTC, ETH and USDT to the DeFiChain-Wallet. ',
                      html.A('Offer', href='https://app.cakedefi.com/?ref=476728', target='_blank', className='defiLink'),
                      ' Condition: DFI are staking for at least 180 days and generate revenue of >30% APY.']), className='refLinkMarquee')

        sidebar = html.Div(
            [
                sidebar_header,

                dbc.Collapse([html.Div(dbc.Nav(submenu_general + submenu_blockchain + submenu_dex + submenu_liquidityMining + submenu_vaultsLoans + submenu_token
                                               + submenu_community + submenu_about,
                              vertical=True, id='navbar-container'), className="scrollbar_sidemenu"),
                             sidebar_footer],
                    id="menuResponsiveCollapse", className="menu_collapse"),
            ],
            className="sidebarstyle",
            id="sidebar",
        )

        MainWindow = dcc.Loading([html.Div(id="page-content", className="contentstyle"),
                                  refLink,
                                  html.Div(id='hiddenDivTimestampsMenuClicked', children='0 0 0 0 0 0 0 0', style={'display':'none'})],
                                 type="default")
        self.trackVisit()
        self.layout = html.Div([dcc.Location(id="url"), sidebar, MainWindow])

        return self.layout