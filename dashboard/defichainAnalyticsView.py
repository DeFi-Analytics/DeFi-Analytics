import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import os
import base64

class defichainAnalyticsViewClass:
    def __init__(self):
        # the style arguments for the sidebar. We use position:fixed and a fixed width
        SIDEBAR_STYLE = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            "background-color": "#cecfcf",
        }

        # the styles for the main content position it to the right of the sidebar and
        # add some padding.
        CONTENT_STYLE = {
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",
        }

        submenu_blockchain = [
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        dbc.Col("Blockchain"),
                        dbc.Col(
                            html.I(className="fas fa-chevron-right mr-3"), width="auto"
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
                    dbc.NavLink("Addresses", href="/blockchain?entry=addresses"),
                    dbc.NavLink("DAA", href="/blockchain?entry=daa"),
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
                            html.I(className="fas fa-chevron-right mr-3"), width="auto"
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
                    dbc.NavLink("Fees", href="/liquidityMining?entry=fees")
                ],
                id="submenu-liquidityMining-collapse",
            ),
        ]

        submenu_2 = [
            html.Li(
                dbc.Row(
                    [
                        dbc.Col("Menu 2"),
                        dbc.Col(
                            html.I(className="fas fa-chevron-right mr-3"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                style={"cursor": "pointer"},
                id="submenu-2",
            ),
            dbc.Collapse(
                [
                    dbc.NavLink("Page 2.1", href="/page-2/1"),
                    dbc.NavLink("Page 2.2", href="/page-2/2"),
                ],
                id="submenu-2-collapse",
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
                dbc.Nav(submenu_blockchain + submenu_liquidityMining + submenu_2, vertical=True, ),
            ],
            style=SIDEBAR_STYLE,
            id="sidebar",
        )

        MainWindow = dcc.Loading(html.Div(id="page-content", style=CONTENT_STYLE), type="default")
        self.layout = html.Div([dcc.Location(id="url"), sidebar, MainWindow])
