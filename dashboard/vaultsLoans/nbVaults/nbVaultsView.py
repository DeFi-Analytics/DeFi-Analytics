import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from datetime import datetime
import dateutil.relativedelta

from plotly.subplots import make_subplots


class nbVaultsViewClass:

    def getnbVaultsContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info Number Vaults on DefiChain"),
                              dbc.ModalBody(self.getNbVaultsExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoNbVaults", className="ml-auto"))],
                                    id="modalNbVaults", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Number vaults on DefiChain']),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createNbVaultsFig(data, bgImage), config={'displayModeBar': False}, id='figureNbVaults'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoNbVaults")))
                                          ]))]
        return content



    @staticmethod
    def createNbVaultsFig(data, bgImage):
        figNbVaults = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))



        lastValidDate = datetime.utcfromtimestamp(data['nbVaults'].dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)


        trace_nbVaults = dict(type='scatter', name='Vaults',
                         x=data['nbVaults'].dropna().index, y=data['nbVaults'].dropna(),
                         mode='lines', line=dict(color='#ff00af'), line_width=2, hovertemplate='%{y:.0f}')
        figNbVaults.add_trace(trace_nbVaults, 1, 1)

        figNbVaults.update_yaxes(title_text='number vaults', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)  # ,range=[-50, 200]
        figNbVaults.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figNbVaults.update_layout(xaxis=dict(
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
        figNbVaults.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figNbVaults.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d",
                                             bgcolor='#ffffff', ),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )
        figNbVaults.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figNbVaults.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figNbVaults.layout.legend.font.color = '#6c757d'  # font color legend

        return figNbVaults

    @staticmethod
    def getNbVaultsExplanation():
        nbVaultsCardExplanation = [html.P([''],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return nbVaultsCardExplanation