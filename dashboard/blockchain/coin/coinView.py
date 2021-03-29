import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class coinViewClass:

    def getCoinContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info Coins"),
                              dbc.ModalBody(self.getCoinExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoCoin", className="ml-auto"))],
                                    id="modalCoin", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([dbc.Row(dbc.Col(dcc.Graph(figure=self.createCoinFigure(data, bgImage), config={'displayModeBar': False}))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoCoin")))
                                          ]))]
        return content


    @staticmethod
    def createCoinFigure(data, bgImage):
        figDFI = make_subplots(
            rows=2, cols=1,
            vertical_spacing=0.15,
            row_width=[0.5, 0.5],  # from bottom to top
            specs=[[{}],
                   [{}]],
            shared_xaxes=True,
            subplot_titles=(['Total representation', 'Relative representation']))
        figDFI.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figDFI.layout.annotations[0].font.size = 20
        figDFI.layout.annotations[0].yref = 'paper'
        figDFI.layout.annotations[0].yanchor = 'bottom'
        figDFI.layout.annotations[0].y = 1.05

        figDFI.layout.annotations[1].font.color = '#6c757d'
        figDFI.layout.annotations[1].font.size = 20

        # absolut DFI representation
        trace_mnDFI = dict(type='scatter', name='Masternodes', x=data['mnDFI'].dropna().index, y=data['mnDFI'].dropna(),
                           mode='lines', line=dict(color='#f44235'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='MN')
        figDFI.add_trace(trace_mnDFI, 1, 1)

        trace_fundDFI = dict(type='scatter', name='Community fund', x=data['fundDFI'].dropna().index, y=data['fundDFI'].dropna(),
                             mode='lines', line=dict(color='#ff9800'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='CF')
        figDFI.add_trace(trace_fundDFI, 1, 1)

        trace_foundationDFI = dict(type='scatter', name='Foundation', x=data['foundationDFI'].dropna().index,
                                   y=data['foundationDFI'].dropna(),mode='lines', line=dict(color='#22b852'), line_width=3,
                                   hovertemplate='%{y:,.0f}', legendgroup='Found')
        figDFI.add_trace(trace_foundationDFI, 1, 1)

        trace_otherDFI = dict(type='scatter', name='Other', x=data['otherDFI'].dropna().index,
                              y=data['otherDFI'].dropna(), mode='lines', line=dict(color='#410eb2'), line_width=3,
                              hovertemplate='%{y:,.0f}', legendgroup='other')
        figDFI.add_trace(trace_otherDFI, 1, 1)

        trace_lmDFI = dict(type='scatter', name='Liquidity pool', x=data['lmDFI'].dropna().index, y=data['lmDFI'].dropna(),
                           mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:,.0f}', legendgroup='lm')
        figDFI.add_trace(trace_lmDFI, 1, 1)


        # relative DFI representation
        trace_relMnDFI = dict(type='scatter', name='', x=data['mnDFI'].dropna().index, y=data['mnDFI'].dropna() / data['totalDFI'].dropna() * 100,
                              mode='lines', line=dict(color='#f44235'), line_width=3, hovertemplate='%{y:,.1f} %', legendgroup='MN', showlegend=False)
        figDFI.add_trace(trace_relMnDFI, 2, 1)

        trace_relFundDFI = dict(type='scatter', name='', x=data['fundDFI'].dropna().index, y=data['fundDFI'].dropna() / data['totalDFI'].dropna() * 100,
                                mode='lines', line=dict(color='#ff9800'), line_width=3, hovertemplate='%{y:,.1f} %', legendgroup='CF', showlegend=False)
        figDFI.add_trace(trace_relFundDFI, 2, 1)

        trace_relFoundationDFI = dict(type='scatter', name='', x=data['totalDFI'].dropna().index, y=data['foundationDFI'].dropna() / data['totalDFI'].dropna() * 100,
                                      mode='lines', line=dict(color='#22b852'), line_width=3, hovertemplate='%{y:,.1f} %', legendgroup='Found', showlegend=False)
        figDFI.add_trace(trace_relFoundationDFI, 2, 1)

        trace_relOtherDFI = dict(type='scatter', name='', x=data['otherDFI'].dropna().index, y=data['otherDFI'].dropna() / data['totalDFI'].dropna() * 100,
                                 mode='lines', line=dict(color='#410eb2'), line_width=3, hovertemplate='%{y:,.1f} %', legendgroup='other', showlegend=False)
        figDFI.add_trace(trace_relOtherDFI, 2, 1)

        trace_relLMDFI = dict(type='scatter', name='', x=data['totalDFI'].dropna().index, y=data['lmDFI'].dropna() / data['totalDFI'].dropna() * 100,
                              mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:,.1f} %', legendgroup='lm', showlegend=False)
        figDFI.add_trace(trace_relLMDFI, 2, 1)

        figDFI.update_yaxes(title_text='DFI amount', tickformat=",.f", gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figDFI.update_yaxes(title_text='Rel. part in %', tickformat=",.1f", gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=2, col=1)
        figDFI.update_xaxes(gridcolor='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figDFI.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=2,
                            col=1)

        figDFI.update_layout(xaxis=dict(
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
        figDFI.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.79, sizex=0.45, sizey=0.45,  xanchor="center", yanchor="middle", opacity=0.2))
        figDFI.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.22, sizex=0.45, sizey=0.45, xanchor="center", yanchor="middle", opacity=0.2))

        figDFI.update_layout(height=790,
                             margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.1,
                                             xanchor="right",
                                             x=1),
                             )
        figDFI.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDFI.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDFI.layout.legend.font.color = '#6c757d'  # font color legend

        return figDFI

    @staticmethod
    def getCoinExplanation():
        coinCardExplanation = [html.P(['For tracking the amount of DFI and their distribution a snapshot of the DeFiChain richlist is made once a day (in the night).', html.Br(),
                                       html.A('http://explorer.defichain.io/#/DFI/mainnet/rich-list', href='http://explorer.defichain.io/#/DFI/mainnet/rich-list',
                                              target='_blank')], style={'text-align': 'justify'}),

                               html.P('The first diagram shows the absolute number of coins and their allocation.', style={'text-align': 'justify'}),
                               html.P([ 'The second diagram uses the same data base, but is a relative representation. Due to the fact that the DefiChain foundation no '
                                        'longer has masternodes their relative share is now steadily decreasing'],
                                      style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),
                                       ' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on '
                                       'the corresponding legend entry.'],
                                      style={'text-align': 'justify', 'fontSize': '0.7rem', 'color': '#6c757d'})]
        return coinCardExplanation