import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import dateutil.relativedelta


class coinpriceViewClass:

    def getCoinpriceContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info DEX Coinprice"),
                              dbc.ModalBody(self.getCoinPriceExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoCoinprice", className="ml-auto"))], id="modalCoinprice", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Coinprices on DEX and other exchanges']),
                                          html.Table([html.Tr([html.Td('Select price feed reference for deviation calculation:'),
                                          html.Td(dcc.Dropdown(id='dexCoinpriceReference', options=[{'label': 'Coingecko', 'value': 'Coingecko'},
                                                                                                 {'label': 'Bittrex', 'value': 'Bittrex'}],
                                                               value='Coingecko', clearable=False, style=dict(width='200px', verticalAlign="bottom")))]),
                                          html.Tr([html.Td('Select Coin for absolute price graph:'),
                                          html.Td(dcc.Dropdown(id='dexCoinpriceCoin', options=[{'label': 'BTC', 'value': 'BTC'},
                                                                                            {'label': 'ETH', 'value': 'ETH'},
                                                                                            {'label': 'USDT', 'value': 'USDT'},
                                                                                            {'label': 'LTC', 'value': 'LTC'},
                                                                                            {'label': 'DOGE', 'value': 'DOGE'},
                                                                                            {'label': 'BCH', 'value': 'BCH'}],
                                                               value='BTC', clearable=False, style=dict(width='200px',verticalAlign="bottom")))])]),
                                          dbc.Row([dbc.Col(dcc.Graph(id='figureCoinpriceLongterm', config={'displayModeBar': False}), lg=7, xl=8, align='start'),
                                                   dbc.Col(dcc.Graph(id='figureCoinpriceShortterm', config={'displayModeBar': False}), lg=5, xl=4)], no_gutters=True),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoCoinprice")))])),
                   dcc.Interval(id='dexCoinprice60s', interval=60 * 1000, n_intervals=0),
                   dcc.Interval(id='dexCoinprice600s', interval=600 * 1000, n_intervals=0),
                   ]
        return content

    @staticmethod
    def createPriceGraph(data, selectedCoin, selectedReference, selectedTimeRange, bgImage):

        if selectedTimeRange == 'Long':
            leftMarginGraphic = 130
            rightMarginGraphic = 20
            bgimageSize = 0.6
            lastValidDate = datetime.utcfromtimestamp(data.index.values[-1].tolist()/1e9)
            date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)
            startIndex = data[data.index > date14DaysBack].index.values[0]
        else:
            leftMarginGraphic = 0
            rightMarginGraphic = 50
            bgimageSize = 0.8
            startIndex = data.index.values[0]

        # Plotting long term price
        figPrice = make_subplots(
            rows=2, cols=1,
            vertical_spacing=0.15,
            row_width=[0.6, 0.4],  # from bottom to top
            specs=[[{}],
                   [{}]],
            shared_xaxes=True,
            subplot_titles=(['Relative price deviation', 'Absolute prices']))
        figPrice.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figPrice.layout.annotations[0].font.size = 20

        figPrice.layout.annotations[1].font.color = '#6c757d'
        figPrice.layout.annotations[1].font.size = 20

        # relative price deviation
        trace_relLongBTC = dict(type='scatter', name='BTC', x=data['BTC-DFI_relPriceDev'+selectedReference].loc[startIndex:].dropna().index, y=data['BTC-DFI_relPriceDev'+selectedReference].loc[startIndex:].dropna()*100,
                                mode='lines', line=dict(color='#da3832'), line_width=2, hovertemplate='%{y:.2f}%')
        trace_relLongETH = dict(type='scatter', name='ETH', x=data['ETH-DFI_relPriceDev'+selectedReference].loc[startIndex:].dropna().index, y=data['ETH-DFI_relPriceDev'+selectedReference].loc[startIndex:].dropna()*100,
                                mode='lines', line=dict(color='#617dea'), line_width=2, hovertemplate='%{y:.2f}%')
        trace_relLongUSDT = dict(type='scatter', name='USDT', x=data['USDT-DFI_relPriceDev'+selectedReference].loc[startIndex:].dropna().index, y=data['USDT-DFI_relPriceDev'+selectedReference].loc[startIndex:].dropna()*100,
                                 mode='lines', line=dict(color='#22b852'), line_width=2, hovertemplate='%{y:.2f}%')
        trace_relLongDoge = dict(type='scatter', name='DOGE', x=data['DOGE-DFI_relPriceDev'+selectedReference].loc[startIndex:].dropna().index, y=data['DOGE-DFI_relPriceDev'+selectedReference].loc[startIndex:].dropna()*100,
                                 mode='lines', line=dict(color='#c2a634'), line_width=2, hovertemplate='%{y:.2f}%')
        trace_relLongLTC = dict(type='scatter', name='LTC', x=data['LTC-DFI_relPriceDev'+selectedReference].loc[startIndex:].dropna().index, y=data['LTC-DFI_relPriceDev'+selectedReference].loc[startIndex:].dropna()*100,
                                mode='lines', line=dict(color='#ff2ebe'), line_width=2, hovertemplate='%{y:.2f}%')
        trace_relLongBCH = dict(type='scatter', name='BCH', x=data['BCH-DFI_relPriceDev'+selectedReference].loc[startIndex:].dropna().index, y=data['BCH-DFI_relPriceDev'+selectedReference].loc[startIndex:].dropna()*100,
                                mode='lines', line=dict(color='#410eb2'), line_width=2, hovertemplate='%{y:.2f}%')
        figPrice.add_trace(trace_relLongBTC, 1, 1)
        figPrice.add_trace(trace_relLongETH, 1, 1)
        figPrice.add_trace(trace_relLongUSDT, 1, 1)
        figPrice.add_trace(trace_relLongDoge, 1, 1)
        figPrice.add_trace(trace_relLongLTC, 1, 1)
        figPrice.add_trace(trace_relLongBCH, 1, 1)

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
        else:
            tickFormatYAxis = ",.7f"
            lineColor = '#da3832'
            priceCurrency = 'BTC/DFI'

        trace_absPriceDEX = dict(type='scatter', name='DEX', x=data[selectedCoin+'-DFI_reserveA/reserveB'].loc[startIndex:].dropna().index, y=data[selectedCoin+'-DFI_reserveA/reserveB'].loc[startIndex:].dropna(),
                                 mode='lines', line=dict(color=lineColor), line_width=3, hovertemplate='%{y:.8f} '+priceCurrency)
        trace_absPriceCG = dict(type='scatter', name='CoinGecko', x=data[selectedCoin+'-DFI_DFIPrices'].loc[startIndex:].dropna().index, y=data[selectedCoin+'-DFI_DFIPrices'].loc[startIndex:].dropna(),
                                mode='lines', line=dict(color='#000000'), line_width=2, hovertemplate='%{y:.8f} '+priceCurrency)
        trace_absPriceBittrex = dict(type='scatter', name='Bittrex', x=data[selectedCoin+'-DFI_DFIPricesBittrex'].loc[startIndex:].dropna().index, y=data[selectedCoin+'-DFI_DFIPricesBittrex'].loc[startIndex:].dropna(),
                                     mode='lines', line=dict(color='#7f7f7f'), line_width=2, hovertemplate='%{y:.8f} '+priceCurrency)

        figPrice.add_trace(trace_absPriceCG, 2, 1)
        figPrice.add_trace(trace_absPriceBittrex, 2, 1)
        figPrice.add_trace(trace_absPriceDEX, 2, 1)

        figPrice.update_yaxes(title_text='Rel. price deviation', tickformat=",.1f", gridcolor='#6c757d', color='#6c757d',
                                      zerolinecolor='#6c757d', row=1, col=1)
        figPrice.update_yaxes(title_text='Absolute prices', tickformat=tickFormatYAxis, gridcolor='#6c757d', color='#6c757d',
                                      zerolinecolor='#6c757d', row=2, col=1)

        if selectedTimeRange == 'Long':
            figPrice.update_yaxes(range=[-25, 25], row=1, col=1)

        figPrice.update_xaxes(gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figPrice.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=2, col=1)

        # add background picture
        figPrice.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.832, sizex=bgimageSize, sizey=bgimageSize,  xanchor="center", yanchor="middle", opacity=0.25))
        figPrice.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.26, sizex=bgimageSize, sizey=bgimageSize, xanchor="center", yanchor="middle", opacity=0.25))

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
    def getCoinPriceExplanation():
        coinAddressCardExplanation = [html.P(['The decentral exchange (DEX) on DefiChain has, like other DEXes, no classical orderbook. The coin ratio in the liquidity pool represents the price and can be influenced by '
                                       ' coin swaps. Each swap will add coins on one side and will remove coins on the other side of the liquidity pool. Thus the coin price is a helpful parameter for liquidity providers and arbitrage traders. '],style={'text-align': 'justify'}),
                               html.P(['This tab is divided in 2 parts. On the left side the longterm behaviour of the coin prices is shown. And the right side represents the last 1.5 hours with a higher sample rate of data points every minute. '
                                       'For each coin the relative deviation to the coin price from Coingecko is calculated and shown. '],style={'text-align': 'justify'}),
                               html.P(['The user can select a coin to get more details. The absolut prices of the DEX and Coingecko will then be drawn for the selection.'],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return coinAddressCardExplanation

