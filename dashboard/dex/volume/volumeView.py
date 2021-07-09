import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta


class volumeViewClass:
    def getVolumeContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info DEX volume"),
                              dbc.ModalBody(self.getVolumeExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoVolume", className="ml-auto"))],
                                    id="modalVolume", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Trading volume on DEX']),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createDEXVolumeGraph(data, bgImage, 'hourly'), config={'displayModeBar': False}, id='figureVolume'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoVolume")))
                                          ]))]
        return content


    @staticmethod
    def createDEXVolumeGraph(data, bgImage, representation):
        figDEXvolume = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        formatHover = '%{y:,.0f}'
        yAxisLabel = 'Traded DFI volume'
        yAxisTick = ",.0f"
        lastValidDate = datetime.utcfromtimestamp(data.index.values[-1].tolist() / 1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        lastValidDate = datetime.utcfromtimestamp(data['volumeOverallbuyDFI'].dropna().index.values[-1].tolist() / 1e9)
        date30DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=30)

        trace_diff = dict(type='scatter', name='Difference', x=(data['volumeOverallbuyDFI' ] -data['volumeOverallsellDFI']).dropna().index,
                          y=(data['volumeOverallbuyDFI' ] -data['volumeOverallsellDFI']).dropna(),
                          mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate=formatHover)
        trace_followed = dict(type='scatter', name='Bought DFI', x=data['volumeOverallbuyDFI'].dropna().index, y=(data['volumeOverallbuyDFI']).dropna(),
                              mode='lines', line=dict(color='#90dba8'), line_width=3, hovertemplate=formatHover, fill='tozeroy')
        trace_unfollowed = dict(type='scatter', name='Sold DFI', x=data['volumeOverallsellDFI'].dropna().index, y=(-data['volumeOverallsellDFI']).dropna(),
                                mode='lines', line=dict(color='#ec9b98'), line_width=3, hovertemplate=formatHover, fill='tozeroy')

        figDEXvolume.add_trace(trace_followed, 1, 1)
        figDEXvolume.add_trace(trace_unfollowed, 1, 1)
        figDEXvolume.add_trace(trace_diff, 1, 1)

        figDEXvolume.update_yaxes(title_text=yAxisLabel, tickformat=yAxisTick, gridcolor='#6c757d', color='#6c757d',
                                              zerolinecolor='#6c757d', row=1, col=1)
        figDEXvolume.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                                              row=1, col=1)       # select 14 days range: range=[date30DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate]

        # Add range slider
        figDEXvolume.update_layout(xaxis=dict(
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
        DEXVolumeCardExplanation = [html.P(['...']),
                                     html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                                   ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                                    style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'}) ]
        return DEXVolumeCardExplanation