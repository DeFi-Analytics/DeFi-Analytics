import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
import numpy as np


class slippageViewClass:
    def getSlippageContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info slippage DEX"),
                              dbc.ModalBody(self.getSlippageExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoStability", className="ml-auto"))], id="modalStability", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Slippage for DEX swaps']),
                                          html.Table([html.Tr([html.Td('Select pool for your swap:'),
                                                               html.Td(dcc.Dropdown(id='slippagePoolSelection', options=[{'label': 'BTC', 'value': 'BTC'},
                                                                                              {'label': 'ETH', 'value': 'ETH'},
                                                                                              {'label': 'USDT', 'value': 'USDT'},
                                                                                              {'label': 'DOGE', 'value': 'DOGE'},
                                                                                              {'label': 'LTC', 'value': 'LTC'},
                                                                                              {'label': 'BCH', 'value': 'BCH'}],
                                                                                        value='BTC', clearable=False, style=dict(width='150px', verticalAlign="bottom")))])]),
                                          html.Div(['Data used for calculation: Update from ', html.Span(id='slippagePoolLastUpdate'), ', Pool-size of ',
                                                    html.Span(id='slippagePoolCoinA'), ' and ',
                                                    html.Span(id='slippagePoolCoinB')], style={'margin-top': 15}),
                                          html.Table([html.Tr([html.Td('Do you want to buy or sell DFI?'),
                                                               html.Td(dcc.Dropdown(id='slippageOrderSelection', options=[{'label': 'buy', 'value': 'buy'},
                                                                                                                         {'label': 'sell', 'value': 'sell'}],
                                                                                    value='buy', clearable=False, style=dict(width='150px', verticalAlign="bottom")))]),
                                                      html.Tr([html.Td('How many coins should be swapped?'),
                                                               html.Td(dcc.Input(id="slippageCoinAmount", type='number', debounce=True, value=10, min=-90, max=900))])
                                                      ],
                                                               style=dict(marginTop='30px')),
                                          dcc.Graph(figure=self.createSlippageGraph(data, bgImage, 'BTC', 'sell', 10000000), id='figureSlippage', config={'displayModeBar': False}),
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
        elif selectedPool == 'ETH':
            tickFormatYAxis = ",.5f"
            hoverTemplateRepresenation = '%{y:,.8f} ETH/DFI'
        elif selectedPool == 'DOGE':
            tickFormatYAxis = ",.2f"
            hoverTemplateRepresenation = '%{y:,.2f} DOGE/DFI'
        elif selectedPool == 'LTC':
            tickFormatYAxis = ",.4f"
            hoverTemplateRepresenation = '%{y:,.6f} LTC/DFI'
        elif selectedPool == 'BCH':
            tickFormatYAxis = ",.4f"
            hoverTemplateRepresenation = '%{y:,.6f} BCH/DFI'
        else:
            tickFormatYAxis = ",.7f"
            hoverTemplateRepresenation = '%{y:,.8f} BTC/DFI'

        currDFI = data[selectedPool+'-DFI_reserveB'].dropna().iloc[-1]
        currRatio = data[selectedPool+'-DFI_reserveA/reserveB'].dropna().iloc[-1]
        currLT = data[selectedPool+'-DFI_totalLiquidity'].dropna().iloc[-1]

        amountRange = np.linspace(0, coinAmount*2.5, 1000)
        priceRange = currLT**2/((currDFI+amountRange)**2)


        traceCurve = dict(type='scatter', name='DFI amount', x=amountRange, y=priceRange,
                                mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate=hoverTemplateRepresenation)

        # tracePoint = dict(type='scatter', name='Selected change', x=[float(ratioChangeInput)], y=[neededDFI],marker_line_color="#030a65",marker_line_width=2,
        #                         mode='markers', marker=dict(color="#7f50ff", size=12), marker_symbol='diamond', hovertemplate=hoverTemplateRepresenation)

        figSlippage.add_trace(traceCurve, 1, 1)
        # figStabDFI.add_trace(tracePoint, 1, 1)

        figSlippage.update_yaxes(title_text='DFI amount', tickformat=tickFormatYAxis, gridcolor='#6c757d', color='#6c757d',
                               zerolinecolor='#6c757d', row=1, col=1)
        figSlippage.update_xaxes(title_text="Price/ratio change", gridcolor='#6c757d', #range=[date14DaysBack.strftime('%Y-%m-%d'), lastValidDate],
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
        return figSlippage


    @staticmethod
    def getSlippageExplanation():
        slippageCardExplanation = [html.P(['....']),
                                    html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                                  ]
        return slippageCardExplanation