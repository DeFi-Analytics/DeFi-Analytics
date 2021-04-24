import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import dateutil.relativedelta

class incomeViewClass:

    def getIncomeContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info DefiChain Income"),
                              dbc.ModalBody(),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoMN", className="ml-auto"))], id="modalMN", size='xl'),

                   dbc.Card(dbc.CardBody([html.H4(['DefiChain Income']),
                                          dbc.Card(dbc.CardBody([dbc.Row([dbc.Col(self.getIncomeInfos(), xl=4, align='start'),
                                                                          dbc.Col(dcc.Graph(id='figureIncomeUsers', config={'displayModeBar': False}), xl=8)], no_gutters=True),
                                                                 dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoOverview")))]))]))]
        return content


    @staticmethod
    def getIncomeInfos():
        content = [
            html.P(['The Website DefiChain-Income was set up to calculate and track your revenues from defichain. It started with calculating your liquidity mining rewards '
                       'based on your holdings of liquidity token or just simpler by giving your DFI address holding the token. All information is get via API from DefiChain.', html.Br(),
                    'Beside the absolute number representation the relative parts could be more of interest. They could be interpreted as a measure of decentralization.'], style={'text-align': 'justify'}),]
        return content
