import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class volumeViewClass:
    def getVolumeContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info 24hr DEX volume"),
                              dbc.ModalBody(self.getDEXVolExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoVolume", className="ml-auto"))],
                                    id="modalVolume", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([dbc.Row(dbc.Col(dcc.Graph(figure=self.createDEXVolumeGraph(data, bgImage), config={'displayModeBar': False}))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoVolume")))
                                          ]))]
        return content

    @staticmethod
    def createDEXVolumeGraph(data, bgImage):
        figDEXVol = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=(['Trading volume (24hr) on DEX']))
        figDEXVol.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figDEXVol.layout.annotations[0].font.size = 20

        hoverTemplateRepresenation = '$%{y:,.0f}'

        trace_VolBTC = dict(type='scatter', name='BTC', x=data['BTC_VolTotal'].dropna().index, y=data['BTC_VolTotal'].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#da3832'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tozeroy')
        trace_VolETH = dict(type='scatter', name='ETH', x=data['ETH_VolTotal'].dropna().index, y=data['ETH_VolTotal'].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#617dea'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_VolUSDT = dict(type='scatter', name='USDT', x=data['USDT_VolTotal'].dropna().index, y=data['USDT_VolTotal'].dropna(), stackgroup='one',
                             mode='lines', line=dict(color='#22b852'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_VolDOGE = dict(type='scatter', name='DOGE', x=data['DOGE_VolTotal'].dropna().index, y=data['DOGE_VolTotal'].dropna(), stackgroup='one',
                             mode='lines', line=dict(color='#c2a634'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_VolLTC = dict(type='scatter', name='LTC', x=data['LTC_VolTotal'].dropna().index, y=data['LTC_VolTotal'].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#ff2ebe'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_VolBCH = dict(type='scatter', name='BCH', x=data['BCH_VolTotal'].dropna().index, y=data['BCH_VolTotal'].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#410eb2'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')

        # overall TVL graph
        trace_VolOverall = dict(type='scatter', name='Overall', x=data['VolTotal'].dropna().index, y=data['VolTotal'].dropna(),
                                mode='lines', line=dict(color='#410eb2'), line_width=3, hovertemplate=hoverTemplateRepresenation)

        figDEXVol.add_trace(trace_VolBTC, 1, 1)
        figDEXVol.add_trace(trace_VolETH, 1, 1)
        figDEXVol.add_trace(trace_VolUSDT, 1, 1)
        figDEXVol.add_trace(trace_VolDOGE, 1, 1)
        figDEXVol.add_trace(trace_VolLTC, 1, 1)
        figDEXVol.add_trace(trace_VolBCH, 1, 1)
        figDEXVol.add_trace(trace_VolOverall, 1, 1)

        figDEXVol.update_yaxes(title_text='24h volume in USD', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                               zerolinecolor='#6c757d', row=1, col=1)
        figDEXVol.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)

        # add background picture
        figDEXVol.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.4, sizey=0.4,  xanchor="center", yanchor="middle", opacity=0.2))

        figDEXVol.update_layout(height=800,
                                margin={"t": 40, "l": 130, "b": 20},
                                hovermode='x unified',
                                hoverlabel=dict(font_color="#6c757d"),
                                legend=dict(orientation="h",
                                            yanchor="bottom",
                                            y=-0.15,
                                            xanchor="right",
                                            x=1),
                                )
        figDEXVol.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDEXVol.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDEXVol.layout.legend.font.color = '#6c757d'  # font color legend

        return figDEXVol

    @staticmethod
    def getDEXVolExplanation():
        coinDEXVolCardExplanation = [html.P(['The ',
                                             html.A('DEX-API',href='https://api.defichain.io/v1/listswaps?network=mainnet',target='_blank'),
                                             ' is used to read out the 24 hour trading volume in USD. The values are given for each trading pool and for each coin.']),
                                             html.P(['In this first version the trading volume for each pool and the overall sum in USD is represented.']),
                                             html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                                   ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                                    style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'}) ]
        return coinDEXVolCardExplanation
