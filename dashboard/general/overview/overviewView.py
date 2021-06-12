import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go


class overviewViewClass:

    def getOverviewContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info Overview"),
                              dbc.ModalBody(self.getOverviewExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoOverview", className="ml-auto"))], id="modalOverview", size='xl'),
                   dbc.Card(dbc.CardBody([dbc.Row([dbc.Col(self.createStatisticsDFI(data), xl=4, align='start'),
                                                   dbc.Col(self.createPieChartDFI(data, bgImage), xl=8)], no_gutters=True),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoOverview")))])),
                   dcc.Interval(id='overviewUpdateCountdown', interval=60*1000, n_intervals=0)]
        return content

    @staticmethod
    def createStatisticsDFI(data):
        htmlContent = [
            html.H4('DFI statistics'),
            html.Table([
                html.Tr(html.Td(html.Br())),
                html.Tr([html.Td('Price'),
                         html.Td("${:,.4f}".format(data['DFIprice'].values[0]), style={'text-align': 'right'})]),
                html.Tr(
                    [html.Td('24h-volume'),
                     html.Td("${:,.0f}".format(data['tradingVolume'].values[0]), style={'text-align': 'right'})]),

                html.Tr(html.Td(html.Br())),
                html.Tr([html.Td('Other addresses'),
                         html.Td("{:,.0f} DFI".format(data['otherDFI'].values[0]), style={'text-align': 'right'})]),
                html.Tr([html.Td('Masternodes'),
                         html.Td("{:,.0f} DFI".format(data['mnDFI'].values[0]), style={'text-align': 'right'})]),
                html.Tr([html.Td('Liquidity Pool'),
                         html.Td("{:,.0f} DFI".format(data['lmDFI'].values[0]), style={'text-align': 'right'})]),
                html.Tr([html.Td('DFI Token'),
                         html.Td("{:,.0f} DFI".format(data['tokenDFI'].values[0]), style={'text-align': 'right'})]),
                html.Tr([html.Td('ERC20 Collateral'),
                         html.Td("{:,.0f} DFI".format(data['erc20DFI'].values[0]), style={'text-align': 'right'})]),
                html.Tr(
                    [html.Td('Circulating supply', style={'font-weight': 'bold'}),
                     html.Td("{:,.0f} DFI".format(data['circDFI'].values[0]), style={'text-align': 'right', 'font-weight': 'bold'})]),
                html.Tr(html.Td(html.Br())),

                html.Tr(
                    [html.Td('Community Fund'),
                     html.Td("{:,.0f} DFI".format(data['fundDFI'].values[0]), style={'text-align': 'right'})]),
                html.Tr([html.Td('Foundation'),
                         html.Td("{:,.0f} DFI".format(data['foundationDFI'].values[0]), style={'text-align': 'right'})]),
                html.Tr(
                    [html.Td('Burned DFI'),
                     html.Td("{:,.0f} DFI".format(data['burnedDFI'].values[0]), style={'text-align': 'right'})]),
                html.Tr(
                    [html.Td('Total supply', style={'font-weight': 'bold'}),
                     html.Td("{:,.0f} DFI".format(data['totalDFI'].values[0]), style={'text-align': 'right', 'font-weight': 'bold'})]),
                html.Tr(html.Td(html.Br())),

                html.Tr(
                    [html.Td('Max supply', style={'font-weight': 'bold'}),
                     html.Td("{:,.0f} DFI".format(data['maxDFI'].values[0]), style={'text-align': 'right', 'font-weight': 'bold'})]),

                html.Tr(html.Td(html.Br())),
                html.Tr(
                    [html.Td('Market-Cap'),
                     html.Td("${:,.0f}".format(data['marketCap'].values[0]), style={'text-align': 'right'})]),
                html.Tr(
                    [html.Td('corresponding rank'),
                     html.Td("{:,.0f}".format(data['marketCapRank'].values[0]), style={'text-align': 'right'})]),

            ]),
            html.P(['MN: Masternodes', html.Br(),
                    'Defichain Richlist and Coingecko: last update ', pd.to_datetime(data['date'].values[0]).strftime("%Y-%m-%d %H:%M"), html.Br(),
                    html.A('http://explorer.defichain.io/#/DFI/mainnet/rich-list', href='http://explorer.defichain.io/#/DFI/mainnet/rich-list', target='_blank', className='defiLink'), html.Br(),
                    html.A('https://www.coingecko.com/en/coins/defichain', href='https://www.coingecko.com/en/coins/defichain', target='_blank', className='defiLink')
                    ], style={'fontSize': '0.65rem', 'padding-top': '20px'})]
        return htmlContent

    @staticmethod
    def createPieChartDFI(data,  bgImage):
        figDFIPie = go.Figure()

        labelList = ['Masternodes', 'Community fund', 'Foundation', 'Other', 'Liquidity Pool', 'DFI token', 'ERC20 Collateral', 'Burned DFI']
        valueList = [data['mnDFI'].values[0], data['fundDFI'].values[0], data['foundationDFI'].values[0], data['otherDFI'].values[0], data['lmDFI'].values[0],
                     data['tokenDFI'].values[0], data['erc20DFI'].values[0], data['burnedDFI'].values[0]]
        colorList = ['#da3832', '#ff9800', '#22b852', '#410eb2', '#ff2ebe', '#00fffb', '#808000', '#5d5d5d']
        trace_pieDFI = dict(type='pie', name='', labels=labelList, values=valueList, marker=dict(colors=colorList), opacity=1,
                            textposition='inside', textfont_size=16, hovertemplate='%{label}: <br> %{value:,.0f}')
        figDFIPie.add_trace(trace_pieDFI)

        figDFIPie.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.75, sizey=0.75,  xanchor="center", yanchor="middle", opacity=0.25))

        figDFIPie.update_layout(margin={"t": 40, "l": 20, "b": 20, "r": 20},
                                hovermode='x unified',
                                # hoverlabel=dict( font_color="#aaaaaa"),
                                legend=dict(yanchor="top",
                                            y=-0.1,
                                            xanchor="center",
                                            x=0.5,
                                            orientation="h",),
                                )
        figDFIPie.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDFIPie.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDFIPie.layout.legend.font.color = '#6c757d'  # font color legend

        dfiGraph = [html.H4('DFI distribution'), dcc.Graph(figure=figDFIPie, config={'displayModeBar': False}, id='figurePieChartDFI')]
        return dfiGraph

    @staticmethod
    def getOverviewExplanation():
        overviewCardExplanation = [
                       html.P(['This overview page gives some information about DFI and the current distribution. Therefore several APIs are used:',
                               html.Ul([html.Li('DefiChain Richlist-API'),
                                        html.Li('Coingecko-API'),
                                        html.Li('DefiChain DEX-API'),
                                        html.Li('Masternode-API from Bernd')])],
                               style={'text-align': 'justify'}),
                        html.P(['Currently there are 4 addresses holding special categories of DFI:', html.Br(),
                                html.Ul([html.Li('Foundation coins: dJEbxbfufyPF14SC93yxiquECEfq4YSd9L'),
                                         html.Li('Community Fund: dZcHjYhKtEM88TtZLjp314H2xZjkztXtRc'),
                                         html.Li('Collateral for ERC20-Token: dZFYejknFdHMHNfHMNQAtwihzvq7DkzV49'),
                                         html.Li(['Burned coins/token:',
                                                          html.Ul([html.Li('Manual burned coins/token on address 8defichainBurnAddressXXXXXXXdRQkSm'),
                                                          html.Li(['Burned fees getting from command getburninfo on API ',html.A('http://api.mydeficha.in/v1/getburninfo/', href='http://api.mydeficha.in/v1/getburninfo/', target='_blank', className='defiLink')]),
                                                          html.Li(['Burned unused block rewards under listCommunities from API ',html.A('https://api.defichain.io/v1/stats?network=mainnet&pretty', href='https://api.defichain.io/v1/stats?network=mainnet&pretty', target='_blank', className='defiLink')])
                                                          ])])]),
                                'All these addresses are represented in the Richlist with their DFI holdings. For identification of the masternodes the listmasternodes() command is used, which is provided by API of Bernd Mack. ',
                            html.A('http://api.mydeficha.in/v1/listmasternodes/?state=ENABLED', href='http://api.mydeficha.in/v1/listmasternodes/?state=ENABLED', target='_blank', className='defiLink')],
                               style={'text-align': 'justify'}),
                        html.P([html.B('Hint:'),' The presented diagrams are interactive.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})]

        return overviewCardExplanation

