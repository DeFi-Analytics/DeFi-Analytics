import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import plotly.graph_objects as go


class coinsAddressesViewClass:

    def getCoinsAddressesContent(self, data):
        content = [dbc.Modal([dbc.ModalHeader("Info Coins/Addresses"),
                          dbc.ModalBody(self.getCoinAddressExplanation(data)),
                          dbc.ModalFooter(dbc.Button("close", id="closeInfoCoinsAddresses", className="ml-auto"))],
                         id="modalCoinsAddresses", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Distribution of coins to addresses']),
                                          dbc.Row(dbc.Col([dcc.Graph(config={'displayModeBar': False}, id='figureCoinsAddresses'),
                                                       html.Div(['Select DFI-range of interest.'], style={'margin-top': 10, 'margin-left': 20}),
                                                       html.Div(['Minimum: ', dcc.Input(id="minDFIValueInput", type="number", debounce=True, value=0, min=0, max=4000000, step=100, )], style={'margin-top': 5, 'margin-left': 20}),
                                                       html.Div(['Maximum: ', dcc.Input(id="maxDFIValueInput", type="number", debounce=True, value=4000000, min=0, max=4000000, step=100, )], style={'margin-top': 5, 'margin-left': 20}),
                                                       html.Div(dcc.RangeSlider(id='DFIAddSlider', min=0, max=4000000, step=100, value=[0, 4000000]), style={'margin-left': 20, 'margin-right': 20, 'margin-top': 10, }), html.Div(id='DFIAddSliderOutput')
                                                       ])),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoCoinsAddresses")))]))]
        return content

    @staticmethod
    def getCoinAddressFigure(data, minDFI, maxDFI, bgImage):
        figDFIDist = go.Figure()

        condXValues = (data.balance >= minDFI) & (data.balance <= maxDFI)
        xValues = data[condXValues].balance
        stepSize = (maxDFI - minDFI) / 50

        trace_DFIDist = dict(type='histogram', name='Current distribution', x=xValues, xbins=dict(start=minDFI - stepSize / 2, end=maxDFI + stepSize / 2, size=stepSize), autobinx=False)  # 8097ee
        figDFIDist.add_trace(trace_DFIDist)

        figDFIDist.update_yaxes(title_text='# addresses', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d')

        figDFIDist.update_xaxes(title_text="DFI deposited", tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', range=[0, maxDFI])

        # add background picture
        figDFIDist.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figDFIDist.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                 legend=dict(orientation="h",
                                             yanchor="bottom",
                                             y=-0.15,
                                             xanchor="right",
                                             x=1),
                                 bargroupgap=0.1
                                 )

        figDFIDist.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDFIDist.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDFIDist.layout.legend.font.color = '#6c757d'  # font color legend

        return figDFIDist

    @staticmethod
    def getCoinAddressExplanation(data):
        coinAddressCardExplanation = [html.P(['For distribution visualization of DFI-deposits per address a snapshot of the Richlist is used as a base.', html.Br(),
                               html.A('http://explorer.defichain.io/#/DFI/mainnet/rich-list', href='http://explorer.defichain.io/#/DFI/mainnet/rich-list', target='_blank', className='defiLink')], style={'text-align': 'justify'}),
                               html.P('From this snapshop all individual addresses are extracted. This means, that the following categories are not displayed here:', style={'text-align': 'justify'}),
                               html.Ul([html.Li('Foundation coins'),
                                        html.Li('Community fund coins')]),
                               html.P('You can select a specific range of your interest and the complete histogram is recalculated.', style={'text-align': 'justify'}),
                               html.P(['Defichain Richlist: last update ', data['date'].dt.strftime("%Y-%m-%d").values[0], ' 01:00' , html.Br(),
                                        html.A('http://explorer.defichain.io/#/DFI/mainnet/rich-list', href='http://explorer.defichain.io/#/DFI/mainnet/rich-list', target='_blank', className='defiLink')],
                                        style={'fontSize': '0.65rem', 'padding-top': '20px'})]
        return coinAddressCardExplanation