import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

class premiumDTokenViewClass:

    def getPremiumDTokenContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info dToken prices - DEX vs. Oracles"),
                              dbc.ModalBody(self.getPremiumExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoPremiumDToken", className="ml-auto"))],
                                    id="modalPremiumDToken", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['dToken Premium (rel. deviation DEX vs. Oracles)']),
                                          dcc.Graph(figure=self.createPricesDToken(data, bgImage), id='figurePremiumDToken', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoPremiumDToken")))
                                          ]))]
        return content


    @staticmethod
    def createPricesDToken(data, bgImage):
        figPrices = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        hoverNumber = '%{y:.2f}%'
        lastValidDate = datetime.utcfromtimestamp(data['AAPL-USD'].index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        trace_premiumDUSD = dict(type='scatter', name='dSUD',
                              x=((data['DFI-USD']/data['DUSD-DFI_reserveA/reserveB'])-1).dropna().index,
                              y=((data['DFI-USD']/data['DUSD-DFI_reserveA/reserveB'])-1).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumAAPL = dict(type='scatter', name='dAAPL',
                              x=((data['AAPL-DUSD_reserveB/reserveA']-data['AAPL-USD'])/data['AAPL-USD']).dropna().index,
                              y=((data['AAPL-DUSD_reserveB/reserveA']-data['AAPL-USD'])/data['AAPL-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumAMZN = dict(type='scatter', name='dAMZN',
                              x=((data['AMZN-DUSD_reserveB/reserveA']-data['AMZN-USD'])/data['AMZN-USD']).dropna().index,
                              y=((data['AMZN-DUSD_reserveB/reserveA']-data['AMZN-USD'])/data['AMZN-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumARKK = dict(type='scatter', name='dARKK',
                              x=((data['ARKK-DUSD_reserveB/reserveA']-data['ARKK-USD'])/data['ARKK-USD']).dropna().index,
                              y=((data['ARKK-DUSD_reserveB/reserveA']-data['ARKK-USD'])/data['ARKK-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumBABA = dict(type='scatter', name='dBABA',
                              x=((data['BABA-DUSD_reserveB/reserveA']-data['BABA-USD'])/data['BABA-USD']).dropna().index,
                              y=((data['BABA-DUSD_reserveB/reserveA']-data['BABA-USD'])/data['BABA-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumCOIN = dict(type='scatter', name='dCOIN',
                              x=((data['COIN-DUSD_reserveB/reserveA']-data['COIN-USD'])/data['COIN-USD']).dropna().index,
                              y=((data['COIN-DUSD_reserveB/reserveA']-data['COIN-USD'])/data['COIN-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumEEM = dict(type='scatter', name='dEEM',
                              x=((data['EEM-DUSD_reserveB/reserveA']-data['EEM-USD'])/data['EEM-USD']).dropna().index,
                              y=((data['EEM-DUSD_reserveB/reserveA']-data['EEM-USD'])/data['EEM-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumGLD = dict(type='scatter', name='dGLD',
                              x=((data['GLD-DUSD_reserveB/reserveA']-data['GLD-USD'])/data['GLD-USD']).dropna().index,
                              y=((data['GLD-DUSD_reserveB/reserveA']-data['GLD-USD'])/data['GLD-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumGME = dict(type='scatter', name='dGME',
                              x=((data['GME-DUSD_reserveB/reserveA']-data['GME-USD'])/data['GME-USD']).dropna().index,
                              y=((data['GME-DUSD_reserveB/reserveA']-data['GME-USD'])/data['GME-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumGOOGL = dict(type='scatter', name='dGOOGL',
                              x=((data['GOOGL-DUSD_reserveB/reserveA']-data['GOOGL-USD'])/data['GOOGL-USD']).dropna().index,
                              y=((data['GOOGL-DUSD_reserveB/reserveA']-data['GOOGL-USD'])/data['GOOGL-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumNVDA = dict(type='scatter', name='dNVDA',
                              x=((data['NVDA-DUSD_reserveB/reserveA']-data['NVDA-USD'])/data['NVDA-USD']).dropna().index,
                              y=((data['NVDA-DUSD_reserveB/reserveA']-data['NVDA-USD'])/data['NVDA-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumPDBC = dict(type='scatter', name='dPDBC',
                              x=((data['PDBC-DUSD_reserveB/reserveA']-data['PDBC-USD'])/data['PDBC-USD']).dropna().index,
                              y=((data['PDBC-DUSD_reserveB/reserveA']-data['PDBC-USD'])/data['PDBC-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumPLTR = dict(type='scatter', name='dPLTR',
                              x=((data['PLTR-DUSD_reserveB/reserveA']-data['PLTR-USD'])/data['PLTR-USD']).dropna().index,
                              y=((data['PLTR-DUSD_reserveB/reserveA']-data['PLTR-USD'])/data['PLTR-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumQQQ = dict(type='scatter', name='dQQQ',
                              x=((data['QQQ-DUSD_reserveB/reserveA']-data['QQQ-USD'])/data['QQQ-USD']).dropna().index,
                              y=((data['QQQ-DUSD_reserveB/reserveA']-data['QQQ-USD'])/data['QQQ-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumSLV = dict(type='scatter', name='dSLV',
                              x=((data['SLV-DUSD_reserveB/reserveA']-data['SLV-USD'])/data['SLV-USD']).dropna().index,
                              y=((data['SLV-DUSD_reserveB/reserveA']-data['SLV-USD'])/data['SLV-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumSPY = dict(type='scatter', name='dSPY',
                              x=((data['SPY-DUSD_reserveB/reserveA']-data['SPY-USD'])/data['SPY-USD']).dropna().index,
                              y=((data['SPY-DUSD_reserveB/reserveA']-data['SPY-USD'])/data['SPY-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumTLT = dict(type='scatter', name='dTLT',
                              x=((data['TLT-DUSD_reserveB/reserveA']-data['TLT-USD'])/data['TLT-USD']).dropna().index,
                              y=((data['TLT-DUSD_reserveB/reserveA']-data['TLT-USD'])/data['TLT-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumTSLA = dict(type='scatter', name='dTSLA',
                              x=((data['TSLA-DUSD_reserveB/reserveA']-data['TSLA-USD'])/data['TSLA-USD']).dropna().index,
                              y=((data['TSLA-DUSD_reserveB/reserveA']-data['TSLA-USD'])/data['TSLA-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumURTH = dict(type='scatter', name='dURTH',
                              x=((data['URTH-DUSD_reserveB/reserveA']-data['URTH-USD'])/data['URTH-USD']).dropna().index,
                              y=((data['URTH-DUSD_reserveB/reserveA']-data['URTH-USD'])/data['URTH-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumVNQ = dict(type='scatter', name='dVNQ',
                              x=((data['VNQ-DUSD_reserveB/reserveA']-data['VNQ-USD'])/data['VNQ-USD']).dropna().index,
                              y=((data['VNQ-DUSD_reserveB/reserveA']-data['VNQ-USD'])/data['VNQ-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        figPrices.add_trace(trace_premiumDUSD, 1, 1)
        figPrices.add_trace(trace_premiumAAPL, 1, 1)
        figPrices.add_trace(trace_premiumAMZN, 1, 1)
        figPrices.add_trace(trace_premiumARKK, 1, 1)
        figPrices.add_trace(trace_premiumBABA, 1, 1)
        figPrices.add_trace(trace_premiumCOIN, 1, 1)
        figPrices.add_trace(trace_premiumEEM, 1, 1)
        figPrices.add_trace(trace_premiumGLD, 1, 1)
        figPrices.add_trace(trace_premiumGME, 1, 1)
        figPrices.add_trace(trace_premiumGOOGL, 1, 1)
        figPrices.add_trace(trace_premiumNVDA, 1, 1)
        figPrices.add_trace(trace_premiumPDBC, 1, 1)
        figPrices.add_trace(trace_premiumPLTR, 1, 1)
        figPrices.add_trace(trace_premiumQQQ, 1, 1)
        figPrices.add_trace(trace_premiumSLV, 1, 1)
        figPrices.add_trace(trace_premiumSPY, 1, 1)
        figPrices.add_trace(trace_premiumTLT, 1, 1)
        figPrices.add_trace(trace_premiumTSLA, 1, 1)
        figPrices.add_trace(trace_premiumURTH, 1, 1)
        figPrices.add_trace(trace_premiumVNQ, 1, 1)



        figPrices.update_yaxes(title_text='Premium in %', gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1, range=[-20, 60])
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
    def getPremiumExplanation():
        dTokenPricesCardExplanation = [html.P(['The dToken prices on DefiChain are determined by the corresponding pool ratio and may differ from the current oracle price. '
                                               'The premium is the relative deviation between the DEX and oracle price. It shows you if people are more buying (positive premium) or '
                                               'selling the decentralized asset.'], style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return dTokenPricesCardExplanation