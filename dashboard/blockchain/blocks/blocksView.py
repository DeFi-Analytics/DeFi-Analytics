import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from datetime import datetime
import dateutil.relativedelta

from plotly.subplots import make_subplots


class blocksViewClass:

    def getBlocksContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info Blocks per day"),
                              dbc.ModalBody(self.getBlocksExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoBlocks", className="ml-auto"))],
                                    id="modalBlocks", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Blocks per Day']),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createBlocksFig(data, bgImage), config={'displayModeBar': False}, id='figureBlocks'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoBlocks")))
                                          ]))]
        return content

    @staticmethod
    def createBlocksFig(data, bgImage):
        figBlocks = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))


        lastValidDate = datetime.strptime(data['nbBlocks'].dropna().index.values[-2], '%Y-%m-%d')
        date2MonthsBack = lastValidDate - dateutil.relativedelta.relativedelta(months=2)

        trace_Blocks = dict(type='scatter', name='Blocks',
                         x=data['nbBlocks'].dropna().index.values[:-1], y=data['nbBlocks'].dropna().values[:-1],
                         mode='lines', line=dict(color='#ff00af'), line_width=2, hovertemplate='%{y:.0f}')
        figBlocks.add_trace(trace_Blocks, 1, 1)

        figBlocks.update_yaxes(title_text='minted blocks per day', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1,
                            col=1)  # ,range=[-50, 200]
        figBlocks.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date2MonthsBack.strftime('%Y-%m-%d'), data['nbBlocks'].dropna().index.values[-2]], row=1, col=1)

        # Add range slider
        figBlocks.update_layout(xaxis=dict(
            rangeselector=dict(
                buttons=list([dict(count=30, label="30d", step="day", stepmode="backward"),
                              dict(count=2, label="2m", step="month", stepmode="backward"),
                              dict(count=6, label="6m", step="month", stepmode="backward"),
                              dict(count=1, label="YTD", step="year", stepmode="todate"),
                              dict(count=1, label="1y", step="year", stepmode="backward"),
                              dict(step="all")])),
            rangeslider=dict(visible=False),
            type="date"))

        # add background picture
        figBlocks.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figBlocks.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d",
                                             bgcolor='#ffffff', ),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )
        figBlocks.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figBlocks.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figBlocks.layout.legend.font.color = '#6c757d'  # font color legend

        return figBlocks

    @staticmethod
    def getBlocksExplanation():
        blocksCardExplanation = [html.P(['This evaluation shows the number of minted blocks per day. With an mean block time of 30s round about 2900 blocks should be found per day. '
                                         'Due to statistical uncertainties this number will vary a little bit.'],
                                             style={'text-align': 'justify'}),
                                      html.P([html.B('Hint:'),
                                              ' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                              ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                             style={'text-align': 'justify', 'fontSize': '0.7rem',
                                                    'color': '#6c757d'})]
        return blocksCardExplanation