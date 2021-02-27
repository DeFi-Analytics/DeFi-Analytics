import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class blocktimeViewClass:

    def getAddressContent(self, data):
        content = [dbc.Card(dbc.CardBody([dcc.Graph(figure=self.createBlocktimeFigure(data),
                                                    config={'displayModeBar': False})])),
                   dbc.Card(dbc.CardBody(self.getBlockTimeExplanation()), style={'margin-top': '1.0rem'})]
        return content

    @staticmethod
    def createBlocktimeFigure(data):
        figBlockTime = make_subplots(
            rows=2, cols=1,
            vertical_spacing=0.15,
            row_width=[0.7, 0.3],  # from bottom to top
            specs=[[{}],
                   [{}]],
            shared_xaxes=True,
            subplot_titles=(['Mean Block time', 'Block time distribution']))
        figBlockTime.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figBlockTime.layout.annotations[0].font.size = 20
        figBlockTime.layout.annotations[1].font.color = '#6c757d'
        figBlockTime.layout.annotations[1].font.size = 20

        trace_meanTime = dict(type='scatter', name='Mean Time',
                              x=data['meanBlockTime'].dropna().index.values[1:],
                              y=data['meanBlockTime'].dropna().values[1:],
                              mode='lines', line=dict(color='#da3832'), line_width=3, hovertemplate='%{y:.2f}s')
        figBlockTime.add_trace(trace_meanTime, 1, 1)

        trace_Min = dict(type='scatter', name='Mininum',
                         x=data['MinBlockTime'].dropna().index.values[1:],
                         y=data['MinBlockTime'].dropna().values[1:],
                         mode='lines', line=dict(color='#90d1e5'), line_width=0, hovertemplate='%{y:.0f}s',
                         showlegend=False)
        trace_10Perc = dict(type='scatter', name='10% quantile',
                            x=data['10PercentBlockTime'].dropna().index.values[1:],
                            y=data['10PercentBlockTime'].dropna().values[1:],
                            mode='lines', line=dict(color='#90d1e5'), line_width=2, hovertemplate='%{y:.0f}s')
        trace_4Fill10 = dict(type='scatter', name='4Filling',
                             x=data['30PercentBlockTime'].dropna().index.values[1:],
                             y=data['30PercentBlockTime'].dropna().values[1:],
                             fill='tonexty', fillcolor='rgba(144, 209, 229, 0.5)',
                             mode='lines', line=dict(color='#90d1e5'), line_width=0, hoverinfo='none', showlegend=False)
        trace_30Perc = dict(type='scatter', name='30% quantile',
                            x=data['30PercentBlockTime'].drop().index.values[1:],
                            y=data['30PercentBlockTime'].drop().values[1:], fill='tonexty',
                            mode='lines', line=dict(color='#3fbadf'), line_width=2, hovertemplate='%{y:.0f}s')
        trace_4Fill30 = dict(type='scatter', name='4Filling',
                             x=data['medianBlockTime'].dropna().index.values[1:],
                             y=data['medianBlockTime'].dropna().values[1:],
                             fill='tonexty', fillcolor='rgba(63, 186, 223, 0.5)',
                             mode='lines', line=dict(color='#3fbadf'), line_width=0, hoverinfo='none', showlegend=False)
        trace_Median = dict(type='scatter', name='Median',
                            x=data['medianBlockTime'].dropna().index.values[1:],
                            y=data['medianBlockTime'].dropna().values[1:],
                            mode='lines', line=dict(color='#7f50ff'), line_width=4, hovertemplate='%{y:.0f}s')
        trace_70Perc = dict(type='scatter', name='70% quantile',
                            x=data['70PercentBlockTime'].dropna().index.values[1:],
                            y=data['70PercentBlockTime'].dropna().values[1:],
                            fill='tonexty', fillcolor='rgba(63, 186, 223, 0.5)',
                            mode='lines', line=dict(color='#3fbadf'), line_width=2, hovertemplate='%{y:.0f}s')
        trace_90Perc = dict(type='scatter', name='90% quantile',
                            x=data['90PercentBlockTime'].dropna().index.values[1:],
                            y=data['90PercentBlockTime'].dropna().values[1:],
                            fill='tonexty', fillcolor='rgba(144, 209, 229, 0.5)',
                            mode='lines', line=dict(color='#90d1e5'), line_width=2, hovertemplate='%{y:.0f}s')
        trace_Max = dict(type='scatter', name='Maximum',
                         x=data['MaxBlockTime'].dropna().index.values[1:],
                         y=data['MaxBlockTime'].dropna().values[1:],
                         mode='lines', line=dict(color='#90d1e5'), line_width=0, hovertemplate='%{y:.0f}s',
                         showlegend=False)

        figBlockTime.add_trace(trace_Min, 2, 1)
        figBlockTime.add_trace(trace_10Perc, 2, 1)
        figBlockTime.add_trace(trace_4Fill10, 2, 1)
        figBlockTime.add_trace(trace_30Perc, 2, 1)
        figBlockTime.add_trace(trace_4Fill30, 2, 1)
        figBlockTime.add_trace(trace_Median, 2, 1)
        figBlockTime.add_trace(trace_70Perc, 2, 1)
        figBlockTime.add_trace(trace_90Perc, 2, 1)
        figBlockTime.add_trace(trace_Max, 2, 1)

        figBlockTime.update_yaxes(title_text='Time in s', tickformat=",.2f", gridcolor='#6c757d', color='#6c757d',
                                  zerolinecolor='#6c757d', range=[30, 45], row=1, col=1)  # ,range=[-50, 200]
        figBlockTime.update_yaxes(title_text='Time in s', tickformat=",.2f", gridcolor='#6c757d', color='#6c757d',
                                  zerolinecolor='#6c757d', range=[0, 100], row=2, col=1)  # ,range=[-200000, 1000000]
        figBlockTime.update_xaxes(gridcolor='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figBlockTime.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                                  row=2, col=1)
        figBlockTime.update_layout(height=680,
                                   margin={"t": 40, "l": 130, "b": 20},
                                   hovermode='x unified',
                                   hoverlabel=dict(font_color="#6c757d"),
                                   legend=dict(orientation="h",
                                               yanchor="bottom",
                                               y=-0.3,
                                               xanchor="right",
                                               x=1),
                                   )
        figBlockTime.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figBlockTime.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figBlockTime.layout.legend.font.color = '#6c757d'  # font color legend

        return figBlockTime


    def getBlockTimeExplanation(self):
        coinAddressCardExplanation = [html.H4("Info Block Time"),
                                      html.P(['On this tab the block time of Defichain is tracked. With the help of the API a database is generated, where for each block ',
                                                 'the generation time is saved. With these timestamps the mean value of the time difference between 2 blocks is calculated for each day.'],
                                             style={'text-align': 'justify'}),
                                      html.P([
                                                 'Beside the mean value also the distribution of the blocktime for each day could be interesting. To visualize this, 5 different quantiles are ',
                                                 'plottes as lines over time']),
                                      html.P([html.B('Hint:'),
                                              ' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                              ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                             style={'text-align': 'justify', 'fontSize': '0.7rem',
                                                    'color': '#6c757d'})
                                      ]
        return coinAddressCardExplanation