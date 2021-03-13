import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class liquidityTokenViewClass:

    def getLiquidityTokenContent(self, data):
        content = [dbc.Modal([dbc.ModalHeader("Info Liquidity Token (LT)"),
                              dbc.ModalBody(self.getLTExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoLT", className="ml-auto"))], id="modalLT", size='xl'),
                   dbc.Card(dbc.CardBody([html.Table([html.Tr([html.Td('Select pool for plotting liquidity token data:'),
                                           html.Td(dcc.Dropdown(id='LTSelection',options=[
                                            {'label':'BTC','value':'BTC'},
                                            {'label':'ETH','value':'ETH'},
                                            {'label':'USDT','value':'USDT'},
                                            {'label':'DOGE','value':'DOGE'},
                                            {'label':'LTC','value':'LTC'},
                                            {'label':'BCH','value':'BCH'}],
                                            value='BTC', style=dict(width='200px',verticalAlign="bottom")))])]),
                            dbc.Col(dcc.Graph(id = 'liquidityTokenGraph', config={'displayModeBar': False})),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoLT")))]))]
        return content

    @staticmethod
    def createLiquidityTokenGraph(data, selectedCoin):
        figLiquidityToken = make_subplots(
            rows=3, cols=1,
            vertical_spacing=0.15,
            row_width=[0.4, 0.2, 0.4],  # from bottom to top
            specs=[[{}],
                   [{}],
                   [{}]],
            shared_xaxes=True,
            subplot_titles=(['Liquidity Token', 'Daily change in Liquidity Token', 'Addresses holding Liquidity Token']))
        figLiquidityToken.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figLiquidityToken.layout.annotations[0].font.size = 20
        figLiquidityToken.layout.annotations[1].font.color = '#6c757d'
        figLiquidityToken.layout.annotations[1].font.size = 20
        figLiquidityToken.layout.annotations[2].font.color = '#6c757d'
        figLiquidityToken.layout.annotations[2].font.size = 20
        # absolute price
        if selectedCoin == 'USDT':
            lineColor = '#22b852'
        elif selectedCoin == 'ETH':
            lineColor = '#617dea'
        elif selectedCoin == 'DOGE':
            lineColor = '#c2a634'
        elif selectedCoin == 'LTC':
            lineColor = '#ff2ebe'
        elif selectedCoin == 'BCH':
            lineColor = '#410eb2'
        else:
            lineColor = '#da3832'

        trace_LiquidityToken = dict(type='scatter', name='Liquidity Token', x=data[selectedCoin + '-DFI_totalLiquidity'].index,
                                    y=data[selectedCoin + '-DFI_totalLiquidity'],
                                    mode='lines', line=dict(color=lineColor), line_width=2, hovertemplate='%{y:,.1f} ' + selectedCoin + '-DFI')
        trace_dailyChange = dict(type='scatter', name='Absolute Daily Change',
                                 x=data.groupby('Date')[selectedCoin + '-DFI_totalLiquidity'].first().diff().index,
                                 y=data.groupby('Date')[selectedCoin + '-DFI_totalLiquidity'].first().diff(),
                                 mode='lines', line=dict(color=lineColor, dash='dash'), line_width=2, hovertemplate='%{y:,.1f} ' + selectedCoin + '-DFI')
        trace_nbAddresses = dict(type='scatter', name='Number Addresses', x=data[selectedCoin + '-DFI_numberAddresses'].dropna().index,
                                 y=data[selectedCoin + '-DFI_numberAddresses'].dropna(),
                                 mode='lines', line=dict(color=lineColor, dash='dot'), line_width=2, hovertemplate='%{y:,.0f}')

        figLiquidityToken.add_trace(trace_LiquidityToken, 1, 1)
        figLiquidityToken.add_trace(trace_dailyChange, 2, 1)
        figLiquidityToken.add_trace(trace_nbAddresses, 3, 1)

        figLiquidityToken.update_yaxes(title_text='Liquidity Token ' + selectedCoin + '-DFI', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                                       zerolinecolor='#6c757d', row=1, col=1)
        figLiquidityToken.update_yaxes(title_text='Absolute change of ' + selectedCoin + '-DFI', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                                       zerolinecolor='#6c757d', row=2, col=1)
        figLiquidityToken.update_yaxes(title_text='Number', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                                       zerolinecolor='#6c757d', row=3, col=1)

        figLiquidityToken.update_xaxes(gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figLiquidityToken.update_xaxes(gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=2, col=1)
        figLiquidityToken.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=3, col=1)

        figLiquidityToken.update_layout(height=765,
                                        margin={"t": 40, "l": 120, "b": 20, "r": 20},
                                        hovermode='x unified',
                                        hoverlabel=dict(font_color="#6c757d",
                                                        bgcolor='#ffffff', ),
                                        showlegend=False,
                                        legend=dict(orientation="h",
                                                    yanchor="bottom",
                                                    y=-0.15,
                                                    xanchor="right",
                                                    x=1),
                                        )
        figLiquidityToken.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figLiquidityToken.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figLiquidityToken.layout.legend.font.color = '#6c757d'  # font color legend

        return figLiquidityToken

    @staticmethod
    def getLTExplanation():
        liquidityTokenExplanation = [html.P(['As a liquidity provider you are getting liquidity token, which can be seen in the wallet. These tokens are your part of the corresponding pool. ',
                                       'Removing liquidity will swap these tokens back to the original pool pair tokens. More information regarding LT can be found on ',
                                       html.A('Reddit',href='https://www.reddit.com/r/defiblockchain/comments/kfm6zw/liquidity_token_in_a_nutshell/',target='_blank'),'.'],style={'text-align': 'justify'}),
                               html.P(['While the TVL also depends on the current price, the number of liquidity token (first graph) represents the actual pool size. ',
                                       ' The ratio of your LT to the total number defines the reward part you are getting.'],style={'text-align': 'justify'}),
                               html.P(['Changing the number of liquidity token is only possible by adding or removing liquidity to the pool. The second graph calculates the '
                                       'daily change of the liquidity tokens. The mean value of the LT number per day is used for this purpose. ',
                                       'A positive change represents an increase of the pool, so overall more liquidity was added then removed. If the value is negative the pool size was decreased.'],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return liquidityTokenExplanation