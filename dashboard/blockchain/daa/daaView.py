import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from datetime import datetime
import dateutil.relativedelta

from plotly.subplots import make_subplots


class daaViewClass:

    def getDAAContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info Daily Active Addresses"),
                              dbc.ModalBody(self.getDAAExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoDAA", className="ml-auto"))],
                                    id="modalDAA", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Daily active addresses (DAA)']),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createDAAFig(data, bgImage), config={'displayModeBar': False}, id='figureDAA'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoDAA")))
                                          ]))]
        return content

    @staticmethod
    def createDAAFig(data, bgImage):
        figDAA = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))


        lastValidDate = datetime.strptime(data['countAddresses'].dropna().index.values[-2], '%Y-%m-%d')
        date6MonthsBack = lastValidDate - dateutil.relativedelta.relativedelta(months=6)

        MA7dDAA = data['countAddresses'].rolling(window=7).mean()
        MA28dDAA = data['countAddresses'].rolling(window=28).mean()

        trace_DAA = dict(type='scatter', name='daily data',
                         x=data['countAddresses'].dropna().index.values[:-1], y=data['countAddresses'].dropna().values[:-1],
                         mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:,.0f}')
        trace_DAA7d = dict(type='scatter', name='7d moving average',
                         x=MA7dDAA.dropna().index.values[:-1], y=MA7dDAA.dropna().values[:-1],
                         mode='lines', line=dict(color='#5f18ff'), line_width=3, hovertemplate='%{y:,.0f}')
        trace_DAA28d = dict(type='scatter', name='28d moving average',
                         x=MA28dDAA.dropna().index.values[:-1], y=MA28dDAA.dropna().values[:-1],
                         mode='lines', line=dict(color='#af8bfe'), line_width=3, hovertemplate='%{y:,.0f}')

        figDAA.add_trace(trace_DAA, 1, 1)
        figDAA.add_trace(trace_DAA7d, 1, 1)
        figDAA.add_trace(trace_DAA28d, 1, 1)

        figDAA.update_yaxes(title_text='number addresses involved in transactions', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1,
                            col=1)  # ,range=[-50, 200]
        figDAA.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date6MonthsBack.strftime('%Y-%m-%d'), data['countAddresses'].dropna().index.values[-2]], row=1, col=1)

        # Add range slider
        figDAA.update_layout(xaxis=dict(
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
        figDAA.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figDAA.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d",
                                             bgcolor='#ffffff', ),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )
        figDAA.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDAA.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDAA.layout.legend.font.color = '#6c757d'  # font color legend

        return figDAA

    @staticmethod
    def getDAAExplanation():
        daaCardExplanation = [html.P(['The characteristic value DAA (daily active addresses) indicates the number of addresses with at least one transaction on the selected day. '
                                       'The address can be the sender or receiver of any amount.'],style={'text-align': 'justify'}),
                               html.P(['The data is extracted by analyzing each block and getting the included transactions. With this transaction information '
                                       'the sending and receiving addresses are determined.'],style={'text-align': 'justify'}),
                               html.P([html.B('Remark: ' ),'Due to the high effort, the data is determined manually via a node and not automatically usind API. I try my best, but there might be some delay.'],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return daaCardExplanation