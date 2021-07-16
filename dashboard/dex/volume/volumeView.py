import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

import pandas as pd


class volumeViewClass:
    def getVolumeContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info DEX volume"),
                              dbc.ModalBody(self.getVolumeExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoVolume", className="ml-auto"))],
                                    id="modalVolume", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Trading volume on DEX']),
                                          html.Table([html.Tr([html.Td('Select time base for representation:'),
                                                               html.Td(dcc.Dropdown(id='dexVolumeSelection',
                                                                                    options=[{'label': 'Hourly volume', 'value': 'H'},
                                                                                             {'label': 'Daily volume', 'value': 'D'},
                                                                                             {'label': 'Weekly volume', 'value': 'W'}],
                                                                                    value='H', clearable=False, style=dict(width='235px', verticalAlign="bottom")))])]),
                                                      dbc.FormGroup([dbc.Checkbox(id="dexVolumeAlldata", className="form-check-input", checked=False),
                                                                     dbc.Label("Show all data (could need some time)", html_for="dexVolumeAlldata",className="form-check-label")], check=True),
                                          dbc.Row(dbc.Col(dcc.Graph(config={'displayModeBar': False}, id='figureVolume'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoVolume")))
                                          ]))]
        return content


    @staticmethod
    def createDEXVolumeGraph(data, bgImage, representation, allData):
        figDEXvolume = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        formatHover = '$%{y:,.0f}'
        yAxisLabel = 'Traded DFI volume in USD'
        yAxisTick = ",.0f"
        lastValidDate = datetime.utcfromtimestamp(data['volumeOverallbuyDFI'].dropna().index.values[-1].tolist() / 1e9)

        if (representation=='H') & (~allData):
            maxRangeIndex = 14*24
            dateGoBack = lastValidDate - dateutil.relativedelta.relativedelta(hours=48)
        elif (representation=='D') & (~allData):
            maxRangeIndex = 180*24
            dateGoBack = lastValidDate - dateutil.relativedelta.relativedelta(days=30)
        else:
            maxRangeIndex = data['volumeOverallbuyDFI'].dropna().size
            dateGoBack = lastValidDate - dateutil.relativedelta.relativedelta(months=6)




        trace_diff = dict(type='scatter', name='Difference',
                          x=(data['volumeOverallbuyDFI' ] -data['volumeOverallsellDFI']).dropna().iloc[-maxRangeIndex:].groupby(pd.Grouper(freq=representation)).sum().index,
                          y=(data['volumeOverallbuyDFI' ] -data['volumeOverallsellDFI']).dropna().iloc[-maxRangeIndex:].groupby(pd.Grouper(freq=representation)).sum(),
                          mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate=formatHover)
        trace_bought = dict(type='scatter', name='Bought DFI',
                            x=data['volumeOverallbuyDFI'].dropna().iloc[-maxRangeIndex:].groupby(pd.Grouper(freq=representation)).sum().index,
                            y=(data['volumeOverallbuyDFI']).dropna().iloc[-maxRangeIndex:].groupby(pd.Grouper(freq=representation)).sum(),
                              mode='lines', line=dict(color='#90dba8'), line_width=3, hovertemplate=formatHover, fill='tozeroy')
        trace_sold = dict(type='scatter', name='Sold DFI',
                          x=data['volumeOverallsellDFI'].dropna().iloc[-maxRangeIndex:].groupby(pd.Grouper(freq=representation)).sum().index,
                          y=(-data['volumeOverallsellDFI']).dropna().iloc[-maxRangeIndex:].groupby(pd.Grouper(freq=representation)).sum(),
                                mode='lines', line=dict(color='#ec9b98'), line_width=3, hovertemplate=formatHover, fill='tozeroy')

        figDEXvolume.add_trace(trace_bought, 1, 1)
        figDEXvolume.add_trace(trace_sold, 1, 1)
        figDEXvolume.add_trace(trace_diff, 1, 1)

        figDEXvolume.update_yaxes(title_text=yAxisLabel, tickformat=yAxisTick, gridcolor='#6c757d', color='#6c757d',
                                              zerolinecolor='#6c757d', row=1, col=1)
        figDEXvolume.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                                  range=[dateGoBack, lastValidDate], row=1, col=1)       # select 14 days range: range=[date30DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate]

        # Add range slider
        figDEXvolume.update_layout(barmode='stack',
            xaxis=dict(
            rangeselector=dict(
                buttons=list([dict(count=2, label="2d", step="day", stepmode="backward"),
                              dict(count=7, label="7d", step="day", stepmode="backward"),
                              dict(count=14, label="14d", step="day", stepmode="backward"),
                              dict(count=30, label="30d", step="day", stepmode="backward"),
                              dict(count=2, label="2m", step="month", stepmode="backward"),
                              dict(count=6, label="6m", step="month", stepmode="backward"),
                              dict(count=1, label="YTD", step="year", stepmode="todate"),
                              dict(count=1, label="1y", step="year", stepmode="backward"),
                              dict(step="all")])),
            rangeslider=dict(visible=False),
            type="date"))

        # add background picture
        figDEXvolume.add_layout_image \
            (dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.25))

        figDEXvolume.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                                               hovermode='x unified',
                                               hoverlabel=dict(font_color="#6c757d"),
                                               legend=dict(orientation="h",
                                                           yanchor="top",
                                                           y=-0.12,
                                                           xanchor="right",
                                                           x=1),
                                               )
        figDEXvolume.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDEXvolume.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDEXvolume.layout.legend.font.color = '#6c757d'  # font color legend
        figDEXvolume.layout.hoverlabel.bgcolor = 'white'
        return figDEXvolume

    @staticmethod
    def getVolumeExplanation():
        DEXVolumeCardExplanation = [html.P(['In this graphic all DEX trades are read out, summed up on an hourly base and multiplied with the DFI price in USD. Over all pools you can see how many DFI are bought, '
                                            'sold and the difference (in USD). The user can also choose if the values should aggregated again to a daily or weekly base.']),
                                    html.P(['In the standard representation not all data is shown for hourly and daily time base to keep the performance. If you are interested in all values, just activate the corresponding '
                                            'checkbox.']),
                                     html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                                   ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                                    style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'}) ]
        return DEXVolumeCardExplanation