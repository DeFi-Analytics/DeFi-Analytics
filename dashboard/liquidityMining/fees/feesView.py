import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class feesViewClass:

    def getFeesContent(self, data):
        content = [dbc.Modal([dbc.ModalHeader("Info DEX Trading Fees"),
                              dbc.ModalBody(self.getFeesExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoFees", className="ml-auto"))], id="modalFees", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Trading fees from DEX']),
                                          html.Table([html.Tr([html.Td('Select representation style for fee graphic: '),
                                          html.Td(dcc.Dropdown(id='feeRepresentation', options=[{'label': 'stacked area curves', 'value': 'stacked'},
                                                                                                {'label': 'individual line curves', 'value': 'individual'}],
                                                               value='stacked', clearable=False, style=dict(width='200px', verticalAlign="bottom")))])]),
                                          dcc.Graph(id='lmPaidFees', config={'displayModeBar': False}),
                                          html.Table([html.Tr([html.Td('Select pool for showing paid fees as native token: '),
                                                               html.Td(dcc.Dropdown(id='feeNativeCoin', options=[{'label': 'BTC', 'value': 'BTC'},
                                                                                                                 {'label': 'ETH', 'value': 'ETH'},
                                                                                                                 {'label': 'USDT', 'value': 'USDT'},
                                                                                                                 {'label': 'LTC', 'value': 'LTC'},
                                                                                                                 {'label': 'DOGE', 'value': 'DOGE'},
                                                                                                                 {'label': 'BCH', 'value': 'BCH'}],
                                                                                    value='BTC', clearable=False, style=dict(width='200px', verticalAlign="bottom")))])]),
                                          dcc.Graph(id='lmPaidCoinFees', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoFees")))]))]
        return content

    @staticmethod
    def createFeesGraph(data, representationStyle, bgImage):
        # Plotting paid Fees in USD
        figFee = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=(['Paid trading Fees']))
        figFee.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figFee.layout.annotations[0].font.size = 20
        figFee.layout.annotations[0].update(y=1.075)
        hoverTemplateRepresenation = '$%{y:,.0f}'

        # single TVL graphs
        trace_feeBTC = dict(type='scatter', name='BTC',
                            x=data.BTCpool_sum_inUSD.dropna().index, y=data.BTCpool_sum_inUSD.dropna() * 0.002,
                            mode='lines', line=dict(color='#da3832'), hovertemplate=hoverTemplateRepresenation)
        trace_feeETH = dict(type='scatter', name='ETH',
                            x=data.ETHpool_sum_inUSD.dropna().index, y=data.ETHpool_sum_inUSD.dropna() * 0.002,
                            mode='lines', line=dict(color='#617dea'), hovertemplate=hoverTemplateRepresenation)
        trace_feeUSDT = dict(type='scatter', name='USDT',
                             x=data.USDTpool_sum_inUSD.dropna().index, y=data.USDTpool_sum_inUSD.dropna() * 0.002,
                             mode='lines', line=dict(color='#22b852'), hovertemplate=hoverTemplateRepresenation)
        trace_feeDOGE = dict(type='scatter', name='DOGE',
                             x=data.DOGEpool_sum_inUSD.dropna().index, y=data.DOGEpool_sum_inUSD.dropna() * 0.002,
                             mode='lines', line=dict(color='#c2a634'), hovertemplate=hoverTemplateRepresenation)
        trace_feeLTC = dict(type='scatter', name='LTC',
                            x=data.LTCpool_sum_inUSD.dropna().index, y=data.LTCpool_sum_inUSD.dropna() * 0.002,
                            mode='lines', line=dict(color='#ff2ebe'), hovertemplate=hoverTemplateRepresenation)
        trace_feeBCH = dict(type='scatter', name='BCH',
                            x=data.BCHpool_sum_inUSD.dropna().index, y=data.BCHpool_sum_inUSD.dropna() * 0.002,
                            mode='lines', line=dict(color='#410eb2'), hovertemplate=hoverTemplateRepresenation)

        if representationStyle == 'stacked':
            trace_feeBTC.update(dict(fill='tozeroy', stackgroup='one', line_width=0))
            trace_feeETH.update(dict(fill='tonexty', stackgroup='one', line_width=0))
            trace_feeUSDT.update(dict(fill='tonexty', stackgroup='one', line_width=0))
            trace_feeDOGE.update(dict(fill='tonexty', stackgroup='one', line_width=0))
            trace_feeLTC.update(dict(fill='tonexty', stackgroup='one', line_width=0))
            trace_feeBCH.update(dict(fill='tonexty', stackgroup='one', line_width=0))
        else:
            trace_feeBTC.update(dict(line_width=2))
            trace_feeETH.update(dict(line_width=2))
            trace_feeUSDT.update(dict(line_width=2))
            trace_feeDOGE.update(dict(line_width=2))
            trace_feeLTC.update(dict(line_width=2))
            trace_feeBCH.update(dict(line_width=2))

            # overall TVL graph
        trace_feeOverall = dict(type='scatter', name='Overall', x=data[
                                      ['BTCpool_sum_inUSD', 'ETHpool_sum_inUSD', 'USDTpool_sum_inUSD',
                                       'DOGEpool_sum_inUSD', 'LTCpool_sum_inUSD', 'BCHpool_sum_inUSD']].dropna(how='all').index,
                                y=data[
                                      ['BTCpool_sum_inUSD', 'ETHpool_sum_inUSD', 'USDTpool_sum_inUSD',
                                       'DOGEpool_sum_inUSD', 'LTCpool_sum_inUSD', 'BCHpool_sum_inUSD']].dropna(how='all').sum(axis=1) * 0.002,
                                mode='lines', line=dict(color='#410eb2'), line_width=3,
                                hovertemplate=hoverTemplateRepresenation)

        figFee.add_trace(trace_feeBTC, 1, 1)
        figFee.add_trace(trace_feeETH, 1, 1)
        figFee.add_trace(trace_feeUSDT, 1, 1)
        figFee.add_trace(trace_feeDOGE, 1, 1)
        figFee.add_trace(trace_feeLTC, 1, 1)
        figFee.add_trace(trace_feeBCH, 1, 1)

        if representationStyle == 'stacked':
            figFee.add_trace(trace_feeOverall, 1, 1)

        figFee.update_yaxes(title_text='Fees in USD', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figFee.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)

        # Add range slider
        figFee.update_layout(xaxis=dict(
            rangeselector=dict(
                buttons=list([dict(count=14, label="14d", step="day", stepmode="backward"),
                              dict(count=30, label="30d", step="day", stepmode="backward"),
                              dict(count=2, label="2m", step="month", stepmode="backward"),
                              dict(count=6, label="6m", step="month", stepmode="backward"),
                              dict(count=1, label="YTD", step="year", stepmode="todate"),
                              dict(count=1, label="1y", step="year", stepmode="backward"),
                              dict(step="all")])),
            rangeslider=dict(visible=False),type="date"))

        # add background picture
        figFee.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.5, sizey=0.5,  xanchor="center", yanchor="middle", opacity=0.2))

        figFee.update_layout(height=600,
                             margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                         yanchor="top",
                                         y=-0.12,
                                         xanchor="right",
                                         x=1),
                             )
        figFee.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figFee.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figFee.layout.legend.font.color = '#6c757d'  # font color legend

        return figFee

    @staticmethod
    def createFeesCoinFigure(data, selectedCoin, bgImage):
        figFeeCoins = make_subplots(
            rows=2, cols=1,
            vertical_spacing=0.15,
            row_width=[0.5, 0.5],  # from bottom to top
            specs=[[{}],
                   [{}]],
            shared_xaxes=True,
            subplot_titles=(['Paid DFI fees', 'Paid ' + selectedCoin + ' fees']))
        figFeeCoins.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figFeeCoins.layout.annotations[0].font.size = 20
        figFeeCoins.layout.annotations[1].font.color = '#6c757d'
        figFeeCoins.layout.annotations[1].font.size = 20

        # choosing color for fees in native coins
        if selectedCoin == 'BTC':
            coinColor = '#da3832'
        elif selectedCoin == 'ETH':
            coinColor = '#617dea'
        elif selectedCoin == 'USDT':
            coinColor = '#22b852'
        elif selectedCoin == 'DOGE':
            coinColor = '#c2a634'
        elif selectedCoin == 'LTC':
            coinColor = '#ff2ebe'
        elif selectedCoin == 'BCH':
            coinColor = '#410eb2'

        trace_DFIFee = dict(type='scatter', name='DFI', x=data[selectedCoin + 'pool_baseDFI'].dropna().index,
                            y=data[selectedCoin + 'pool_baseDFI'].dropna() * 0.002,
                            mode='lines', line=dict(color=coinColor, dash='dot'), line_width=2,
                            hovertemplate='%{y:,.4f} DFI')
        trace_coinFee = dict(type='scatter', name=selectedCoin, x=data[selectedCoin + 'pool_base' + selectedCoin].dropna().index,
                             y=data[selectedCoin + 'pool_base' + selectedCoin].dropna() * 0.002,
                             mode='lines', line=dict(color=coinColor, dash='dash'), line_width=2,
                             hovertemplate='%{y:,.4f} ' + selectedCoin)

        figFeeCoins.add_trace(trace_DFIFee, 1, 1)
        figFeeCoins.add_trace(trace_coinFee, 2, 1)

        figFeeCoins.update_yaxes(title_text='DFI-Fees', gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                                 row=1, col=1)
        figFeeCoins.update_yaxes(title_text=selectedCoin + '-Fees', gridcolor='#6c757d', color='#6c757d',
                                 zerolinecolor='#6c757d', row=2, col=1)
        figFeeCoins.update_xaxes(gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figFeeCoins.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                                 row=2, col=1)

        # add background picture
        figFeeCoins.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.78, sizex=0.4, sizey=0.4,  xanchor="center", yanchor="middle", opacity=0.2))
        figFeeCoins.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.22, sizex=0.4, sizey=0.4,  xanchor="center", yanchor="middle", opacity=0.2))

        figFeeCoins.update_layout(height=680,
                                  margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                                  hovermode='x unified',
                                  hoverlabel=dict(font_color="#6c757d"),
                                  legend=dict(orientation="h",
                                              yanchor="top",
                                              y=-0.12,
                                              xanchor="right",
                                              x=1),
                                  )
        figFeeCoins.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figFeeCoins.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figFeeCoins.layout.legend.font.color = '#6c757d'  # font color legend

        return figFeeCoins

    def getFeesExplanation(self):
        feeCardExplanation = [html.P(['For every coinswap on DefiChain-DEX the user have to pay a fee of 0.2% for the coins given into the pool to the liquidity providers.'],
                                     style={'text-align': 'justify'}),
                              html.P(['In this evaluation every trade is analyzed regarding the Coin given into the DEX. This can be done via a DEX API (',
                                         html.A('API-Link last 20 Trades BTC-Pool', href='https://api.defichain.io/v1/getswaptransaction?id=5&network=mainnet&skip=0&limit=20', target='_blank', className='defiLink'),
                                         '). For these coins the fee part is calculated and converted to the USD-value.'],
                                     style={'text-align': 'justify'}),
                              html.P(['The summation of all single fees per pool and day gives the graphs on the right side. You can choose between a stacked and an individual curve representation. '],
                                     style={'text-align': 'justify'}),
                              html.P([html.B('Hint:'),
                                      ' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                      ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                     style={'text-align': 'justify', 'fontSize': '0.7rem', 'color': '#6c757d'})
                              ]
        return feeCardExplanation