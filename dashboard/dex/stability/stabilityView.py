import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
import numpy as np


class stabilityViewClass:
    def getStabilityContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info price stability DEX"),
                              dbc.ModalBody(self.getStabilityExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoStability", className="ml-auto"))], id="modalStability", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Price stability on DEX']),
                                          html.Table([html.Tr([html.Td('Select pool for price stability calculation:'),
                                          html.Td(dcc.Dropdown(id='stabilityPoolSelection', options=[
                                              {'label': 'BTC', 'value': 'BTC-DFI'},
                                              {'label': 'ETH', 'value': 'ETH-DFI'},
                                              {'label': 'USDT', 'value': 'USDT-DFI'},
                                              {'label': 'DOGE', 'value': 'DOGE-DFI'},
                                              {'label': 'LTC', 'value': 'LTC-DFI'},
                                              {'label': 'BCH', 'value': 'BCH-DFI'},
                                              {'label': 'USDC', 'value': 'USDC-DFI'},
                                              {'label': 'csETH', 'value': 'csETH-ETH'},
                                              {'label': 'dUSD-DFI', 'value': 'DUSD-DFI'},
                                              {'label': 'dUSD-dUSDT', 'value': 'USDT-DUSD'},
                                              {'label': 'dUSD-dUSDC', 'value': 'USDC-DUSD'},
                                              {'label': 'AAPL', 'value': 'AAPL-DUSD'},
                                              {'label': 'ADDYY', 'value': 'ADDYY-DUSD'},
                                              {'label': 'AMZN', 'value': 'AMZN-DUSD'},
                                              {'label': 'ARKK', 'value': 'ARKK-DUSD'},
                                              {'label': 'ARKX', 'value': 'ARKX-DUSD'},
                                              {'label': 'BABA', 'value': 'BABA-DUSD'},
                                              {'label': 'BRK.B', 'value': 'BRK.B-DUSD'},
                                              {'label': 'COIN', 'value': 'COIN-DUSD'},
                                              {'label': 'CS', 'value': 'CS-DUSD'},
                                              {'label': 'DAX', 'value': 'DAX-DUSD'},
                                              {'label': 'DIS', 'value': 'DIS-DUSD'},
                                              {'label': 'EEM', 'value': 'EEM-DUSD'},
                                              {'label': 'FB', 'value': 'FB-DUSD'},
                                              {'label': 'GLD', 'value': 'GLD-DUSD'},
                                              {'label': 'GME', 'value': 'GME-DUSD'},
                                              {'label': 'GS', 'value': 'GS-DUSD'},
                                              {'label': 'GSG', 'value': 'GSG-DUSD'},
                                              {'label': 'GOOGL', 'value': 'GOOGL-DUSD'},
                                              {'label': 'GOVT', 'value': 'GOVT-DUSD'},
                                              {'label': 'INTC', 'value': 'INTC-DUSD'},
                                              {'label': 'JNJ', 'value': 'JNJ-DUSD'},
                                              {'label': 'KO', 'value': 'KO-DUSD'},
                                              {'label': 'MCHI', 'value': 'MCHI-DUSD'},
                                              {'label': 'MSFT', 'value': 'MSFT-DUSD'},
                                              {'label': 'MSTR', 'value': 'MSTR-DUSD'},
                                              {'label': 'NFLX', 'value': 'NFLX-DUSD'},
                                              {'label': 'NVDA', 'value': 'NVDA-DUSD'},
                                              {'label': 'PDBC', 'value': 'PDBC-DUSD'},
                                              {'label': 'PG', 'value': 'PG-DUSD'},
                                              {'label': 'PLTR', 'value': 'PLTR-DUSD'},
                                              {'label': 'PPLT', 'value': 'PPLT-DUSD'},
                                              {'label': 'PYPL', 'value': 'PYPL-DUSD'},
                                              {'label': 'QQQ', 'value': 'QQQ-DUSD'},
                                              {'label': 'SAP', 'value': 'SAP-DUSD'},
                                              {'label': 'SLV', 'value': 'SLV-DUSD'},
                                              {'label': 'SPY', 'value': 'SPY-DUSD'},
                                              {'label': 'TAN', 'value': 'TAN-DUSD'},
                                              {'label': 'TLT', 'value': 'TLT-DUSD'},
                                              {'label': 'TSLA', 'value': 'TSLA-DUSD'},
                                              {'label': 'UL', 'value': 'UL-DUSD'},
                                              {'label': 'UNG', 'value': 'UNG-DUSD'},
                                              {'label': 'URA', 'value': 'URA-DUSD'},
                                              {'label': 'USO', 'value': 'USO-DUSD'},
                                              {'label': 'URTH', 'value': 'URTH-DUSD'},
                                              {'label': 'VBK', 'value': 'VBK-DUSD'},
                                              {'label': 'VNQ', 'value': 'VNQ-DUSD'},
                                              {'label': 'VOO', 'value': 'VOO-DUSD'},
                                              {'label': 'WMT', 'value': 'WMT-DUSD'},
                                              {'label': 'XLE', 'value': 'XLE-DUSD'},
                                              {'label': 'XLRE', 'value': 'XLRE-DUSD'},
                                              {'label': 'XOM', 'value': 'XOM-DUSD'},
                                          ],
                                          value='BTC-DFI', clearable=False, style=dict(width='150px', verticalAlign="bottom")))])]),
                                          html.Div(['Data used for calculation: Update from ', html.Span(id='stabilityPoolLastUpdate'), ', Pool-size of ',
                                                    html.Span(id='stabilityPoolCoinA'), ' and ',
                                                    html.Span(id='stabilityPoolCoinB')], style={'margin-top': 15}),

                                          dbc.Row([dbc.Col([html.H6('Determine DFI-Change'),
                                                            html.Div(['Define the ratio/price change (in %) of the DEX pool, to get the resulting ',html.Span(id='stabilityPoolCoinBName1'),' amount to be added/removed.'], style={'margin-top': 15, 'margin-left': 0}),
                                                            html.Div(['Change [-90...+900%]: ', dcc.Input(id="stabilityChangePriceInput", type='number', debounce=True, value=10, min=-90, max=900)], style={'margin-top': 5, 'margin-left': 0}),
                                                            dcc.Graph(id='figureStabilityDFI', config={'displayModeBar': False}),
                                                            html.Div(['The needed coin amount to be added/removed: ',html.B('xy',id='stabilityChangePriceOutput', style={'color': '#ff00af'})], style={'margin-top': 5, 'margin-left': 0})],
                                                            style={'margin-top': 40}, lg=6, xl=6, align='start'),
                                                   dbc.Col([html.H6('Determine Price-Change'),
                                                            html.Div(['Define the ',html.Span(id='stabilityPoolCoinBName2'),' amount in/out of the DEX pool, to get the resulting ratio/price change in positiv/negative direction.'], style={'margin-top': 15, 'margin-left': 0}),
                                                            html.Div([html.Span(id='stabilityPoolCoinBName3'),' amount: ', dcc.Input(id="stabilityChangeDFIInput", type='number', debounce=True, value=10)], style={'margin-top': 5, 'margin-left': 0}),
                                                            dcc.Graph(id='figureStabilityPrice', config={'displayModeBar': False}),
                                                            html.Div(['The resulting price change is: ',html.B('xy',id='stabilityChangeDFIOutput', style={'color': '#ff00af'})], style={'margin-top': 5, 'margin-left': 0})
                                                            ],style={'margin-top': 40}, lg=6, xl=6)]),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoStability")), style={'margin-top': 15})]))]
        return content

    @staticmethod
    def createStabilityDFIGraph(data, bgImage, selectedCoin, ratioChangeInput):
        figStabDFI = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        hoverTemplateRepresenation = '%{y:,.0f}'

        currDFI = data[selectedCoin+'_reserveB'].dropna().iloc[-1]
        curr2ndCoin = data[selectedCoin + '_reserveA'].dropna().iloc[-1]
        currRatio = data[selectedCoin+'_reserveA/reserveB'].dropna().iloc[-1]
        currLT = np.sqrt(currDFI * curr2ndCoin)

        changeRange = np.logspace(np.log10(0.1), np.log10(10), 1000)

        if selectedCoin[selectedCoin.index('-') + 1:] == 'DFI':
            priceUnit = selectedCoin[:selectedCoin.index('-')] + '/' + selectedCoin[selectedCoin.index('-') + 1:]
            newRatio = (1 + float(ratioChangeInput) / 100) * currRatio
            newDFIamount = np.sqrt(1 / newRatio) * currLT
            ratioRange = changeRange * currRatio
            DFIRange = np.sqrt(1 / ratioRange) * currLT
        else:
            priceUnit = selectedCoin[selectedCoin.index('-') + 1:] + '/' + selectedCoin[:selectedCoin.index('-')]
            newRatio = currRatio / (1 + float(ratioChangeInput) / 100)
            newDFIamount = np.sqrt(1 / newRatio) * currLT
            ratioRange = changeRange / currRatio
            DFIRange = np.sqrt(ratioRange) * currLT


        neededDFI = newDFIamount - currDFI

        traceCurve = dict(type='scatter', name='Amount', x=(changeRange-1)*100, y=DFIRange-currDFI,
                                mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate=hoverTemplateRepresenation)

        tracePoint = dict(type='scatter', name='Selected change', x=[float(ratioChangeInput)], y=[neededDFI],marker_line_color="#030a65",marker_line_width=2,
                                mode='markers', marker=dict(color="#7f50ff", size=12), marker_symbol='diamond', hovertemplate=hoverTemplateRepresenation)

        figStabDFI.add_trace(traceCurve, 1, 1)
        figStabDFI.add_trace(tracePoint, 1, 1)

        figStabDFI.update_yaxes(title_text=selectedCoin[selectedCoin.index('-')+1:]+' amount', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                               zerolinecolor='#6c757d', row=1, col=1)
        figStabDFI.update_xaxes(title_text=priceUnit+" change in %", gridcolor='#6c757d', #range=[date14DaysBack.strftime('%Y-%m-%d'), lastValidDate],
                               showticklabels=True, color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)



        #add background picture
        figStabDFI.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figStabDFI.update_layout(margin={"t": 30, "l": 0, "b": 0, 'r': 0},
                                hovermode='x unified',
                                hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                showlegend=False
                                )
        figStabDFI.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figStabDFI.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figStabDFI.layout.legend.font.color = '#6c757d'  # font color legend
        return figStabDFI, neededDFI

    @staticmethod
    def createDFIRatioGraph(data, bgImage, selectedCoin, userChangeDFI):
        figRatioDFI = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        hoverTemplateRepresenation = '%{y:,.1f}%'
        currDFI = data[selectedCoin+'_reserveB'].dropna().iloc[-1]
        curr2ndCoin = data[selectedCoin + '_reserveA'].dropna().iloc[-1]
        currRatio = data[selectedCoin+'_reserveA/reserveB'].dropna().iloc[-1]
        currLT = np.sqrt(currDFI * curr2ndCoin)

        changeDFI = np.linspace(-currDFI*0.5, 2*currDFI, 1000)
        newDFIamount = currDFI+float(userChangeDFI)

        if selectedCoin[selectedCoin.index('-') + 1:] == 'DFI':
            priceUnit = selectedCoin[:selectedCoin.index('-')] + '/' + selectedCoin[selectedCoin.index('-') + 1:]
            resultingRatioChange = ((currLT ** 2) / (newDFIamount ** 2)  - currRatio) / currRatio * 100
            ratioChange = (currLT ** 2 / ((currDFI + changeDFI) ** 2) - currRatio) / currRatio * 100
        else: # for dToken the price must be in the other ratio
            priceUnit = selectedCoin[selectedCoin.index('-') + 1:] + '/' + selectedCoin[:selectedCoin.index('-')]
            resultingRatioChange = ((newDFIamount ** 2) / (currLT ** 2) - 1/currRatio) / (1/currRatio) * 100
            ratioChange = (((currDFI + changeDFI) ** 2) / currLT ** 2 - 1/currRatio) / (1/currRatio) * 100


        traceCurve = dict(type='scatter', name='Change', x=changeDFI, y=ratioChange,
                                mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate=hoverTemplateRepresenation)

        tracePoint = dict(type='scatter', name='Selected change', x=[float(userChangeDFI)], y=[resultingRatioChange],marker_line_color="#030a65",marker_line_width=2,
                                mode='markers', marker=dict(color="#7f50ff", size=12), marker_symbol='diamond', hovertemplate=hoverTemplateRepresenation)

        figRatioDFI.add_trace(traceCurve, 1, 1)
        figRatioDFI.add_trace(tracePoint, 1, 1)

        figRatioDFI.update_yaxes(title_text=priceUnit+' change in %', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                               zerolinecolor='#6c757d', row=1, col=1)
        figRatioDFI.update_xaxes(title_text=selectedCoin[selectedCoin.index('-')+1:]+" amount", gridcolor='#6c757d', #range=[date14DaysBack.strftime('%Y-%m-%d'), lastValidDate],
                               showticklabels=True, color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)



        #add background picture
        figRatioDFI.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figRatioDFI.update_layout(margin={"t": 30, "l": 0, "b": 0, 'r': 0},
                                hovermode='x unified',
                                hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                showlegend=False
                                )
        figRatioDFI.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figRatioDFI.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figRatioDFI.layout.legend.font.color = '#6c757d'  # font color legend
        return figRatioDFI, resultingRatioChange



    @staticmethod
    def getStabilityExplanation():
        stabilityCardExplanation = [html.P(['The DEX has no external price information of the coin pairs. The current pool ratio just represents the price and can only be changed via '
                                            'swaps on the DEX. If there is a difference to external exchanges arbitrage traders uses the opportunity to make profit while buying low or selling high on DEX.'],style={'text-align': 'justify'}),
                                    html.P(['Chaging the ratio means, you have to remove or add a certain amount of coins, for bigger pools more and smaller pools less. This effect '
                                            'is evaluated here. The user can choose 2 different ways of calculation: ', html.Br(),
                                            html.Ul([html.Li('Use the expected change in ratio/price as an input and determine the needed DFI coins to be added/removed'),
                                                     html.Li('Use the amount of DFI to be added/removed and determine the new ratio/price')],
                                                    style={'text-align': 'justify'})], style={'text-align': 'justify'}),
                                    html.P(['Due to the big BTC-pool, the DEX stabilizes the DFI price on Bitcoin. A movement in this ration means swaping a lot of DFI.']),
                                    html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                                  ]
        return stabilityCardExplanation