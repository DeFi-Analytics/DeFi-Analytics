import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import dateutil.relativedelta

class overallTVLViewClass:

    def getOverallTVLContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Overall Total Value Locked (TVL)"),
                              dbc.ModalBody(self.getOverallTVLExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoOverallTVL", className="ml-auto"))], id="modalOverallTVL", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Overall total value locked (TVL)']),
                                          html.Table([html.Tr([html.Td('Select currency for Overall TVL representation:'),
                                          html.Td(dcc.Dropdown(id='defiOverallTVLCurrency',options=[{'label': 'USD', 'value': 'USD'},
                                                                                             {'label': 'BTC', 'value': 'BTC'},
                                                                                             {'label': 'DFI', 'value': 'DFI'}],
                                                               value='USD', clearable=False, style=dict(width='150px',verticalAlign="bottom")))])]),
                                          dcc.Graph(id = 'figureOverallTVL', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoOverallTVL")))]))]
        return content

    @staticmethod
    def createOverallTVLGraph(data, currencySelection, bgImage):
        if currencySelection == 'BTC':
            DFIPrice = data['DFIPriceUSD']/data['BTCPriceUSD']        # choose BTC-pool DFI-price in BTC
            yAxisLabel = 'Value in BTC'
            hoverTemplateRepresenation = '%{y:,.3f}BTC'
        elif currencySelection == 'DFI':
            DFIPrice = data['DFIPriceUSD'] / data['DFIPriceUSD']      # create series with 1 as an entry
            yAxisLabel = 'Value in DFI'
            hoverTemplateRepresenation = '%{y:,.0f}DFI'
        else:
            DFIPrice = data['DFIPriceUSD']       # choose USDT-pool for DFI-price in BTC
            yAxisLabel = 'Value in $'
            hoverTemplateRepresenation = '$%{y:,.0f}'

        TVLOverall = (data['tvlMNDFI']+data['tvlDEXDFI']) * DFIPrice  # DFI is USD is highest price of the 3
        indexVector = data['tvlMNDFI'].notnull() & data['tvlDEXDFI'].notnull() & DFIPrice.notnull()

        lastValidDate = datetime.strptime(TVLOverall.dropna().index.values[-1], '%Y-%m-%d')
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        # Plotting long term price
        figTVL = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        # single TVL graphs
        trace_tvlMN = dict(type='scatter', name='Masternodes', x=(data.loc[indexVector,'tvlMNDFI']*DFIPrice[indexVector]).index, y=(data.loc[indexVector,'tvlMNDFI']*DFIPrice[indexVector]), stackgroup='one',
                            mode='lines', line=dict(color='#da3832'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tozeroy')
        trace_tvlDEX = dict(type='scatter', name='DEX', x=(data.loc[indexVector,'tvlDEXDFI']*DFIPrice[indexVector]).index, y=(data.loc[indexVector,'tvlDEXDFI']*DFIPrice[indexVector]), stackgroup='one',
                            mode='lines', line=dict(color='#ff2ebe'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')

        # overall TVL graph
        trace_TVLOverall = dict(type='scatter', name='Overall', x=TVLOverall[indexVector].index, y=TVLOverall[indexVector],
                                mode='lines', line=dict(color='#410eb2'), line_width=3, hovertemplate=hoverTemplateRepresenation)

        figTVL.add_trace(trace_tvlMN, 1, 1)
        figTVL.add_trace(trace_tvlDEX, 1, 1)

        figTVL.add_trace(trace_TVLOverall, 1, 1)

        figTVL.update_yaxes(title_text=yAxisLabel, tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figTVL.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                            range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figTVL.update_layout(xaxis=dict(
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
        figTVL.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.25))

        figTVL.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                         yanchor="top",
                                         y=-0.12,
                                         xanchor="right",
                                         x=1),
                             )
        figTVL.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figTVL.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figTVL.layout.legend.font.color = '#6c757d'  # font color legend

        return figTVL

    @staticmethod
    def getOverallTVLExplanation():
        coinTVLCardExplanation = [html.P(['The overall total value locked is a key figure, that describes the value stored on DefiChain.'],style={'text-align': 'justify'}),
                                  html.P(['The graph shows the part of the masternodes (red area), the DEX (pink area) and the sum of all parts (purple line).'],style={'text-align': 'justify'}),
                                  html.P(['Normally the TVL is shown in USD. But maybe the reprensentation in BTC or DFI is also interesting for giving some information of the overall TVL.'],style={'text-align': 'justify'}),
                                   html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                                  ]
        return coinTVLCardExplanation