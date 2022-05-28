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
                                                               html.Td(dcc.Dropdown(id='slippagePoolSelection', options=[
                                                                   {'label': 'BTC', 'value': 'BTC-DFI'},
                                                                   {'label': 'ETH', 'value': 'ETH-DFI'},
                                                                   {'label': 'USDT', 'value': 'USDT-DFI'},
                                                                   {'label': 'DOGE', 'value': 'DOGE-DFI'},
                                                                   {'label': 'LTC', 'value': 'LTC-DFI'},
                                                                   {'label': 'BCH', 'value': 'BCH-DFI'},
                                                                   {'label': 'USDC', 'value': 'USDC-DFI'},
                                                                   {'label': 'dUSD', 'value': 'DUSD-DFI'},
                                                                   {'label': 'AAPL', 'value': 'AAPL-DUSD'},
                                                                   {'label': 'AMZN', 'value': 'AMZN-DUSD'},
                                                                   {'label': 'ARKK', 'value': 'ARKK-DUSD'},
                                                                   {'label': 'BABA', 'value': 'BABA-DUSD'},
                                                                   {'label': 'BRK.B', 'value': 'BRK.B-DUSD'},
                                                                   {'label': 'COIN', 'value': 'COIN-DUSD'},
                                                                   {'label': 'CS', 'value': 'CS-DUSD'},
                                                                   {'label': 'DIS', 'value': 'DIS-DUSD'},
                                                                   {'label': 'EEM', 'value': 'EEM-DUSD'},
                                                                   {'label': 'FB', 'value': 'FB-DUSD'},
                                                                   {'label': 'GLD', 'value': 'GLD-DUSD'},
                                                                   {'label': 'GME', 'value': 'GME-DUSD'},
                                                                   {'label': 'GSG', 'value': 'GSG-DUSD'},
                                                                   {'label': 'GOOGL', 'value': 'GOOGL-DUSD'},
                                                                   {'label': 'INTC', 'value': 'INTC-DUSD'},
                                                                   {'label': 'KO', 'value': 'KO-DUSD'},
                                                                   {'label': 'MCHI', 'value': 'MCHI-DUSD'},
                                                                   {'label': 'MSFT', 'value': 'MSFT-DUSD'},
                                                                   {'label': 'MSTR', 'value': 'MSTR-DUSD'},
                                                                   {'label': 'NFLX', 'value': 'NFLX-DUSD'},
                                                                   {'label': 'NVDA', 'value': 'NVDA-DUSD'},
                                                                   {'label': 'PDBC', 'value': 'PDBC-DUSD'},
                                                                   {'label': 'PG', 'value': 'PG-DUSD'},
                                                                   {'label': 'PLTR', 'value': 'PLTR-DUSD'},
                                                                   {'label': 'PYPL', 'value': 'PYPL-DUSD'},
                                                                   {'label': 'QQQ', 'value': 'QQQ-DUSD'},
                                                                   {'label': 'SAP', 'value': 'SAP-DUSD'},
                                                                   {'label': 'SLV', 'value': 'SLV-DUSD'},
                                                                   {'label': 'SPY', 'value': 'SPY-DUSD'},
                                                                   {'label': 'TLT', 'value': 'TLT-DUSD'},
                                                                   {'label': 'TSLA', 'value': 'TSLA-DUSD'},
                                                                   {'label': 'URA', 'value': 'URA-DUSD'},
                                                                   {'label': 'URTH', 'value': 'URTH-DUSD'},
                                                                   {'label': 'VNQ', 'value': 'VNQ-DUSD'},
                                                                   {'label': 'VOO', 'value': 'VOO-DUSD'},
                                                               ],
                                                                                        value='BTC-DFI', clearable=False, style=dict(width='150px', verticalAlign="bottom")))])]),
                                          html.Div(['Data used for calculation: Update from ', html.Span(id='slippagePoolLastUpdate'), ', Pool-size of ',
                                                    html.Span(id='slippagePoolCoinA'), ' and ',
                                                    html.Span(id='slippagePoolCoinB')], style={'margin-top': 15}),
                                          html.Table([html.Tr([html.Td(['Do you want to buy or sell ',html.Span(id='slippagePoolCoinBName1'),'?']),
                                                               html.Td(dcc.Dropdown(id='slippageOrderSelection', options=[{'label': 'buy', 'value': 'buy'},
                                                                                                                         {'label': 'sell', 'value': 'sell'}],
                                                                                    value='buy', clearable=False, style=dict(width='150px', verticalAlign="bottom")))]),
                                                      html.Tr([html.Td(['How many ',html.Span(id='slippagePoolCoinBName2'),' should be swapped?']),
                                                               html.Td(dcc.Input(id="slippageCoinAmount", type='number', debounce=True, value=20000))])
                                                      ],
                                                               style=dict(marginTop='30px')),
                                          dbc.Row([dbc.Col(dcc.Graph(id='figureSlippage', config={'displayModeBar': False}),style={'margin-top': 10}, lg=8, xl=9, align='start'),
                                                   dbc.Col([html.Div([html.B('Swapped coins'), html.Br(),
                                                                      html.Span(id='slippageSwappedCoinA'), html.Br(),
                                                                      html.Span(id='slippageSwappedCoinB')]),
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

        if selectedPool[selectedPool.index('-') + 1:] == 'DFI':
            priceUnit = selectedPool[:selectedPool.index('-')] + '/' + selectedPool[selectedPool.index('-') + 1:]
        else:
            priceUnit = selectedPool[selectedPool.index('-') + 1:] + '/' + selectedPool[:selectedPool.index('-')]

        if selectedPool == 'BTC-DFI':
            tickFormatYAxis = ",.7f"
            hoverTemplateRepresenation = '%{y:,.8f} BTC/DFI'
            yAxisLabel = 'Coinprice in BTC/DFI'
        elif selectedPool == 'USDT-DFI':
            tickFormatYAxis = ",.2f"
            hoverTemplateRepresenation = '%{y:,.3f} USDT/DFI'
            yAxisLabel = 'Coinprice in USDT/DFI'
        elif selectedPool == 'USDC-DFI':
            tickFormatYAxis = ",.2f"
            hoverTemplateRepresenation = '%{y:,.3f} USDC/DFI'
            yAxisLabel = 'Coinprice in USDC/DFI'
        elif selectedPool == 'ETH-DFI':
            tickFormatYAxis = ",.5f"
            hoverTemplateRepresenation = '%{y:,.8f} ETH/DFI'
            yAxisLabel = 'Coinprice in ETH/DFI'
        elif selectedPool == 'DOGE-DFI':
            tickFormatYAxis = ",.2f"
            hoverTemplateRepresenation = '%{y:,.2f} DOGE/DFI'
            yAxisLabel = 'Coinprice in DOGE/DFI'
        elif selectedPool == 'LTC-DFI':
            tickFormatYAxis = ",.4f"
            hoverTemplateRepresenation = '%{y:,.6f} LTC/DFI'
            yAxisLabel = 'Coinprice in LTC/DFI'
        elif selectedPool == 'BCH-DFI':
            tickFormatYAxis = ",.4f"
            hoverTemplateRepresenation = '%{y:,.6f} BCH/DFI'
            yAxisLabel = 'Coinprice in BCH/DFI'
        else:
            tickFormatYAxis = ",.2f"
            hoverTemplateRepresenation = '%{y:,.3f} '+priceUnit
            yAxisLabel = 'Coinprice in '+priceUnit

        currDFI = data[selectedPool+'_reserveB'].dropna().iloc[-1]
        curr2ndCoin = data[selectedPool+'_reserveA'].dropna().iloc[-1]
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


        swappedCoinA = selectedPool[:selectedPool.index('-')] + ': '+f"{amountGetCoin:.8f}"
        swappedCoinB = selectedPool[selectedPool.index('-')+1:] + ': ' + f"{coinAmount:.8f}"

        # change ratio in case of dToken pools
        if selectedPool[selectedPool.index('-') + 1:] == 'DUSD':
            currRatio = 1/currRatio
            meanPrice = 1/meanPrice
            endPrice = 1/endPrice
            priceRange = 1/priceRange


        traceCurve = dict(type='scatter', name='Price', x=amountRange, y=priceRange,
                                mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate=hoverTemplateRepresenation)
        traceCoins2Sell = dict(type='scatter', name='amount', x=[coinAmount, coinAmount],
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

        return figSlippage, swappedCoinA, swappedCoinB, \
               f"{currRatio:.8f} "+priceUnit, \
               f"{meanPrice:.8f} "+priceUnit, \
               f"{endPrice:.8f} "+priceUnit


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