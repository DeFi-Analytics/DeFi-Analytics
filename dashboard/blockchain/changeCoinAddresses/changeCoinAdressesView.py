import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class changeCoinAddressesViewClass:

    def getChangeCoinsAddressesContent(self, data):
        content = [dbc.Card(dbc.CardBody([dcc.Graph(figure=self.createCoinChangeAddressesFigure(data),
                                                    config={'displayModeBar': False})])),
                   dbc.Card(dbc.CardBody(self.getChangeExplanation()), style={'margin-top': '1.0rem'})]
        return content

    @staticmethod
    def createCoinChangeAddressesFigure(data):
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
        figChange.layout.annotations[1].font.color = '#6c757d'
        figChange.layout.annotations[1].font.size = 20

        # change in address count
        trace_diffNbMN = dict(type='scatter', name='Masternodes', x=data['diffNbMN'].dropna().index, y=data['diffNbMN'].dropna(),
                              mode='lines', line=dict(color='#f44235'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='MN', visible='legendonly')
        figChange.add_trace(trace_diffNbMN, 1, 1)

        trace_diffNbFund = dict(type='scatter', name='Community fund', x=data['diffNbNone'].dropna().index, y=data['diffNbNone'].dropna(),            # dropna not useful for none-array
                                mode='lines', line=dict(color='#ff9800'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='CF', visible='legendonly')
        figChange.add_trace(trace_diffNbFund, 1, 1)

        trace_diffNbFoundation = dict(type='scatter', name='Foundation', x=data['diffNbNone'].dropna().index, y=data['diffNbNone'].dropna(),          # dropna not useful for none-array
                                      mode='lines', line=dict(color='#22b852'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='Found', visible='legendonly')
        figChange.add_trace(trace_diffNbFoundation, 1, 1)

        trace_diffNbOther = dict(type='scatter', name='Other', x=data['diffNbOther'].dropna().index, y=data['diffNbOther'].dropna(),
                                 mode='lines', line=dict(color='#410eb2'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='other')

        figChange.add_trace(trace_diffNbOther, 1, 1)

        # change in DFI amount
        trace_diffMnDFI = dict(type='scatter', name='', x=data['diffmnDFI'].dropna().index, y=data['diffmnDFI'].dropna(),
                               mode='lines', line=dict(color='#f44235'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='MN', showlegend=False, visible='legendonly')
        figChange.add_trace(trace_diffMnDFI, 2, 1)

        trace_diffFundDFI = dict(type='scatter', name='', x=data['difffundDFI'].dropna().index, y=data['difffundDFI'].dropna(),
                                 mode='lines', line=dict(color='#ff9800'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='CF', showlegend=False, visible='legendonly')
        figChange.add_trace(trace_diffFundDFI, 2, 1)

        trace_diffFoundationDFI = dict(type='scatter', name='', x=data['difffoundationDFI'].dropna().index, y=data['difffoundationDFI'].dropna(),
                                       mode='lines', line=dict(color='#22b852'), line_width=3,
                                       hovertemplate='%{y:,.0f}', legendgroup='Found', showlegend=False, visible='legendonly')
        figChange.add_trace(trace_diffFoundationDFI, 2, 1)

        trace_diffOtherDFI = dict(type='scatter', name='', x=data['diffotherDFI'].dropna().index, y=data['diffotherDFI'].dropna(),
                                  mode='lines', line=dict(color='#410eb2'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='other', showlegend=False)
        figChange.add_trace(trace_diffOtherDFI, 2, 1)

        trace_diffLMDFI = dict(type='scatter', name='Liquidity pool', x=data['diffLMDFI'].dropna().index, y=data['diffLMDFI'].dropna(),
                               mode='lines', line=dict(color='#ff00af'), line_width=3,
                               hovertemplate='%{y:,.0f}', legendgroup='lm')
        figChange.add_trace(trace_diffLMDFI, 2, 1)

        figChange.update_yaxes(title_text='Daily change address count', tickformat=",.f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1,
                               col=1)  # ,range=[-50, 200]
        figChange.update_yaxes(title_text='Daily DFI-change ', tickformat=",.f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=2,
                               col=1)  # ,range=[-200000, 1000000]
        figChange.update_xaxes(gridcolor='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figChange.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=2, col=1)

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

        figChange.update_layout(height=680,
                                margin={"t": 40, "l": 130, "b": 20},
                                hovermode='x unified',
                                hoverlabel=dict(font_color="#6c757d"),
                                legend=dict(orientation="h",
                                            yanchor="bottom",
                                            y=-0.3,
                                            xanchor="right",
                                            x=1),
                                )
        figChange.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figChange.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figChange.layout.legend.font.color = '#6c757d'  # font color legend

        return figChange

    def getChangeExplanation(self):
        changeCardExplanation = [html.H4("Info Change"),
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

