import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

class pricesDTokenViewClass:

    def getPricesDTokenContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info dToken prices - DEX vs. Oracles"),
                              dbc.ModalBody(self.getPricesExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoPricesDToken", className="ml-auto"))],
                                    id="modalPricesDToken", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['dToken prices - DEX vs. Oracles']),
                                          html.Table([html.Tr([html.Td('Select dToken for price evaluation:'),
                                                               html.Td(dcc.Dropdown(id='vaultsLoansPricesDtoken', options=[{'label': 'dUSD', 'value': 'DUSD'},
                                                                                                                           {'label': 'DFI in dUSD', 'value': 'DFI'},
                                                                                                                           {'label': 'AAPL', 'value': 'AAPL'},
                                                                                                                           {'label': 'ADDYY', 'value': 'ADDYY'},
                                                                                                                           {'label': 'AMZN', 'value': 'AMZN'},
                                                                                                                           {'label': 'ARKK', 'value': 'ARKK'},
                                                                                                                           {'label': 'ARKX', 'value': 'ARKX'},
                                                                                                                           {'label': 'BABA', 'value': 'BABA'},
                                                                                                                           {'label': 'BRK.B', 'value': 'BRK.B'},
                                                                                                                           {'label': 'COIN', 'value': 'COIN'},
                                                                                                                           {'label': 'CS', 'value': 'CS'},
                                                                                                                           {'label': 'DAX', 'value': 'DAX'},
                                                                                                                           {'label': 'DIS', 'value': 'DIS'},
                                                                                                                           {'label': 'EEM', 'value': 'EEM'},
                                                                                                                           {'label': 'FB', 'value': 'FB'},
                                                                                                                           {'label': 'GLD', 'value': 'GLD'},
                                                                                                                           {'label': 'GS', 'value': 'GS'},
                                                                                                                           {'label': 'GSG', 'value': 'GSG'},
                                                                                                                           {'label': 'GME', 'value': 'GME'},
                                                                                                                           {'label': 'GOOGL', 'value': 'GOOGL'},
                                                                                                                           {'label': 'GOVT', 'value': 'GOVT'},
                                                                                                                           {'label': 'INTC', 'value': 'INTC'},
                                                                                                                           {'label': 'JNJ', 'value': 'JNJ'},
                                                                                                                           {'label': 'KO', 'value': 'KO'},
                                                                                                                           {'label': 'MCHI', 'value': 'MCHI'},
                                                                                                                           {'label': 'MSFT', 'value': 'MSFT'},
                                                                                                                           {'label': 'MSTR', 'value': 'MSTR'},
                                                                                                                           {'label': 'NFLX', 'value': 'NFLX'},
                                                                                                                           {'label': 'NVDA', 'value': 'NVDA'},
                                                                                                                           {'label': 'PDBC', 'value': 'PDBC'},
                                                                                                                           {'label': 'PG', 'value': 'PG'},
                                                                                                                           {'label': 'PLTR', 'value': 'PLTR'},
                                                                                                                           {'label': 'PPLT', 'value': 'PPLT'},
                                                                                                                           {'label': 'PYPL', 'value': 'PYPL'},
                                                                                                                           {'label': 'QQQ', 'value': 'QQQ'},
                                                                                                                           {'label': 'SAP', 'value': 'SAP'},
                                                                                                                           {'label': 'SLV', 'value': 'SLV'},
                                                                                                                           {'label': 'SPY', 'value': 'SPY'},
                                                                                                                           {'label': 'TAN', 'value': 'TAN'},
                                                                                                                           {'label': 'TLT', 'value': 'TLT'},
                                                                                                                           {'label': 'TSLA', 'value': 'TSLA'},
                                                                                                                           {'label': 'UL', 'value': 'UL'},
                                                                                                                           {'label': 'UNG', 'value': 'UNG'},
                                                                                                                           {'label': 'USO', 'value': 'USO'},
                                                                                                                           {'label': 'URA', 'value': 'URA'},
                                                                                                                           {'label': 'URTH', 'value': 'URTH'},
                                                                                                                           {'label': 'VBK', 'value': 'VBK'},
                                                                                                                           {'label': 'VNQ', 'value': 'VNQ'},
                                                                                                                           {'label': 'VOO', 'value': 'VOO'},
                                                                                                                           {'label': 'WMT', 'value': 'WMT'},
                                                                                                                           {'label': 'XLE', 'value': 'XLE'},
                                                                                                                           {'label': 'XLRE', 'value': 'XLRE'},
                                                                                                                           {'label': 'XOM', 'value': 'XOM'},],
                                                                                    value='DUSD', clearable=False, style=dict(width='150px', verticalAlign="bottom")))])]),
                                          dcc.Graph(id='figurePricesDToken', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoPricesDToken")))
                                          ]))]
        return content


    @staticmethod
    def createPricesDToken(data, bgImage, representation):
        figPrices = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        if representation =='DUSD':
            dataDEX = (data['DFI-USD']/data['DUSD-DFI_reserveA/reserveB']).dropna()
            dataDEX_USDT = (data['DUSD-DFI_reserveB/reserveA']*data['USDT-DFI_reserveA/reserveB']).dropna()
            dataOracle = (data['DFI-USD']/data['DFI-USD']).dropna()
            selectionDEX = dataDEX != 0
            figPrices.update_yaxes(range=[0.60, 1.4])
        elif representation =='DFI':
            dataDEX = data['DUSD-DFI_reserveA/reserveB'].dropna()
            dataDEX_USDT = data['USDT-DFI_reserveA/reserveB'].dropna()
            dataOracle = data['DFI-USD'].dropna()
            selectionDEX = dataDEX != 0
        else:
            dataDEX = data[representation+'-DUSD_reserveB/reserveA'].dropna()
            dataDEX_USDT = (data[representation+'-DUSD_reserveB/reserveA']*data['DUSD-DFI_reserveB/reserveA']*data['USDT-DFI_reserveA/reserveB']).dropna()
            dataOracle = data[representation+'-USD'].dropna()
            selectionDEX = dataDEX != 0

        lastValidDate = datetime.utcfromtimestamp(dataDEX.index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        trace_priceDEX = dict(type='scatter', name='DEX price in dUSD', x=dataDEX[selectionDEX].index, y=dataDEX[selectionDEX],
                                 mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:.f}')

        trace_priceOracle = dict(type='scatter', name='Oracle price in USD', x=dataOracle.index, y=dataOracle,
                              mode='lines', line=dict(color='#ff9fe2'), line_width=3, hovertemplate='%{y:.f}')

        trace_priceDEXUSDT = dict(type='scatter', name='DEX price in dUSDT', x=dataDEX_USDT.index, y=dataDEX_USDT,
                              mode='lines', line=dict(color='#ff9fe2', dash='dot'), line_width=3, hovertemplate='%{y:.f}')

        if representation =='DUSD':
            trace_priceDEX['name'] = 'DEX price of dUSD-DFI pool'
            trace_priceDEXUSDT['name'] = 'DEX price of dUSD-DFI pool in USDT'
            trace_priceDEX_USDTPool = dict(type='scatter', name='DEX price of dUSD-USDT pool', x=data['USDT-DUSD_reserveA/reserveB'].dropna().index, y=data['USDT-DUSD_reserveA/reserveB'].dropna(),
                                 mode='lines', line=dict(color='#00ac84'), line_width=3, hovertemplate='%{y:.f}')
            trace_priceDEX_USDCPool = dict(type='scatter', name='DEX price of dUSD-USDC pool', x=data['USDC-DUSD_reserveA/reserveB'].dropna().index, y=data['USDC-DUSD_reserveA/reserveB'].dropna(),
                                 mode='lines', line=dict(color='#2975ca'), line_width=3, hovertemplate='%{y:.f}')

        figPrices.add_trace(trace_priceDEX, 1, 1)
        figPrices.add_trace(trace_priceOracle, 1, 1)
        figPrices.add_trace(trace_priceDEXUSDT, 1, 1)

        if representation =='DUSD':
            figPrices.add_trace(trace_priceDEX_USDTPool, 1, 1)
            figPrices.add_trace(trace_priceDEX_USDCPool, 1, 1)

        figPrices.update_yaxes(title_text='dToken price', gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figPrices.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d',
                               range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figPrices.update_layout(xaxis=dict(
            rangeselector=dict(
                buttons=list([dict(count=14, label="14d", step="day", stepmode="backward"),
                              dict(count=30, label="30d", step="day", stepmode="backward"),
                              dict(count=2, label="2m", step="month", stepmode="backward"),
                              dict(count=6, label="6m", step="month", stepmode="backward"),
                              dict(count=1, label="YTD", step="year", stepmode="todate"),
                              dict(count=1, label="1y", step="year", stepmode="backward"),
                              dict(step="all")])),
            rangeslider=dict(visible=False),
            type="date"))

        figPrices.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))

        figPrices.update_layout(margin={"t": 60, "l": 0, "b": 0, "r": 0},
                                barmode='stack',
                                hovermode='x unified',
                                hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                legend=dict(orientation="h",
                                            yanchor="top",
                                            y=-0.12,
                                            xanchor="right",
                                            x=1),
                                )
        figPrices.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figPrices.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figPrices.layout.legend.font.color = '#6c757d'  # font color legend
        return figPrices


    @staticmethod
    def getPricesExplanation():
        dTokenPricesCardExplanation = [html.P(['dTokens on DefiChain are tradable on the DEX and the current price is defined by the pool ratio. The token price is not directly linked to the real asset. '
                                               'The only connection to the world outside the blockchain is the price feed of the oracle, which is used in the loan. With the oracle price the '
                                               'current collateralization ratio is determined and defines the liquidation level.'],style={'text-align': 'justify'}),
                                       html.P(['This graphs shows both price informations - DEX and oracle - over time for the selected ticker symbol. Additionally the price in dUSDT is shown for a composite swap from '
                                               'dUSDT to the selected dToken. In this case you have multiple premium/discounts influencing the price.'], style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return dTokenPricesCardExplanation