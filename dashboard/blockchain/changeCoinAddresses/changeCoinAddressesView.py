import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from datetime import datetime

from plotly.subplots import make_subplots


class changeCoinAddressesViewClass:

    def getChangeCoinsAddressesContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info Change of Addresses number and Coins amount"),
                              dbc.ModalBody(self.getChangeExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoChangeCoinAddresses", className="ml-auto"))],
                                    id="modalChangeCoinAddresses", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Change of coins and addresses numbers on a daily base']),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createCoinChangeAddressesFigure(data, bgImage), config={'displayModeBar': False}, id='figureChangeCoin'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoChangeCoinAddresses")))
                                          ]))]
        return content

    @staticmethod
    def createCoinChangeAddressesFigure(data, bgImage):
        figChange = make_subplots(
            rows=2, cols=1,
            vertical_spacing=0.15,
            row_width=[0.5, 0.5],  # from bottom to top
            specs=[[{}],
                   [{}]],
            shared_xaxes=True,
            subplot_titles=(['Change in addresses', 'Change in DFI amount']))
        figChange.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figChange.layout.annotations[0].font.size = 20
        figChange.layout.annotations[0].yref = 'paper'
        figChange.layout.annotations[0].yanchor = 'bottom'
        figChange.layout.annotations[0].y = 1.05

        figChange.layout.annotations[1].font.color = '#6c757d'
        figChange.layout.annotations[1].font.size = 20

        # change in address count
        trace_diffNbMN = dict(type='scatter', name='Masternodes', x=data['diffNbMN'].dropna().index, y=data['diffNbMN'].dropna(),
                              mode='lines', line=dict(color='#f44235'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='MN', visible='legendonly')

        trace_diffNbOther = dict(type='scatter', name='Other', x=data['diffNbOther'].dropna().index, y=data['diffNbOther'].dropna(),
                                 mode='lines', line=dict(color='#410eb2'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='other')

        figChange.add_trace(trace_diffNbMN, 1, 1)
        figChange.add_trace(trace_diffNbOther, 1, 1)


        # change in DFI amount
        trace_diffMnDFI = dict(type='scatter', name='', x=data['diffmnDFI'].dropna().index, y=data['diffmnDFI'].dropna(),
                               mode='lines', line=dict(color='#f44235'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='MN', showlegend=False, visible='legendonly')

        trace_diffOtherDFI = dict(type='scatter', name='', x=data['diffotherDFI'].dropna().index, y=data['diffotherDFI'].dropna(),
                                  mode='lines', line=dict(color='#410eb2'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='other', showlegend=False)

        trace_diffLMDFI = dict(type='scatter', name='Liquidity pool', x=data['diffLMDFI'].dropna().index, y=data['diffLMDFI'].dropna(),
                               mode='lines', line=dict(color='#ff00af'), line_width=3,
                               hovertemplate='%{y:,.0f}', legendgroup='lm')

        trace_diffvaultDFI = dict(type='scatter', name='Vaults', x=data['diffvaultDFI'].dropna().index, y=data['diffvaultDFI'].dropna(),
                               mode='lines', line=dict(color='#808000'), line_width=3,
                               hovertemplate='%{y:,.0f}', legendgroup='vaults')

        figChange.add_trace(trace_diffMnDFI, 2, 1)
        figChange.add_trace(trace_diffOtherDFI, 2, 1)
        figChange.add_trace(trace_diffLMDFI, 2, 1)
        figChange.add_trace(trace_diffvaultDFI, 2, 1)

        figChange.update_yaxes(title_text='Daily change address count', tickformat=",.f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1,
                               col=1)  # ,range=[-50, 200]
        figChange.update_yaxes(title_text='Daily DFI-change ', tickformat=",.f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=2,
                               col=1)  # ,range=[-200000, 1000000]

        figChange.update_xaxes(gridcolor='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figChange.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                               range=[datetime.strptime(data['otherDFI'].dropna().index.values[0], '%Y-%m-%d'), datetime.strptime(data['otherDFI'].dropna().index.values[-1], '%Y-%m-%d')], row=2, col=1)

        figChange.update_layout(xaxis=dict(
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
        figChange.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.79, sizex=0.45, sizey=0.45,  xanchor="center", yanchor="middle", opacity=0.2))
        figChange.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.22, sizex=0.45, sizey=0.45, xanchor="center", yanchor="middle", opacity=0.2))

        figChange.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                                hovermode='x unified',
                                hoverlabel=dict(font_color="#6c757d"),
                                legend=dict(orientation="h",
                                            yanchor="top",
                                            y=-0.12,
                                            xanchor="right",
                                            x=1),
                                )
        figChange.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figChange.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figChange.layout.legend.font.color = '#6c757d'  # font color legend

        return figChange

    def getChangeExplanation(self):
        changeCardExplanation = [
                               html.P(['In the tabs ',html.I('Addresses'),' and ',html.I('Coins'),' the graphs are showing the absolut numbers. In this graphs, '
                                       'the rate of change can only be roughly seen directly. This additional tab shows the daily change.'],style={'text-align': 'justify'}),
                               html.P(['The first diagram represents the increase (positive value) or decrease (negative value) of the addresses '
                                       'with a DFI amount greater 0.'],style={'text-align': 'justify'}),
                               html.P(['The second diagram has the same logic, but for the DFI-amount.' ],style={'text-align': 'justify'}),
                               html.P(['For a better overview only the graph for individual addresses is shown. Further categories can be shown by clicking on the '
                                       'legend entry.' ],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})        ]
        return changeCardExplanation

