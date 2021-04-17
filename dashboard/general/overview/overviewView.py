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
            # html.H4(['Countdown 1st ',html.I('"Halving"')]),
            html.H4(['Countdown ', html.I('Reduction of Liquidity Mining rewards')]),
            html.Table([
                html.Tr(html.Td(html.Br())),
                html.Tr([html.Td('Blocks left:'),
                         html.Td(id='dfiCountdownBlocks', style={'color': '#ff00af', 'padding-left': '10px'})]),
                html.Tr(
                    [html.Td('Estimated duration:'),
                     html.Td(id='dfiCountdownDuration', style={'color': '#ff00af', 'padding-left': '10px'})]),
                html.Tr(
                    [html.Td('Estimated time (UTC):'),
                     html.Td(id='dfiCountdownTime', style={'color': '#ff00af', 'padding-left': '10px'})])]),
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
                html.Tr([html.Td('ERC20 Collateral'),
                         html.Td("{:,.0f} DFI".format(data['erc20DFI'].values[0]))]),

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
                    html.A('http://explorer.defichain.io/#/DFI/mainnet/rich-list', href='http://explorer.defichain.io/#/DFI/mainnet/rich-list', target='_blank', className='defiLink'), html.Br(),
                    html.A('https://www.coingecko.com/en/coins/defichain', href='https://www.coingecko.com/en/coins/defichain', target='_blank', className='defiLink')
                    ], style={'fontSize': '0.65rem', 'padding-top': '20px'})]
        return htmlContent

    @staticmethod
    def createPieChartDFI(data,  bgImage):
        figDFIPie = go.Figure()

        labelList = ['Masternodes', 'Community fund', 'Foundation', 'Other', 'Liquidity Pool', 'DFI token', 'ERC20 Collateral']
        valueList = [data['mnDFI'].values[0], data['fundDFI'].values[0], data['foundationDFI'].values[0], data['otherDFI'].values[0], data['lmDFI'].values[0], data['tokenDFI'].values[0], data['erc20DFI'].values[0]]
        colorList = ['#da3832', '#ff9800', '#22b852', '#410eb2', '#ff2ebe', '#00fffb','#808000']
        trace_pieDFI = dict(type='pie', name='', labels=labelList, values=valueList, marker=dict(colors=colorList), opacity=1,
                            textposition='inside', textfont_size=16, hovertemplate='%{label}: <br> %{value:,.0f}')
        figDFIPie.add_trace(trace_pieDFI)

        figDFIPie.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.75, sizey=0.75,  xanchor="center", yanchor="middle", opacity=0.25))

        figDFIPie.update_layout(height=630,
                                margin={"t": 40, "l": 20, "b": 20},
                                hovermode='x unified',
                                # hoverlabel=dict( font_color="#aaaaaa"),
                                legend=dict(yanchor="top",
                                            y=0.5,
                                            xanchor="left",
                                            x=1.1),
                                )
        figDFIPie.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDFIPie.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDFIPie.layout.legend.font.color = '#6c757d'  # font color legend

        dfiGraph = [html.H4('DFI distribution'), dcc.Graph(figure=figDFIPie, config={'displayModeBar': False})]
        return dfiGraph

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
                               ' DFI amount.', html.Br(),
                            'For identification of the masternodes the listmasternodes() command is used, which is provided by API of Bernd Mack. ',
                            html.Br(),
                            html.A('http://defichain-node.de/api/v1/listmasternodes/?state=ENABLED', href='http://defichain-node.de/api/v1/listmasternodes/?state=ENABLED', target='_blank', className='defiLink')],
                               style={'text-align': 'justify'}),
                        html.P([html.B('Hint:'),' The presented diagrams are interactive.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})]

        return overviewCardExplanation

