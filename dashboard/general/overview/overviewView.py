import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
from plotly.subplots import make_subplots


class overviewViewClass:

    def getOverviewContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info Overview"),
                              dbc.ModalBody(self.getOverviewExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoTwitter", className="ml-auto"))], id="modalTwitter", size='xl'),
                   dbc.Card(dbc.CardBody([dbc.Row([ dbc.Col(self.createStatisticsDFI(data), lg=4, xl=4, align='start'),
                                      dbc.Col(None, lg=8, xl=8)], no_gutters=True), #self.createPieChartDFI()
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoTwitter")))]))]
        return content

    @staticmethod
    def createStatisticsDFI(data):
        htmlContent = [
            # html.H4(['Countdown 1st ',html.I('"Halving"')]),
            html.H4(['Countdown ', html.I('Reduction of Liquidity Mining rewards')]),
            html.Table([
                html.Tr(html.Td(html.Br())),
                html.Tr([html.Td('Blocks left:'),
                         html.Td(id='dfiCountdownBlocks', style={'color': '#5c0fff', 'padding-left': '10px'})]),
                html.Tr(
                    [html.Td('Estimated duration:'),
                     html.Td(id='dfiCountdownDuration', style={'color': '#5c0fff', 'padding-left': '10px'})]),
                html.Tr(
                    [html.Td('Estimated time (UTC):'),
                     html.Td(id='dfiCountdownTime', style={'color': '#5c0fff', 'padding-left': '10px'})])]),
            html.Br(),
            html.H4('DFI statistics'),
            html.Table([
                html.Tr(html.Td(html.Br())),
                html.Tr([html.Td('Price'),
                         html.Td("${:,.4f}".format(data['DFIprice'].values[0]))]),
                html.Tr(
                    [html.Td('24h-volume'),
                     html.Td("${:,.0f}".format(data['tradingVolume'].values[0]))]),

                html.Tr(html.Td(html.Br())),
                html.Tr(
                    [html.Td('Community Fund'),
                     html.Td("{:,.0f} DFI".format(data['fundDFI'].values[0]))]),
                html.Tr([html.Td('Other addresses'),
                         html.Td("{:,.0f} DFI".format(data['otherDFI'].values[0]))]),
                html.Tr([html.Td('Masternodes'),
                         html.Td("{:,.0f} DFI".format(data['mnDFI'].values[0]))]),
                html.Tr([html.Td('Foundation'),
                         html.Td("{:,.0f} DFI".format(data['foundationDFI'].values[0]))]),
                html.Tr([html.Td('Liquidity Pool'),
                         html.Td("{:,.0f} DFI".format(data['lmDFI'].values[0]))]),
                html.Tr([html.Td('DFI Token'),
                         html.Td("{:,.0f} DFI".format(data['tokenDFI'].values[0]))]),

                html.Tr(html.Td(html.Br())),
                html.Tr(
                    [html.Td('Circulating supply'),
                     html.Td("{:,.0f} DFI".format(data['circDFI'].values[0]))]),
                html.Tr(
                    [html.Td('Total supply'),
                     html.Td("{:,.0f} DFI".format(data['totalDFI'].values[0]))]),
                html.Tr(
                    [html.Td('Max supply'),
                     html.Td("{:,.0f} DFI".format(data['maxDFI'].values[0]))]),

                html.Tr(html.Td(html.Br())),
                html.Tr(
                    [html.Td('Market-Cap'),
                     html.Td("${:,.0f}".format(data['marketCap'].values[0]))]),
                html.Tr(
                    [html.Td('corresponding rank'),
                     html.Td("{:,.0f}".format(data['marketCapRank'].values[0]))]),
                html.Tr(html.Td(html.Br())),

            ]),
            html.P(['MN: Masternodes', html.Br(),
                    'Defichain Richlist and Coingecko: last update ', pd.to_datetime(data['date'].values[0]).strftime("%Y-%m-%d %H:%M"), html.Br(),
                    html.A('http://explorer.defichain.io/#/DFI/mainnet/rich-list', href='http://explorer.defichain.io/#/DFI/mainnet/rich-list', target='_blank'), html.Br(),
                    html.A('https://www.coingecko.com/en/coins/defichain', href='https://www.coingecko.com/en/coins/defichain', target='_blank')
                    ], style={'fontSize': '0.65rem', 'padding-top': '20px'})]
        return htmlContent


    @staticmethod
    def getOverviewExplanation():
        overviewCardExplanation = [
                       html.P(['Here a countdown to an important DefiChain event and some basic statistics are shown. Different sources are used to retrieve this data:',
                               html.Ul([html.Li('DefiChain Block-API'),
                                        html.Li('DefiChain block statistics (see tab Block Time)'),
                                        html.Li('Coingecko-API'),
                                        html.Li('DefiChain Richlist-API')])],
                               style={'text-align': 'justify'}),
                        html.P(['The countdown is calculated by using the mean block time over the last 10 days, the current block from DefiChain-API and the defined goal block ',
                                'of the event.']),
                        html.P(['Both the Community Fund and the DefiChain Foundation have a unique address, which is used to determine the corresponding'
                               ' DFI amount.',html.Br(),
                               'For getting the masternode addresses currently the amount of deposited DFI is used, which must be in a'
                               ' range of 1 to 1.1 million DFI.']),
                        html.P([html.B('Hint:'),' The presented diagrams are interactive.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})]

        return overviewCardExplanation

