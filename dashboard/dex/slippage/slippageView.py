import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
import numpy as np


class slippageViewClass:
    def getSlippageContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info slippage DEX"),
                              dbc.ModalBody(self.getSlippageExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoSlippage", className="ml-auto"))], id="modalSlippage", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Slippage for DEX swaps']),
                                          html.Table([html.Tr([html.Td('Select pool for your swap:'),
                                                               html.Td(dcc.Dropdown(id='slippagePoolSelection', options=[{'label': 'BTC', 'value': 'BTC'},
                                                                                              {'label': 'ETH', 'value': 'ETH'},
                                                                                              {'label': 'USDT', 'value': 'USDT'},
                                                                                              {'label': 'DOGE', 'value': 'DOGE'},
                                                                                              {'label': 'LTC', 'value': 'LTC'},
                                                                                              {'label': 'BCH', 'value': 'BCH'},
                                                                                              {'label': 'USDC', 'value': 'USDC'}],
                                                                                        value='BTC', clearable=False, style=dict(width='150px', verticalAlign="bottom")))])]),
                                          html.Div(['Data used for calculation: Update from ', html.Span(id='slippagePoolLastUpdate'), ', Pool-size of ',
                                                    html.Span(id='slippagePoolCoinA'), ' and ',
                                                    html.Span(id='slippagePoolCoinB')], style={'margin-top': 15}),
                                          html.Table([html.Tr([html.Td('Do you want to buy or sell DFI?'),
                                                               html.Td(dcc.Dropdown(id='slippageOrderSelection', options=[{'label': 'buy', 'value': 'buy'},
                                                                                                                         {'label': 'sell', 'value': 'sell'}],
                                                                                    value='buy', clearable=False, style=dict(width='150px', verticalAlign="bottom")))]),
                                                      html.Tr([html.Td('How many DFI should be swapped?'),
                                                               html.Td(dcc.Input(id="slippageCoinAmount", type='number', debounce=True, value=20000))])
                                                      ],
                                                               style=dict(marginTop='30px')),
                                          dbc.Row([dbc.Col(dcc.Graph(id='figureSlippage', config={'displayModeBar': False}),style={'margin-top': 10}, lg=8, xl=9, align='start'),
                                                   dbc.Col([html.Div([html.B('Swapped coins'), html.Br(), 'DFI: ', html.Span(id='slippageSwappedDFI'), html.Br(), html.Span(id='slippageSwappedCoinB')]),
                                                            html.Div([html.B('Price ranges for swap'), html.Br(),
                                                                      'Start: ', html.Span(id='slippageStartPrice'), html.Br(),
                                                                      'Mean: ', html.Span(id='slippageMeanPrice'), html.Br(),
                                                                      'End: ', html.Span(id='slippageEndPrice')], style={'margin-top': 25})],
                                                           style={'margin-top': 10}, lg=4, xl=3, align='start')]),
                                          html.Div([html.B('Remark: '), 'This calculation is just an approximation based on own calculation. Real swap may differ.'], style={'margin-top': 10}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoSlippage")), style={'margin-top': 15})]))]
        return content

    @staticmethod
    def createSlippageGraph(data, bgImage, selectedPool, selectedOrder, coinAmount):
        figSlippage = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        if selectedPool == 'USDT':
            tickFormatYAxis = ",.2f"
            hoverTemplateRepresenation = '%{y:,.3f} USDT/DFI'
            yAxisLabel = 'Coinprice in USDT/DFI'
        elif selectedPool == 'USDC':
            tickFormatYAxis = ",.2f"
            hoverTemplateRepresenation = '%{y:,.3f} USDC/DFI'
            yAxisLabel = 'Coinprice in USDC/DFI'
        elif selectedPool == 'ETH':
            tickFormatYAxis = ",.5f"
            hoverTemplateRepresenation = '%{y:,.8f} ETH/DFI'
            yAxisLabel = 'Coinprice in ETH/DFI'
        elif selectedPool == 'DOGE':
            tickFormatYAxis = ",.2f"
            hoverTemplateRepresenation = '%{y:,.2f} DOGE/DFI'
            yAxisLabel = 'Coinprice in DOGE/DFI'
        elif selectedPool == 'LTC':
            tickFormatYAxis = ",.4f"
            hoverTemplateRepresenation = '%{y:,.6f} LTC/DFI'
            yAxisLabel = 'Coinprice in LTC/DFI'
        elif selectedPool == 'BCH':
            tickFormatYAxis = ",.4f"
            hoverTemplateRepresenation = '%{y:,.6f} BCH/DFI'
            yAxisLabel = 'Coinprice in BCH/DFI'
        else:
            tickFormatYAxis = ",.7f"
            hoverTemplateRepresenation = '%{y:,.8f} BTC/DFI'
            yAxisLabel = 'Coinprice in BTC/DFI'

        currDFI = data[selectedPool+'-DFI_reserveB'].dropna().iloc[-1]
        curr2ndCoin = data[selectedPool+'-DFI_reserveA'].dropna().iloc[-1]
        currLT = np.sqrt(currDFI*curr2ndCoin)

        # start and end point calculation
        currRatio = curr2ndCoin/currDFI
        if selectedOrder=='sell':
            endPrice = currLT ** 2 / ((currDFI + coinAmount) ** 2)
            amountGetCoin = curr2ndCoin - (currLT ** 2 / (currDFI + coinAmount))
            meanPrice = amountGetCoin / coinAmount
            # calculation over range
            amountRange = np.linspace(0, coinAmount*2.5, 1000)
            priceRange = currLT**2/((currDFI+amountRange)**2)

        elif selectedOrder=='buy':
            endPrice = currLT ** 2 / ((currDFI - coinAmount) ** 2)
            amountGetCoin = curr2ndCoin - (currLT ** 2 / (currDFI - coinAmount))
            meanPrice = - amountGetCoin / coinAmount
            # calculation over range
            amountRange = np.linspace(0, np.minimum(coinAmount*2.5, currDFI), 1000)
            priceRange = currLT**2/((currDFI-amountRange)**2)

        swappedDFI = f"{coinAmount:.8f}"
        swappedCoinB = selectedPool+': '+f"{amountGetCoin:.8f}"

        traceCurve = dict(type='scatter', name='DFI amount', x=amountRange, y=priceRange,
                                mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate=hoverTemplateRepresenation)
        traceCoins2Sell = dict(type='scatter', name='DFI amount', x=[coinAmount, coinAmount],
                               y=[np.min(priceRange)-(np.max(priceRange)-np.min(priceRange))*0.1, np.max(priceRange)+(np.max(priceRange)-np.min(priceRange))*0.1],
                                mode='lines', line=dict(color='#7f50ff', dash='dot'), line_width=2, hovertemplate=hoverTemplateRepresenation, showlegend=False)
        figSlippage.add_trace(traceCurve, 1, 1)
        figSlippage.add_trace(traceCoins2Sell, 1, 1)

        # show line for start price
        traceStartPrice = dict(type='scatter', name='Start price', x=[0, coinAmount],  y=[currRatio, currRatio],
                                mode='lines', line=dict(color='#7f50ff', dash='dash'), line_width=3, hovertemplate=hoverTemplateRepresenation)
        figSlippage.add_trace(traceStartPrice, 1, 1)
        figSlippage.add_annotation(x=coinAmount*1.02, y=currRatio, text="Start price", showarrow=False,  font=dict(color="#7f50ff"), bgcolor="#ffffff", xanchor='left')

        # show line for end price
        traceStartPrice = dict(type='scatter', name='End price', x=[0, coinAmount],  y=[endPrice, endPrice],
                                mode='lines', line=dict(color='#7f50ff', dash='dash'), line_width=3, hovertemplate=hoverTemplateRepresenation)
        figSlippage.add_trace(traceStartPrice, 1, 1)
        figSlippage.add_annotation(x=coinAmount*1.02, y=endPrice, text="End price", showarrow=False, font=dict(color="#7f50ff"), bgcolor="#ffffff", xanchor='left')

        # show line for mean price
        traceStartPrice = dict(type='scatter', name='Mean price', x=[0, coinAmount],  y=[meanPrice, meanPrice],
                                mode='lines', line=dict(color='#7f50ff', dash='dash'), line_width=3, hovertemplate=hoverTemplateRepresenation)
        figSlippage.add_trace(traceStartPrice, 1, 1)
        figSlippage.add_annotation(x=coinAmount*1.02, y=meanPrice, text="Mean price", showarrow=False,  font=dict(color="#7f50ff"), bgcolor="#ffffff", xanchor='left')




        figSlippage.update_yaxes(title_text=yAxisLabel, tickformat=tickFormatYAxis, gridcolor='#6c757d', color='#6c757d',
                               zerolinecolor='#6c757d', row=1, col=1)
        figSlippage.update_xaxes(title_text="Coin amount to sell", gridcolor='#6c757d', #range=[date14DaysBack.strftime('%Y-%m-%d'), lastValidDate],
                               showticklabels=True, color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)



        #add background picture
        figSlippage.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figSlippage.update_layout(margin={"t": 30, "l": 0, "b": 0, 'r': 0},
                                hovermode='x unified',
                                hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                showlegend=False
                                )
        figSlippage.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figSlippage.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figSlippage.layout.legend.font.color = '#6c757d'  # font color legend
        return figSlippage, swappedDFI, swappedCoinB, \
               f"{currRatio:.8f} "+selectedPool+'/DFI', f"{meanPrice:.8f} "+selectedPool+'/DFI', f"{endPrice:.8f} "+selectedPool+'/DFI'


    @staticmethod
    def getSlippageExplanation():
        slippageCardExplanation = [html.P(['Every swap on the DEX influences the pool ratio and thus the coinprice of the selected pair. This calculator shows the influence and the movement of the pool ratio. '
                                           'Especially for bigger swaps you will see the resulting mean price.']),
                                   html.P(['All calculation is based on the locked coins of each side and two formulas:',
                                           html.Ul([html.Li('Coin price = (coin amount side 1)/(coin amount side 2)'),
                                                   html.Li('Liquidity Token = sqrt( (coin amount side 1)^2 * (coin amount side 2)^2 )')]),
                                           'This calculation can differ from real behaviour on DEX and also the data may not be up to date. So, be careful with bigger trades.']),
                                    html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                                  ]
        return slippageCardExplanation