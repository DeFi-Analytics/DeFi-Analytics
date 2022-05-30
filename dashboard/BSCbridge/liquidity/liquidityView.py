import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from datetime import datetime
import dateutil.relativedelta

from plotly.subplots import make_subplots


class liquidityViewClass:

    def getLiquidityContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info Liquidity BSC-Bridge"),
                              dbc.ModalBody(self.getLiquidityExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoBSCLiquidity", className="ml-auto"))],
                                    id="modalBSCLiquidity", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Liquidity BSC-Bridge']),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createBSCLiquidityFig(data, bgImage), config={'displayModeBar': False}, id='figureBSCLiquidity'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoBSCLiquidity")))
                                          ]))]
        return content



    @staticmethod
    def createBSCLiquidityFig(data, bgImage):
        figBSCLiquidity = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        bridgeBalance = (data['bridgeInflow']+data['bridgeOutflow'].fillna(0)).cumsum()

        lastValidDate = datetime.utcfromtimestamp(bridgeBalance.dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)


        trace_balance = dict(type='scatter', name='Liquidity', x=bridgeBalance.dropna().index, y=bridgeBalance.dropna(),
                         mode='lines', line=dict(color='#ff00af'), line_width=2, hovertemplate='%{y:,.8f} DFI')

        figBSCLiquidity.add_trace(trace_balance, 1, 1)


        figBSCLiquidity.update_yaxes(title_text='Number DFI locked in bridge', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)  # ,range=[-50, 200]
        figBSCLiquidity.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figBSCLiquidity.update_layout(xaxis=dict(
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
        figBSCLiquidity.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figBSCLiquidity.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d",
                                             bgcolor='#ffffff', ),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )
        figBSCLiquidity.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figBSCLiquidity.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figBSCLiquidity.layout.legend.font.color = '#6c757d'  # font color legend

        return figBSCLiquidity

    @staticmethod
    def getLiquidityExplanation():
        liquidityCardExplanation = [html.P(['For sending DFI from DefiChain to BNB Smart Chain the amount of coins are locked on the DefiChain address 8Jgfq4pBUdJLiFGStunoTCy2wqRQphP6bQ and the corresponding amount of '
                                            'BEP20-token is minted. This graph shows the holding of DFI on the bridge address, which corresponds to the amount of DFI on BNB Smart Chain.'],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return liquidityCardExplanation