import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import dateutil.relativedelta


class coinpricesViewClass:


    def getCoinpricesContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info DEX Coinprice"),
                              dbc.ModalBody(self.getCoinpricesExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoCoinprices", className="ml-auto"))], id="modalCoinprices", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Coinprices on DEX']),
                                          html.Table([html.Tr([html.Td('Select Coin for price graph:'),
                                                               html.Td(dcc.Dropdown(id='dexCoinpriceCoin', options=[{'label': 'BTC', 'value': 'BTC'},
                                                                                            {'label': 'ETH', 'value': 'ETH'},
                                                                                            {'label': 'USDT', 'value': 'USDT'},
                                                                                            {'label': 'LTC', 'value': 'LTC'},
                                                                                            {'label': 'DOGE', 'value': 'DOGE'},
                                                                                            {'label': 'BCH', 'value': 'BCH'},
                                                                                            {'label': 'USDC', 'value': 'USDC'},
                                                                                            {'label': 'EUROC', 'value': 'EUROC'}],
                                                                                    value='BTC', clearable=False, style=dict(width='200px',verticalAlign="bottom")))])]),
                                          dcc.Graph(id='figureCoinprices', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoCoinprices")))]))
                   ]
        return content

    @staticmethod
    def createPriceGraph(data, selectedCoin, bgImage):

        # Plotting long term price
        figPrice = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True)

        bgimageSize = 0.6
        lastValidDate = datetime.utcfromtimestamp(data.index.values[-1].tolist()/1e9)
        date30DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=30)




        # absolute price
        if selectedCoin == 'USDT':
            tickFormatYAxis = ",.2f"
            lineColor = '#22b852'
            priceCurrency = 'USDT/DFI'
        elif selectedCoin == 'ETH':
            tickFormatYAxis = ",.5f"
            lineColor = '#617dea'
            priceCurrency = 'ETH/DFI'
        elif selectedCoin == 'DOGE':
            tickFormatYAxis = ",.2f"
            lineColor = '#c2a634'
            priceCurrency = 'DOGE/DFI'
        elif selectedCoin == 'LTC':
            tickFormatYAxis = ",.4f"
            lineColor = '#ff2ebe'
            priceCurrency = 'LTC/DFI'
        elif selectedCoin == 'BCH':
            tickFormatYAxis = ",.4f"
            lineColor = '#410eb2'
            priceCurrency = 'BCH/DFI'
        elif selectedCoin == 'USDC':
            tickFormatYAxis = ",.2f"
            lineColor = '#7f4c00'
            priceCurrency = 'USDC/DFI'
        elif selectedCoin == 'EUROC':
            tickFormatYAxis = ",.2f"
            lineColor = '#07bfff'
            priceCurrency = 'EUROC/DFI'
        else:
            tickFormatYAxis = ",.7f"
            lineColor = '#da3832'
            priceCurrency = 'BTC/DFI'

        trace_absPriceDEX = dict(type='scatter', name='DEX', x=data[selectedCoin+'-DFI_reserveA/reserveB'].dropna().index, y=data[selectedCoin+'-DFI_reserveA/reserveB'].dropna(),
                                 mode='lines', line=dict(color=lineColor), line_width=3, hovertemplate='%{y:.8f} '+priceCurrency)
        trace_absPriceCG = dict(type='scatter', name='CoinGecko', x=data[selectedCoin+'-DFI_DFIPrices'].dropna().index, y=data[selectedCoin+'-DFI_DFIPrices'].dropna(),
                                mode='lines', line=dict(color='#000000'), line_width=2, hovertemplate='%{y:.8f} '+priceCurrency, visible='legendonly')
        trace_absPriceBittrex = dict(type='scatter', name='Bittrex', x=data[selectedCoin+'-DFI_DFIPricesBittrex'].dropna().index, y=data[selectedCoin+'-DFI_DFIPricesBittrex'].dropna(),
                                     mode='lines', line=dict(color='#7f7f7f'), line_width=2, hovertemplate='%{y:.8f} '+priceCurrency, visible='legendonly')

        figPrice.add_trace(trace_absPriceCG, 1, 1)
        figPrice.add_trace(trace_absPriceBittrex, 1, 1)
        figPrice.add_trace(trace_absPriceDEX, 1, 1)

        figPrice.update_yaxes(title_text='Absolute prices', tickformat=tickFormatYAxis, gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figPrice.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                              range=[date30DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figPrice.update_layout(barmode='stack',
            xaxis=dict(
            rangeselector=dict(
                buttons=list([dict(count=30, label="30d", step="day", stepmode="backward"),
                              dict(count=2, label="2m", step="month", stepmode="backward"),
                              dict(count=6, label="6m", step="month", stepmode="backward"),
                              dict(count=1, label="YTD", step="year", stepmode="todate"),
                              dict(count=1, label="1y", step="year", stepmode="backward"),
                              dict(step="all")])),
            rangeslider=dict(visible=False),
            type="date"))

        # add background picture
        figPrice.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=bgimageSize, sizey=bgimageSize, xanchor="center", yanchor="middle", opacity=0.25))

        figPrice.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                               hovermode='x unified',
                               hoverlabel=dict(font_color="#6c757d"),
                               legend=dict(orientation="h",
                                                   yanchor="top",
                                                   y=-0.12,
                                                   xanchor="right",
                                                   x=1),
                                       )
        figPrice.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figPrice.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figPrice.layout.legend.font.color = '#6c757d'  # font color legend

        return figPrice


    @staticmethod
    def getCoinpricesExplanation():
        coinAddressCardExplanation = [html.P(['The decentral exchange (DEX) on DefiChain has, like other DEXes, no classical orderbook. The coin ratio in the liquidity pool represents the price and can be influenced by '
                                       ' coin swaps. Each swap will add coins on one side and will remove coins on the other side of the liquidity pool. This graph shows the coin ratio development over (nearly) complete time.'],style={'text-align': 'justify'}),
                                      html.P(['The user can select the coin, for which the absolut price of the DEX and Coingecko will be drawn.'],style={'text-align': 'justify'}),
                                      html.P([html.B('Hint:'),
                                              ' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                              ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                             style={'text-align': 'justify', 'fontSize': '0.7rem', 'color': '#6c757d'})
                                      ]
        return coinAddressCardExplanation

