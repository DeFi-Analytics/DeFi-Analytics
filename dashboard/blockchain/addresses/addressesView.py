import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


import time

class addressesViewClass:
    def __init__(self):
        None

    def getAddressContent(self, data):
        content = [dbc.Card(dbc.CardBody([dcc.Graph(figure=self.createAddressesFigure(data),config={'displayModeBar': False})])),
                   dbc.Card(dbc.CardBody(self.getAddressExplanation()),style={'margin-top': '1.0rem'})]
        return content

    def createAddressesFigure(self, data):
        figAddress = make_subplots(
            rows=3, cols=1,
            vertical_spacing=0.15,
            row_width=[0.10, 0.35, 0.55],  # from bottom to top
            specs=[[{}],
                   [{}],
                   [{}]],
            shared_xaxes=True,
            subplot_titles=(['Overall', 'Specific', 'Genesis Masternodes']))
        figAddress.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figAddress.layout.annotations[0].font.size = 20
        figAddress.layout.annotations[1].font.color = '#6c757d'
        figAddress.layout.annotations[1].font.size = 20
        figAddress.layout.annotations[2].font.color = '#6c757d'
        figAddress.layout.annotations[2].font.size = 20

        # generate over addresses
        trace_AllAddresses = dict(type='scatter', name='Overall', x=data.index, y=data['nbOverall'].dropna(),
                                  mode='lines', line=dict(color='#8097ee'), line_width=3, marker_size=8,
                                  hovertemplate='%{y:.f}')
        figAddress.add_trace(trace_AllAddresses, 1, 1)
        figAddress.update_yaxes(title_text='Addresses', tickformat=".f", gridcolor='#6c757d', color='#6c757d',
                                zerolinecolor='#6c757d', row=1, col=1)

        # generate specific addresses
        trace_mnAddresses = dict(type='scatter', name='Full Masternodes',x=data.index, y=data['nbMnId'].dropna() - data['nbMnGenesisId'].dropna(),
                                 mode='lines', line=dict(color='#da3832'), line_width=3, marker_size=8,
                                 hovertemplate='%{y:.f}')
        figAddress.add_trace(trace_mnAddresses, 2, 1)

        trace_otherAddresses = dict(type='scatter', name='Other', x=data.index, y=data['nbOtherId'].dropna(),
                                    mode='lines', line=dict(color='#7f50ff'), line_width=3, marker_size=8,
                                    hovertemplate='%{y:.f}')
        figAddress.add_trace(trace_otherAddresses, 2, 1)
        figAddress.update_yaxes(title_text='Addresses', tickformat=".f", gridcolor='#6c757d', color='#6c757d',
                                zerolinecolor='#6c757d', row=2, col=1)

        # generate genesis masternodes
        trace_mnGenesisAddresses = dict(type='scatter', name='Genesis Masternodes', x=data.index, y=data['nbMnGenesisId'].dropna(),
                                        mode='lines', line=dict(color='#ff00af'), line_width=3, marker_size=8,
                                        hovertemplate='%{y:.f}')
        figAddress.add_trace(trace_mnGenesisAddresses, 3, 1)
        figAddress.update_yaxes(title_text='Addresses', tickformat=".f", gridcolor='#6c757d', color='#6c757d',
                                zerolinecolor='#6c757d', row=3, col=1)

        figAddress.update_xaxes(color='#6c757d', gridcolor='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figAddress.update_xaxes(color='#6c757d', gridcolor='#6c757d', zerolinecolor='#6c757d', row=2, col=1)
        figAddress.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', row=3,
                                col=1)

        figAddress.update_layout(height=850,
                                 margin={"t": 70, "l": 130, "b": 20},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d"),
                                 legend=dict(orientation="h",
                                             yanchor="bottom",
                                             y=-0.25,
                                             xanchor="right",
                                             x=1),
                                 )
        figAddress.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figAddress.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figAddress.layout.legend.font.color = '#6c757d'  # font color legend
        return figAddress

    def getAddressExplanation(self):
        addressCardExplanation = [html.H4("Info Addresses"),
                                  html.P([
                                            'For tracking the number of addresses a snapshot of the DeFiChain richlist is made once a day (in the night).',
                                             html.Br(),
                                             html.A('http://explorer.defichain.io/#/DFI/mainnet/rich-list',
                                                    href='http://explorer.defichain.io/#/DFI/mainnet/rich-list',
                                                    target='_blank')]),
                                  html.P(
                                            'The first diagram shows the overall number of addresses with a DFI amount greater zero.'),
                                  html.P([
                                             'The second diagram shows the number of masternodes and all other addresses. Currently there is no API-function'
                                             ' for identifying masternodes, so the DFI-amount deposited on the address is used. The needed range for a masternode is between '
                                             '1 and 1.2 million DFI'], style={'text-align': 'justify'}),
                                  html.P([
                                             'The last graphic shows the genesis masternode number. The DefiChain started with 3 genesis masternodes, which do not need'
                                             ' the the amount of 1 million DFI. Sometimes a genesis node is not represented in the snapshot, because on the corresponding address there are no DFI.'
                                             ' In this case the masternode is not listed on the Richlist.'],
                                         style={'text-align': 'justify'}),
                                  html.P([html.B('Hint:'),
                                          ' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                          ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                         style={'text-align': 'justify', 'fontSize': '0.7rem', 'color': '#6c757d'})
                                  ]
        return addressCardExplanation
