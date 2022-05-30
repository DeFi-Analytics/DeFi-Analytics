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

        trace_premiumDUSD = dict(type='scatter', name='dUSD',
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

        trace_premiumBRK = dict(type='scatter', name='dBRK.B',
                              x=((data['BRK.B-DUSD_reserveB/reserveA']-data['BRK.B-USD'])/data['BRK.B-USD']).dropna().index,
                              y=((data['BRK.B-DUSD_reserveB/reserveA']-data['BRK.B-USD'])/data['BRK.B-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumCOIN = dict(type='scatter', name='dCOIN',
                              x=((data['COIN-DUSD_reserveB/reserveA']-data['COIN-USD'])/data['COIN-USD']).dropna().index,
                              y=((data['COIN-DUSD_reserveB/reserveA']-data['COIN-USD'])/data['COIN-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumCS = dict(type='scatter', name='dCS',
                              x=((data['CS-DUSD_reserveB/reserveA']-data['CS-USD'])/data['CS-USD']).dropna().index,
                              y=((data['CS-DUSD_reserveB/reserveA']-data['CS-USD'])/data['CS-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumDIS = dict(type='scatter', name='dDIS',
                              x=((data['DIS-DUSD_reserveB/reserveA']-data['DIS-USD'])/data['DIS-USD']).dropna().index,
                              y=((data['DIS-DUSD_reserveB/reserveA']-data['DIS-USD'])/data['DIS-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumEEM = dict(type='scatter', name='dEEM',
                              x=((data['EEM-DUSD_reserveB/reserveA']-data['EEM-USD'])/data['EEM-USD']).dropna().index,
                              y=((data['EEM-DUSD_reserveB/reserveA']-data['EEM-USD'])/data['EEM-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumFB = dict(type='scatter', name='dFB',
                              x=((data['FB-DUSD_reserveB/reserveA']-data['FB-USD'])/data['FB-USD']).dropna().index,
                              y=((data['FB-DUSD_reserveB/reserveA']-data['FB-USD'])/data['FB-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumGLD = dict(type='scatter', name='dGLD',
                              x=((data['GLD-DUSD_reserveB/reserveA']-data['GLD-USD'])/data['GLD-USD']).dropna().index,
                              y=((data['GLD-DUSD_reserveB/reserveA']-data['GLD-USD'])/data['GLD-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumGME = dict(type='scatter', name='dGME',
                              x=((data['GME-DUSD_reserveB/reserveA']-data['GME-USD'])/data['GME-USD']).dropna().index,
                              y=((data['GME-DUSD_reserveB/reserveA']-data['GME-USD'])/data['GME-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumGOOGL = dict(type='scatter', name='dGOOGL',
                              x=((data['GOOGL-DUSD_reserveB/reserveA']-data['GOOGL-USD'])/data['GOOGL-USD']).dropna().index,
                              y=((data['GOOGL-DUSD_reserveB/reserveA']-data['GOOGL-USD'])/data['GOOGL-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumGSG = dict(type='scatter', name='dGSG',
                              x=((data['GSG-DUSD_reserveB/reserveA']-data['GSG-USD'])/data['GSG-USD']).dropna().index,
                              y=((data['GSG-DUSD_reserveB/reserveA']-data['GSG-USD'])/data['GSG-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumINTC = dict(type='scatter', name='dINTC',
                              x=((data['INTC-DUSD_reserveB/reserveA']-data['INTC-USD'])/data['INTC-USD']).dropna().index,
                              y=((data['INTC-DUSD_reserveB/reserveA']-data['INTC-USD'])/data['INTC-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumKO = dict(type='scatter', name='dKO',
                              x=((data['KO-DUSD_reserveB/reserveA']-data['KO-USD'])/data['KO-USD']).dropna().index,
                              y=((data['KO-DUSD_reserveB/reserveA']-data['KO-USD'])/data['KO-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumMCHI = dict(type='scatter', name='dMCHI',
                              x=((data['MCHI-DUSD_reserveB/reserveA']-data['MCHI-USD'])/data['MCHI-USD']).dropna().index,
                              y=((data['MCHI-DUSD_reserveB/reserveA']-data['MCHI-USD'])/data['MCHI-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumMSFT = dict(type='scatter', name='dMSFT',
                              x=((data['MSFT-DUSD_reserveB/reserveA']-data['MSFT-USD'])/data['MSFT-USD']).dropna().index,
                              y=((data['MSFT-DUSD_reserveB/reserveA']-data['MSFT-USD'])/data['MSFT-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumMSTR = dict(type='scatter', name='dMSTR',
                              x=((data['MSTR-DUSD_reserveB/reserveA']-data['MSTR-USD'])/data['MSTR-USD']).dropna().index,
                              y=((data['MSTR-DUSD_reserveB/reserveA']-data['MSTR-USD'])/data['MSTR-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumNFLX = dict(type='scatter', name='dNFLX',
                              x=((data['NFLX-DUSD_reserveB/reserveA']-data['NFLX-USD'])/data['NFLX-USD']).dropna().index,
                              y=((data['NFLX-DUSD_reserveB/reserveA']-data['NFLX-USD'])/data['NFLX-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumNVDA = dict(type='scatter', name='dNVDA',
                              x=((data['NVDA-DUSD_reserveB/reserveA']-data['NVDA-USD'])/data['NVDA-USD']).dropna().index,
                              y=((data['NVDA-DUSD_reserveB/reserveA']-data['NVDA-USD'])/data['NVDA-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumPDBC = dict(type='scatter', name='dPDBC',
                              x=((data['PDBC-DUSD_reserveB/reserveA']-data['PDBC-USD'])/data['PDBC-USD']).dropna().index,
                              y=((data['PDBC-DUSD_reserveB/reserveA']-data['PDBC-USD'])/data['PDBC-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumPG = dict(type='scatter', name='dPG',
                              x=((data['PG-DUSD_reserveB/reserveA']-data['PG-USD'])/data['PG-USD']).dropna().index,
                              y=((data['PG-DUSD_reserveB/reserveA']-data['PG-USD'])/data['PG-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumPLTR = dict(type='scatter', name='dPLTR',
                              x=((data['PLTR-DUSD_reserveB/reserveA']-data['PLTR-USD'])/data['PLTR-USD']).dropna().index,
                              y=((data['PLTR-DUSD_reserveB/reserveA']-data['PLTR-USD'])/data['PLTR-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumPYPL = dict(type='scatter', name='dPYPL',
                              x=((data['PYPL-DUSD_reserveB/reserveA']-data['PYPL-USD'])/data['PYPL-USD']).dropna().index,
                              y=((data['PYPL-DUSD_reserveB/reserveA']-data['PYPL-USD'])/data['PYPL-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumQQQ = dict(type='scatter', name='dQQQ',
                              x=((data['QQQ-DUSD_reserveB/reserveA']-data['QQQ-USD'])/data['QQQ-USD']).dropna().index,
                              y=((data['QQQ-DUSD_reserveB/reserveA']-data['QQQ-USD'])/data['QQQ-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumSAP = dict(type='scatter', name='dSAP',
                              x=((data['SAP-DUSD_reserveB/reserveA']-data['SAP-USD'])/data['SAP-USD']).dropna().index,
                              y=((data['SAP-DUSD_reserveB/reserveA']-data['SAP-USD'])/data['SAP-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

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

        trace_premiumURA = dict(type='scatter', name='dURA',
                              x=((data['URA-DUSD_reserveB/reserveA']-data['URA-USD'])/data['URA-USD']).dropna().index,
                              y=((data['URA-DUSD_reserveB/reserveA']-data['URA-USD'])/data['URA-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumURTH = dict(type='scatter', name='dURTH',
                              x=((data['URTH-DUSD_reserveB/reserveA']-data['URTH-USD'])/data['URTH-USD']).dropna().index,
                              y=((data['URTH-DUSD_reserveB/reserveA']-data['URTH-USD'])/data['URTH-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumVNQ = dict(type='scatter', name='dVNQ',
                              x=((data['VNQ-DUSD_reserveB/reserveA']-data['VNQ-USD'])/data['VNQ-USD']).dropna().index,
                              y=((data['VNQ-DUSD_reserveB/reserveA']-data['VNQ-USD'])/data['VNQ-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        trace_premiumVOO = dict(type='scatter', name='dVOO',
                              x=((data['VOO-DUSD_reserveB/reserveA']-data['VOO-USD'])/data['VOO-USD']).dropna().index,
                              y=((data['VOO-DUSD_reserveB/reserveA']-data['VOO-USD'])/data['VOO-USD']).dropna()*100, mode='lines', line_width=2 , hovertemplate=hoverNumber)

        figPrices.add_trace(trace_premiumDUSD, 1, 1)
        figPrices.add_trace(trace_premiumAAPL, 1, 1)
        figPrices.add_trace(trace_premiumAMZN, 1, 1)
        figPrices.add_trace(trace_premiumARKK, 1, 1)
        figPrices.add_trace(trace_premiumBABA, 1, 1)
        figPrices.add_trace(trace_premiumBRK, 1, 1)
        figPrices.add_trace(trace_premiumCOIN, 1, 1)
        figPrices.add_trace(trace_premiumCS, 1, 1)
        figPrices.add_trace(trace_premiumDIS, 1, 1)
        figPrices.add_trace(trace_premiumEEM, 1, 1)
        figPrices.add_trace(trace_premiumFB, 1, 1)
        figPrices.add_trace(trace_premiumGLD, 1, 1)
        figPrices.add_trace(trace_premiumGSG, 1, 1)
        figPrices.add_trace(trace_premiumGME, 1, 1)
        figPrices.add_trace(trace_premiumGOOGL, 1, 1)
        figPrices.add_trace(trace_premiumINTC, 1, 1)
        figPrices.add_trace(trace_premiumKO, 1, 1)
        figPrices.add_trace(trace_premiumMCHI, 1, 1)
        figPrices.add_trace(trace_premiumMSFT, 1, 1)
        figPrices.add_trace(trace_premiumMSTR, 1, 1)
        figPrices.add_trace(trace_premiumNFLX, 1, 1)
        figPrices.add_trace(trace_premiumNVDA, 1, 1)
        figPrices.add_trace(trace_premiumPDBC, 1, 1)
        figPrices.add_trace(trace_premiumPG, 1, 1)
        figPrices.add_trace(trace_premiumPLTR, 1, 1)
        figPrices.add_trace(trace_premiumPYPL, 1, 1)
        figPrices.add_trace(trace_premiumQQQ, 1, 1)
        figPrices.add_trace(trace_premiumSAP, 1, 1)
        figPrices.add_trace(trace_premiumSLV, 1, 1)
        figPrices.add_trace(trace_premiumSPY, 1, 1)
        figPrices.add_trace(trace_premiumTLT, 1, 1)
        figPrices.add_trace(trace_premiumTSLA, 1, 1)
        figPrices.add_trace(trace_premiumURA, 1, 1)
        figPrices.add_trace(trace_premiumURTH, 1, 1)
        figPrices.add_trace(trace_premiumVNQ, 1, 1)
        figPrices.add_trace(trace_premiumVOO, 1, 1)


        figPrices.update_yaxes(title_text='Premium in %', gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1, range=[-17, 17])
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