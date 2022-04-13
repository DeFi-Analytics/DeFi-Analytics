import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots

class addressesViewClass:
    def __init__(self):
        None

    def getAddressContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info Addresses"),
                              dbc.ModalBody(self.getAddressExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoAddresses", className="ml-auto"))],
                                    id="modalAddresses", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Addresses holding DFI']),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createAddressesFigure(data, bgImage), config={'displayModeBar': False}, id='figureAddressesDFI'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoAddresses")))
                                          ]))]
        return content

    @staticmethod
    def createAddressesFigure(data, bgImage):
        figAddress = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        # generate over addresses
        trace_AllAddresses = dict(type='scatter', name='Overall', x=data['nbOverall'].dropna().index, y=data['nbOverall'].dropna(),
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:,.f}')

        # generate specific addresses
        trace_mnAddresses = dict(type='scatter', name='Masternodes',x=data['nbMnGenesisId'].dropna().index, y=(data['nbMnId'] - data['nbMnGenesisId']).dropna(),
                                 mode='lines', line=dict(color='#ff7fd7'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f}', fill='tozeroy')

        trace_otherAddresses = dict(type='scatter', name='Non-Masternodes', x=data['nbOtherId'].dropna().index, y=data['nbOtherId'].dropna(),
                                    mode='lines', line=dict(color='#ffbfeb'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f}', fill='tonexty')

        figAddress.add_trace(trace_mnAddresses, 1, 1)
        figAddress.add_trace(trace_otherAddresses, 1, 1)
        figAddress.add_trace(trace_AllAddresses, 1, 1)

        figAddress.update_yaxes(title_text='Number addresses', tickformat=",.f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figAddress.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', row=1, col=1)

        figAddress.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))



        figAddress.update_layout(margin={"t": 20, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d"),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figAddress.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figAddress.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figAddress.layout.legend.font.color = '#6c757d'  # font color legend
        return figAddress

    @staticmethod
    def getAddressExplanation():
        addressCardExplanation = [html.P(['For tracking the number of addresses a snapshot of the DeFiChain richlist is made once a day (in the night).',
                                             html.Br(),
                                             html.A('http://explorer.defichain.io/#/DFI/mainnet/rich-list', href='http://explorer.defichain.io/#/DFI/mainnet/rich-list', target='_blank', className='defiLink')]),

                                  html.P(['For identification of the masternodes the listmasternodes() command is used, which is provided by API of Bernd Mack. ',
                                            html.Br(),
                                            html.A('http://api.mydefichain.com/v1/listmasternodes/?state=ENABLED', href='http://api.mydefichain.com/v1/listmasternodes/?state=ENABLED', target='_blank', className='defiLink'),
                                 ], style={'text-align': 'justify'}),
                                  html.P([html.B('Hint:'),
                                          ' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                          ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                         style={'text-align': 'justify', 'fontSize': '0.7rem', 'color': '#6c757d'})
                                  ]
        return addressCardExplanation
