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
                style={"cursor": "pointer"},
                id="submenu-blockchain",
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                [
                    dbc.NavLink("Addresses", href="/blockchain?entry=addresses", className="linkstyle"),
                    dbc.NavLink("DAA", href="/blockchain?entry=daa", className="linkstyle"),
                ],
                id="submenu-blockchain-collapse",
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
                style={"cursor": "pointer"},
                id="submenu-liquidityMining",
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                [
                    dbc.NavLink("Fees", href="/liquidityMining?entry=fees", className="linkstyle")
                ],
                id="submenu-liquidityMining-collapse",
            ),
        ]


        workDir = os.path.abspath(os.getcwd())
        image_filename = workDir + '/assets/'+'logo-defi-analytics.png'
        encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')

        sidebar = html.Div(
            [
                html.A(html.Img(src='data:image/png;base64,{}'.format(encoded_image),
                         style={
                             'width': '14rem',
                             'padding-top': 20,
                             'padding-right': 0,
                             'padding-buttom': 0})),
                html.Hr(),
                dbc.Nav(submenu_blockchain + submenu_liquidityMining , vertical=True, ),
            ],
            className="sidebarstyle",
            id="sidebar",
        )

        MainWindow = dcc.Loading(html.Div(id="page-content", className="contentstyle"), type="default")
        self.layout = html.Div([dcc.Location(id="url"), sidebar, MainWindow])
