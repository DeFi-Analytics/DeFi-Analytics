import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from datetime import datetime
import dateutil.relativedelta

from plotly.subplots import make_subplots


class dUSDMeasuresViewClass:

    def getdUSDMeasuresContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info dUSD Measures"),
                              dbc.ModalBody(self.getdUSDMeasuresExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfodUSDMeasures", className="ml-auto"))],
                                    id="modaldUSDMeasures", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['dUSD Measures']),
                                          html.Div(['On this page all introduced measures to move the dUSD value towards 1 USD are evaluated.'], style={'margin-bottom': '30px'}),
                                          html.H5(['DEX stabilizing fee']),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createDUSDStabFeeFig(data, bgImage), config={'displayModeBar': False}, id='figureDUSDStabFee'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfodUSDMeasures")))
                                          ]))]
        return content



    @staticmethod
    def createDUSDStabFeeFig(data, bgImage):
        figDUSDFee = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))


        lastValidDate = datetime.strptime(data['sellDUSDFee'].dropna().index.values[-1], '%Y-%m-%d')
        date30DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(months=2)


        trace_dUSDStabFee = dict(type='scatter', name='DEX stabilizing fee',
                         x=data['sellDUSDFee'].dropna().index, y=data['sellDUSDFee'].dropna()*100,
                         mode='lines', line=dict(color='#ff00af'), line_width=2, hovertemplate='%{y:,.2f}%')
        figDUSDFee.add_trace(trace_dUSDStabFee, 1, 1)

        figDUSDFee.update_yaxes(title_text='DEX stabilizing fee in %', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)  # ,range=[-50, 200]
        figDUSDFee.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date30DaysBack, lastValidDate], row=1, col=1)

        # Add range slider
        figDUSDFee.update_layout(xaxis=dict(
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
        figDUSDFee.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figDUSDFee.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d",
                                             bgcolor='#ffffff', ),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )
        figDUSDFee.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDUSDFee.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDUSDFee.layout.legend.font.color = '#6c757d'  # font color legend

        return figDUSDFee

    @staticmethod
    def getdUSDMeasuresExplanation():
        dUSDMeasuresCardExplanation = [html.P([''],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return dUSDMeasuresCardExplanation