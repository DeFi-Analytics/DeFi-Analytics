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
                   dbc.Card(dbc.CardBody([dbc.Row(dbc.Col([dcc.Graph(figure=self.getCoinAddressFigure(data, 0, 4000000), config={'displayModeBar': False}, id='figCoinsAddresses'),
                                                       html.Div(['Select DFI-range of interest.'], style={'margin-top': 10, 'margin-left': 125}),
                                                       html.Div(['Minimum: ', dcc.Input(id="minDFIValueInput", type="number", debounce=True, value=0, min=0, max=4000000, step=100, )], style={'margin-top': 5, 'margin-left': 125}),
                                                       html.Div(['Maximum: ', dcc.Input(id="maxDFIValueInput", type="number", debounce=True, value=4000000, min=0, max=4000000, step=100, )], style={'margin-top': 5, 'margin-left': 125}),
                                                       html.Div(dcc.RangeSlider(id='DFIAddSlider', min=0, max=4000000, step=100, value=[0, 4000000]), style={'margin-left': 100, 'margin-right': 50, 'margin-top': 10, }), html.Div(id='DFIAddSliderOutput')
                                                       ])),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoCoinsAddresses")))]))]
        return content

    @staticmethod
    def getCoinAddressFigure(data, minDFI, maxDFI):
        figDFIDist = go.Figure()

        condXValues = (data.balance >= minDFI) & (data.balance <= maxDFI)
        xValues = data[condXValues].balance
        stepSize = (maxDFI - minDFI) / 50

        trace_DFIDist = dict(type='histogram', name='Current distribution', x=xValues, xbins=dict(start=minDFI - stepSize / 2, end=maxDFI + stepSize / 2, size=stepSize), autobinx=False)  # 8097ee
        figDFIDist.add_trace(trace_DFIDist)

        figDFIDist.update_yaxes(title_text='# addresses', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d')

        figDFIDist.update_xaxes(title_text="DFI deposited", tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', range=[0, maxDFI])

        figDFIDist.update_layout(height=650,
                                 margin={"t": 40, "l": 130, "b": 20},
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
                               html.A('http://explorer.defichain.io/#/DFI/mainnet/rich-list', href='http://explorer.defichain.io/#/DFI/mainnet/rich-list', target='_blank')], style={'text-align': 'justify'}),
                               html.P('From this snapshop all individual addresses are extracted. This means, that the following categories are not displayed here:', style={'text-align': 'justify'}),
                               html.Ul([html.Li('Foundation coins'),
                                        html.Li('Community fund coins')]),
                               html.P('You can select a specific range of your interest and the complete histogram is recalculated.', style={'text-align': 'justify'}),
                               html.P(['Defichain Richlist: last update ', data['date'].dt.strftime("%Y-%m-%d").values[0], ' 01:00' , html.Br(),
                                        html.A('http://explorer.defichain.io/#/DFI/mainnet/rich-list', href='http://explorer.defichain.io/#/DFI/mainnet/rich-list', target='_blank')],
                                        style={'fontSize': '0.65rem', 'padding-top': '20px'})]
        return coinAddressCardExplanation