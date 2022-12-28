import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta


class lockViewClass:

    def getLOCKContent(self):
        content = [dbc.Card(dbc.CardBody([html.H4(['Community Project: LOCK']),
                                          html.P(['Defichain has a great community. More and more persons create their own projects to help others and bring value into the ecosystem.',html.Br(),
                                                  'The service of LOCK was set up to have an easy way to invest. You can put your DFI into staking or dUSD into dUSD Yield Machine. ',
                                                  'The company in the background will handle the corresponding masternodes and vaults.',
                                                  html.Br(),
                                                  'You want to know more? Have a look on: ',
                                                  html.A('https://lock.space/', href='https://lock.space/', target='_blank', className='defiLink')],
                                                 style={'text-align': 'justify'}),
                                          html.Table([html.Tr([html.Td('Select service:'),
                                                               html.Td(dcc.Dropdown(id='lockSelectService', options=[{'label': 'DFI staking', 'value': 'DFI'},
                                                                                                                     {'label': 'dUSD Yield Machine', 'value': 'DUSD'}],
                                                                                    value='DFI', clearable=False, style=dict(verticalAlign="bottom")))]),
                                                    html.Tr([html.Td('Select graph for evaluation:'),
                                                               html.Td(dcc.Dropdown(id='lockSelectGraph', options=[{'label': 'Total investment', 'value': 'totalInvestment'},
                                                                                                                   {'label': 'Daily change', 'value': 'dailyChange'}],
                                                                                    value='totalInvestment', clearable=False, style=dict(verticalAlign="bottom")))]),
                                                              ]),
                                          dcc.Graph(id='figureLOCKdata', config={'displayModeBar': False})]))]
        return content

    @staticmethod
    def createLOCKFigure(data, bgImage, serviceSelection, graphSelection):
        figLOCK = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))
        ['DFIdepositsLOCK', 'DFIwithdrawalsLOCK', 'DUSDdepositsLOCK', 'DUSDwithdrawalsLOCK']

        formatHover = '%{y:,.2f}'
        if graphSelection=='totalInvestment':
            ydata = data[serviceSelection+'depositsLOCK'].cumsum()-data[serviceSelection+'withdrawalsLOCK'].cumsum()
            trace_total = dict(type='scatter', name='TVL', x=ydata.dropna().index, y=ydata.dropna(),
                          mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate=formatHover)
            figLOCK.add_trace(trace_total, 1, 1)

        else:
            ydataDeposit = data[serviceSelection+'depositsLOCK'].cumsum().groupby(data['dfxBuyVolume'].index.floor('d')).last().diff()
            ydataWithdrawal = data[serviceSelection+'withdrawalsLOCK'].cumsum().groupby(data['dfxSellVolume'].index.floor('d')).last().diff()

            trace_diff = dict(type='scatter', name='Daily difference', x=(ydataDeposit - ydataWithdrawal).dropna().index, y=(ydataDeposit - ydataWithdrawal).dropna(),
                              mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate=formatHover)
            trace_deposit = dict(type='scatter', name='Daily Deposits', x=ydataDeposit.dropna().index, y=ydataDeposit.dropna(),
                             mode='lines', line=dict(color='#90dba8'), line_width=3, hovertemplate=formatHover, fill='tozeroy')
            trace_withdrawal = dict(type='scatter', name='Daily Withdrawals', x=ydataWithdrawal.dropna().index, y=-ydataWithdrawal.dropna(),
                              mode='lines', line=dict(color='#ec9b98'), line_width=3, hovertemplate=formatHover, fill='tozeroy')

            figLOCK.add_trace(trace_deposit, 1, 1)
            figLOCK.add_trace(trace_withdrawal, 1, 1)
            figLOCK.add_trace(trace_diff, 1, 1)

        lastValidDate = datetime.utcfromtimestamp(data['DFIdepositsLOCK'].dropna().index.values[-1].tolist() / 1e9)
        dateGoBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)


        figLOCK.update_yaxes(title_text='Number coins', tickformat=",.f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figLOCK.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', range=[dateGoBack, lastValidDate], row=1, col=1)
        figLOCK.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))

        # Add range slider
        figLOCK.update_layout(barmode='stack',
            xaxis=dict(
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

        figLOCK.update_layout(margin={"t": 50, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figLOCK.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figLOCK.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figLOCK.layout.legend.font.color = '#6c757d'  # font color legend
        return figLOCK

