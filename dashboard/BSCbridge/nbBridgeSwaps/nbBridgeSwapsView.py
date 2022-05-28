import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from datetime import datetime
import dateutil.relativedelta

from plotly.subplots import make_subplots
import pandas as pd


class nbBridgeSwapsViewClass:

    def getNbBrideSwapsContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Number swaps BSC-Bridge"),
                              dbc.ModalBody(self.getNbSwapsExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoBSCnbSwaps", className="ml-auto"))],
                                    id="modalBSCnbSwaps", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Number swaps BSC-Bridge']),
                                          html.Table([html.Tr([html.Td('Select time base for representation:'),
                                                               html.Td(dcc.Dropdown(id='BSCnbSwapsSelection',
                                                                                    options=[{'label': 'Hourly number swaps', 'value': 'H'},
                                                                                             {'label': 'Daily number swaps', 'value': 'D'},
                                                                                             {'label': 'Weekly number swaps', 'value': 'W'}],
                                                                                    value='H', clearable=False, style=dict(width='200px', verticalAlign="bottom")))])]),
                                          dbc.Row(dbc.Col(dcc.Graph(config={'displayModeBar': False}, id='figureBSCnbSwaps'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoBSCnbSwaps")))
                                          ]))]
        return content

    @staticmethod
    def createBSCNbSwapsFig(data, bgImage, representation):
        figBSCnbSwaps = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        totalNb = (data['bridgeNbInSwaps']+data['bridgeNbOutSwaps']).dropna()

        if representation == 'W':
            days2show = 90
        elif representation == 'D':
            days2show = 30
        else:
            days2show = 7

        lastValidDate = datetime.utcfromtimestamp(totalNb.dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=days2show)

        trace_totalNb = dict(type='scatter', name='Total number swaps', x=totalNb.dropna().groupby(pd.Grouper(freq=representation)).sum().index, y=totalNb.groupby(pd.Grouper(freq=representation)).sum().dropna(),
                         mode='lines', line=dict(color='#ff00af'), line_width=2, hovertemplate='%{y:,.0f}')

        # individual swap numbers
        trace_nbInBridge = dict(type='scatter', name='Number swaps to BSC',
                                x=data['bridgeNbInSwaps'].dropna().groupby(pd.Grouper(freq=representation)).sum().index,
                                y=data['bridgeNbInSwaps'].dropna().groupby(pd.Grouper(freq=representation)).sum(),
                                 mode='lines', line=dict(color='#ff7fd7'), line_width=0, stackgroup='one', hovertemplate='%{y:,.0f}', fill='tozeroy')
        trace_nbOutBridge = dict(type='scatter', name='Number swaps from BSC',
                                 x=data['bridgeNbOutSwaps'].dropna().groupby(pd.Grouper(freq=representation)).sum().index,
                                 y=data['bridgeNbOutSwaps'].dropna().groupby(pd.Grouper(freq=representation)).sum(),
                                    mode='lines', line=dict(color='#ffbfeb'), line_width=0, stackgroup='one', hovertemplate='%{y:,.0f}', fill='tonexty')

        figBSCnbSwaps.add_trace(trace_nbInBridge, 1, 1)
        figBSCnbSwaps.add_trace(trace_nbOutBridge, 1, 1)
        figBSCnbSwaps.add_trace(trace_totalNb, 1, 1)


        figBSCnbSwaps.update_yaxes(title_text='Number swaps BSC-Bridge', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)  # ,range=[-50, 200]
        figBSCnbSwaps.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figBSCnbSwaps.update_layout(xaxis=dict(
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
        figBSCnbSwaps.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figBSCnbSwaps.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d",
                                             bgcolor='#ffffff', ),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )
        figBSCnbSwaps.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figBSCnbSwaps.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figBSCnbSwaps.layout.legend.font.color = '#6c757d'  # font color legend

        return figBSCnbSwaps

    @staticmethod
    def getNbSwapsExplanation():
        nbSwapsCardExplanation = [html.P(['For transferring DFI from DeFiChain to BNC Smart Chain you have to do a bridge swap. For that you are sending DFI to a smart contract address. '
                                          'These coins are locked and the same amount BEP20-token are minted. In this evaluation the number of swaps - regardless the amount - '
                                          'is counted and shown on different time base. Beside the absolut number the bridge swaps from or to BSC is shown. '],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return nbSwapsCardExplanation