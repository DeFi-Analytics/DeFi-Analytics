import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from plotly.subplots import make_subplots

from datetime import datetime
import dateutil.relativedelta


class transactionsViewClass:

    def getTransactionsContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Transactions"),
                              dbc.ModalBody(self.getTxOverviewExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoTransactions", className="ml-auto"))],
                                    id="modalTransactions", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Transactions on a daily base']),
                                          html.Table([html.Tr([html.Td('Select time base for representation:'),
                                                               html.Td(dcc.Dropdown(id='transactionSelection',
                                                                                    options=[{'label': 'Daily Transactions', 'value': 'D'},
                                                                                             {'label': 'Weekly Transactions', 'value': 'W'}],
                                                                                    value='D', clearable=False, style=dict(width='180px', verticalAlign="bottom")))])]),
                                          dbc.Row(dbc.Col(dcc.Graph(config={'displayModeBar': False}, id='figureTransactions'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoTransactions")))
                                          ]))]
        return content

    @staticmethod
    def createTransactionsFigure(data, bgImage, representation):
        figTxOverview = make_subplots(
            rows=2, cols=1,
            vertical_spacing=0.15,
            row_width=[0.55, 0.45],  # from bottom to top
            specs=[[{}],
                   [{}]],
            shared_xaxes=True)

        tempData = data[['txCount', 'txWOreward']].copy()
        tempData.index = pd.to_datetime(tempData.index) # change index from object to datetime for groupby function

        if representation == 'W':
            timeBase4tps = (7 * 24 * 60 * 60)
        else:
            timeBase4tps = (24 * 60 * 60)

        lastValidDate = datetime.strptime(tempData['txCount'].dropna().groupby(pd.Grouper(freq=representation)).sum().index.strftime('%Y-%m-%d').values[-2], '%Y-%m-%d')
        date30DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=30)

        trace_allTx = dict(type='scatter', name='all Tx',
                           x=tempData['txCount'].dropna().groupby(pd.Grouper(freq=representation)).sum().index.strftime('%Y-%m-%d').values[:-1],
                           y=tempData['txCount'].dropna().groupby(pd.Grouper(freq=representation)).sum().values[:-1],
                           mode='lines', line=dict(color='#da3832'), line_width=2, hovertemplate='%{y:,.0f}')

        trace_TxWOReward = dict(type='scatter', name='Tx without rewards',
                                x=tempData['txWOreward'].dropna().groupby(pd.Grouper(freq=representation)).sum().index.strftime('%Y-%m-%d').values[:-1],
                                y=tempData['txWOreward'].dropna().groupby(pd.Grouper(freq=representation)).sum().values[:-1],
                                mode='lines', line=dict(color='#ff9800'), line_width=2, hovertemplate='%{y:,.0f}')

        figTxOverview.add_trace(trace_allTx, 1, 1)
        figTxOverview.add_trace(trace_TxWOReward, 1, 1)

        trace_tps = dict(type='scatter', name='TPS (all Tx)',
                         x=tempData['txCount'].dropna().groupby(pd.Grouper(freq=representation)).sum().index.strftime('%Y-%m-%d').values[:-1],
                         y=tempData['txCount'].dropna().groupby(pd.Grouper(freq=representation)).sum().values[:-1]/timeBase4tps,
                         mode='lines', line=dict(color='#22b852'), line_width=2, hovertemplate='%{y:.3f}')
        figTxOverview.add_trace(trace_tps, 2, 1)

        figTxOverview.update_yaxes(title_text='# transactions / day', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1,
                                   col=1)  # ,range=[-50, 200]
        figTxOverview.update_yaxes(title_text='Transactions per second (TPS)', tickformat=",.2f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=2,
                                   col=1)  # ,range=[-200000, 1000000]
        figTxOverview.update_xaxes(gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                                   range=[date30DaysBack, lastValidDate], row=1, col=1)
        figTxOverview.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                                   range=[date30DaysBack, lastValidDate], row=2, col=1)

        # Add range slider
        figTxOverview.update_layout(xaxis=dict(
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
        figTxOverview.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.87, sizex=0.4, sizey=0.4,  xanchor="center", yanchor="middle", opacity=0.2))
        figTxOverview.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.3, sizex=0.4, sizey=0.4, xanchor="center", yanchor="middle", opacity=0.2))

        figTxOverview.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                                    hovermode='x unified',
                                    hoverlabel=dict(font_color="#6c757d"),
                                    legend=dict(orientation="h",
                                                yanchor="top",
                                                y=-0.12,
                                                xanchor="right",
                                                x=1),
                                    )
        figTxOverview.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figTxOverview.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figTxOverview.layout.legend.font.color = '#6c757d'  # font color legend

        return figTxOverview

    @staticmethod
    def getTxOverviewExplanation():
        coinAddressCardExplanation = [
                               html.P(['On this tab the number of transactions on the DefiChain is tracked. With the help of the API a database is generated, where for each block ',
                                       'the number of done transactions is saved. At least one transaction is included in every block, the one for sending the reward to the masternode. ',html.Br(),                                       'All the other included transactions are done by users or (later) smart contracts transferring DFI-coins. Especially at the beginning of DefiChain ',
                                       'the number of these transactions is very low (see orange line). The red line in the first graphs shows the overall made transactions per day.'],style={'text-align': 'justify'}),
                               html.P(['The second diagram visualizes the key figure ',html.I('Transactions per seconds (TPS)'),'. According to DefiChain''s Whitepaper, the blockchain is designed ',
                                       'for an average value of 1070 tps. So, before starting liquidity mining and DEX the value is far away from the design.'],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return coinAddressCardExplanation