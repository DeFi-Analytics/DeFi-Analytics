import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta


class volume24hrViewClass:
    def getVolume24hrContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info 24hr DEX volume"),
                              dbc.ModalBody(self.getDEXVolExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoVolume24hr", className="ml-auto"))],
                                    id="modalVolume24hr", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Trading volume (24hr) on DEX']),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createDEXVolume24hrGraph(data, bgImage), config={'displayModeBar': False}, id='figureVolume24hr'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoVolume24hr")))
                                          ]))]
        return content

    @staticmethod
    def createDEXVolume24hrGraph(data, bgImage):
        figDEXVol = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        lastValidDate = datetime.utcfromtimestamp(data['BTC_VolTotal'].dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)
        hoverTemplateRepresenation = '$%{y:,.0f}'

        indTradingVolumes = [element for element in data.columns.values if "24hrTrading" in element]
        indTradingVolumesDToken = [element for element in indTradingVolumes if "DUSD" in element]
        indTradingVolumesCrypto = [element for element in indTradingVolumes if ("DUSD" not in element) & ("BURN" not in element)]

        tradingVolumeDToken = data[indTradingVolumesDToken].sum(axis=1, skipna=False)
        tradingVolumeCrypto = data[indTradingVolumesCrypto].sum(axis=1, skipna=False)

        trace_tradingVolumeCrypto = dict(type='scatter', name='Crypto volume', x=tradingVolumeCrypto.dropna().index, y=tradingVolumeCrypto.dropna(),
                                    mode='lines', line=dict(color='#ffbfeb'), line_width=0, stackgroup='one', hovertemplate=hoverTemplateRepresenation, fill='tozeroy')

        trace_tradingVolumeDToken = dict(type='scatter', name='dToken colume',x=tradingVolumeDToken.dropna().index, y=tradingVolumeDToken.dropna(),
                                 mode='lines', line=dict(color='#ff7fd7'), line_width=0, stackgroup='one', hovertemplate=hoverTemplateRepresenation, fill='tonexty')

        # overall TVL graph
        trace_VolOverallDEX = dict(type='scatter', name='Overall DEX', x=(tradingVolumeDToken+tradingVolumeCrypto).dropna().index, y=(tradingVolumeDToken+tradingVolumeCrypto).dropna(),
                                mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate=hoverTemplateRepresenation)
        trace_VolOverallCG = dict(type='scatter', name='Overall Coingecko (only DFI)', x=data['VolTotalCoingecko'].dropna().index, y=data['VolTotalCoingecko'].dropna(),
                                mode='lines', line=dict(color='#5c0fff'), line_width=3, hovertemplate=hoverTemplateRepresenation)


        figDEXVol.add_trace(trace_tradingVolumeCrypto, 1, 1)
        figDEXVol.add_trace(trace_tradingVolumeDToken, 1, 1)
        figDEXVol.add_trace(trace_VolOverallDEX, 1, 1)
        figDEXVol.add_trace(trace_VolOverallCG, 1, 1)

        figDEXVol.update_yaxes(title_text='24h volume in USD', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                               zerolinecolor='#6c757d', row=1, col=1)
        figDEXVol.update_xaxes(title_text="Date", gridcolor='#6c757d', range=[date14DaysBack.strftime('%Y-%m-%d'), lastValidDate],
                               showticklabels=True, color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)

        # Add range slider
        figDEXVol.update_layout(xaxis=dict(
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

        # add background picture
        figDEXVol.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figDEXVol.update_layout(margin={"t": 30, "l": 0, "b": 0, 'r': 0},
                                hovermode='x unified',
                                hoverlabel=dict(font_color="#6c757d"),
                                legend=dict(orientation="h",
                                            yanchor="top",
                                            y=-0.12,
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
                                             html.A('Ocean-API',href='https://ocean.defichain.com/v0/mainnet/poolpairs',target='_blank', className='defiLink'),
                                             ' is used to read out the moving 24 hour trading volume in USD. The values are represented for the crypto- and dToken-pools.',html.Br(),
                                             'Also the 24hr trading volume from the Coingecko is shown to compare the DEX with the centralized exchanges volume.']),
                                             html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                                   ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                                    style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'}) ]
        return coinDEXVolCardExplanation
