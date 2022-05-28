import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from datetime import datetime
import dateutil.relativedelta

from plotly.subplots import make_subplots
import pandas as pd


class inOutFlowViewClass:

    def getInOutFlowContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info BSC-Bridge in- and outflows"),
                              dbc.ModalBody(self.getInOutFlowExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoBSCInOutFlow", className="ml-auto"))],
                                    id="modalBSCInOutFlow", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['BSC-Bridge in- and outflows']),
                                          html.Table([html.Tr([html.Td('Select time base for representation:'),
                                                               html.Td(dcc.Dropdown(id='BSCInOutFlowSelection',
                                                                                    options=[{'label': 'Hourly number swaps', 'value': 'H'},
                                                                                             {'label': 'Daily number swaps', 'value': 'D'},
                                                                                             {'label': 'Weekly number swaps', 'value': 'W'}],
                                                                                    value='H', clearable=False, style=dict(width='200px', verticalAlign="bottom")))])]),
                                          dbc.Row(dbc.Col(dcc.Graph(config={'displayModeBar': False}, id='figureBSCInOutFlow'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoBSCInOutFlow")))
                                          ]))]
        return content

    @staticmethod
    def createBSCInOutFlowFig(data, bgImage, representation):
        figBSCInOutFlow = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        diffInOutFlow = (data['bridgeInflow']+data['bridgeOutflow'].fillna(0)).dropna()

        if representation == 'W':
            days2show = 90
        elif representation == 'D':
            days2show = 30
        else:
            days2show = 7

        lastValidDate = datetime.utcfromtimestamp(diffInOutFlow.dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=days2show)

        trace_diffInOutFlow = dict(type='scatter', name='Change bridge liquidity', x=diffInOutFlow.dropna().groupby(pd.Grouper(freq=representation)).sum().index, y=diffInOutFlow.groupby(pd.Grouper(freq=representation)).sum().dropna(),
                         mode='lines', line=dict(color='#ff00af'), line_width=2, hovertemplate='%{y:,.0f}')

        # individual swap numbers
        trace_InFlow = dict(type='scatter', name='Bridge inflow (DeFiChain → BSC)',
                                x=data.loc[diffInOutFlow.index, 'bridgeInflow'].fillna(0).groupby(pd.Grouper(freq=representation)).sum().index,
                                y=data.loc[diffInOutFlow.index, 'bridgeInflow'].fillna(0).groupby(pd.Grouper(freq=representation)).sum(),
                                 mode='lines', line=dict(color='#90dba8'), line_width=0, hovertemplate='%{y:,.8f}', fill='tozeroy')
        trace_OutFlow = dict(type='scatter', name='Bridge outflow (BSC → DeFiChain)',
                             x=data.loc[diffInOutFlow.index, 'bridgeOutflow'].fillna(0).groupby(pd.Grouper(freq=representation)).sum().index,
                             y=data.loc[diffInOutFlow.index, 'bridgeOutflow'].fillna(0).groupby(pd.Grouper(freq=representation)).sum(),
                                    mode='lines', line=dict(color='#ec9b98'), line_width=0, hovertemplate='%{y:,.8f}', fill='tozeroy')


        figBSCInOutFlow.add_trace(trace_InFlow, 1, 1)
        figBSCInOutFlow.add_trace(trace_OutFlow, 1, 1)
        figBSCInOutFlow.add_trace(trace_diffInOutFlow, 1, 1)

        figBSCInOutFlow.update_yaxes(title_text='Number swaps BSC-Bridge', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)  # ,range=[-50, 200]
        figBSCInOutFlow.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figBSCInOutFlow.update_layout(xaxis=dict(
            rangeselector=dict(
                buttons=list([dict(count=7, label="7d", step="day", stepmode="backward"),
                              dict(count=14, label="14d", step="day", stepmode="backward"),
                              dict(count=30, label="30d", step="day", stepmode="backward"),
                              dict(count=2, label="2m", step="month", stepmode="backward"),
                              dict(count=6, label="6m", step="month", stepmode="backward"),
                              dict(count=1, label="YTD", step="year", stepmode="todate"),
                              dict(count=1, label="1y", step="year", stepmode="backward"),
                              dict(step="all")])),
            rangeslider=dict(visible=False),
            type="date"))

        # add background picture
        figBSCInOutFlow.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figBSCInOutFlow.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d",
                                             bgcolor='#ffffff', ),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )
        figBSCInOutFlow.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figBSCInOutFlow.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figBSCInOutFlow.layout.legend.font.color = '#6c757d'  # font color legend

        return figBSCInOutFlow

    @staticmethod
    def getInOutFlowExplanation():
        inOutFlowExplanation = [html.P(['This evaluation tracks the capital flow trough the BSC bridge, which is needed to get DFI as BEP20-token on BNB smart chain. '
                                        'The DFI inflow means, that DFI were deposited on the smart contract address on DeFiChain and BEP2ß DFI were minted. And with that the '
                                        'outflow is the opposite direction, means a user is sending BEP20 to DeFiChain trough the bridge.'],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return inOutFlowExplanation