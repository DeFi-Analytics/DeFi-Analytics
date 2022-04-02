import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

class nbDTokenViewClass:

    def getnbDTokenContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Number dToken with Loans"),
                              dbc.ModalBody(self.getNbDTokenExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoNbDToken", className="ml-auto"))],
                                    id="modalNbDToken", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Number dTokens with Loans']),
                                          html.Table([html.Tr([html.Td('Select dToken for evaluation:'),
                                                               html.Td(dcc.Dropdown(id='vaultsLoansNbDtoken', options=[{'label': 'dUSD', 'value': 'DUSD'},
                                                                                                                         {'label': 'DFI in dUSD', 'value': 'DFI'},
                                                                                                                         {'label': 'AAPL', 'value': 'AAPL'},
                                                                                                                         {'label': 'AMZN', 'value': 'AMZN'},
                                                                                                                         {'label': 'ARKK', 'value': 'ARKK'},
                                                                                                                         {'label': 'BABA', 'value': 'BABA'},
                                                                                                                         {'label': 'COIN', 'value': 'COIN'},
                                                                                                                         {'label': 'DIS', 'value': 'DIS'},
                                                                                                                         {'label': 'EEM', 'value': 'EEM'},
                                                                                                                         {'label': 'FB', 'value': 'FB'},
                                                                                                                         {'label': 'GLD', 'value': 'GLD'},
                                                                                                                         {'label': 'GME', 'value': 'GME'},
                                                                                                                         {'label': 'GOOGL', 'value': 'GOOGL'},
                                                                                                                         {'label': 'INTC', 'value': 'INTC'},
                                                                                                                         {'label': 'MCHI', 'value': 'MCHI'},
                                                                                                                         {'label': 'MSFT', 'value': 'MSFT'},
                                                                                                                         {'label': 'MSTR', 'value': 'MSTR'},
                                                                                                                         {'label': 'NFLX', 'value': 'NFLX'},
                                                                                                                         {'label': 'NVDA', 'value': 'NVDA'},
                                                                                                                         {'label': 'PDBC', 'value': 'PDBC'},
                                                                                                                         {'label': 'PLTR', 'value': 'PLTR'},
                                                                                                                         {'label': 'QQQ', 'value': 'QQQ'},
                                                                                                                         {'label': 'SLV', 'value': 'SLV'},
                                                                                                                         {'label': 'SPY', 'value': 'SPY'},
                                                                                                                         {'label': 'TLT', 'value': 'TLT'},
                                                                                                                         {'label': 'TSLA', 'value': 'TSLA'},
                                                                                                                         {'label': 'URTH', 'value': 'URTH'},
                                                                                                                         {'label': 'VNQ', 'value': 'VNQ'},
                                                                                                                         {'label': 'VOO', 'value': 'VOO'},],
                                                                                    value='DUSD', clearable=False, style=dict(width='150px', verticalAlign="bottom")))])]),
                                          dcc.Graph(id='figureNbDToken', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoNbDToken")))
                                          ]))]
        return content


    @staticmethod
    def createNbDToken(data, bgImage, representation):
        figNbDToken = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        lastValidDate = datetime.utcfromtimestamp(data['sumLoan'+representation].dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        if representation=='DUSD':
            trace_dUSDLoans = dict(type='scatter', name='dUSD with loans', x=data['sumLoan'+representation].dropna().index, y=data['sumLoan'+representation].dropna(),
                                  mode='lines', line=dict(color='#ff7fd7'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f} dUSD', fill='tozeroy')
            trace_dUSDPaid = dict(type='scatter', name='dUSD without loans (paid with DFI)', x=data['DUSDpaidDFI'].dropna().index, y=data['DUSDpaidDFI'].dropna(),
                                  mode='lines', line=dict(color='#ffbfeb'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f} dUSD', fill='tonexty')
            trace_dUSDburnedFee = dict(type='scatter', name='burned dUSD with DEX-Fee', x=data['burnedDUSDDEX'].dropna().index, y=-data['burnedDUSDDEX'].dropna(),
                                  mode='lines', line=dict(color='#5d5d5d'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f} dUSD', fill='tonexty')
            trace_nbDToken = dict(type='scatter', name='number circulating dTokens',
                                  x=(data['sumLoan'+representation]+data['DUSDpaidDFI'].fillna(0)-data['burnedDUSDDEX'].fillna(0)).dropna().index,
                                  y=(data['sumLoan'+representation]+data['DUSDpaidDFI'].fillna(0)-data['burnedDUSDDEX'].fillna(0)).dropna(),
                                     mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:,.f}')

            figNbDToken.add_trace(trace_dUSDLoans, 1, 1)
            figNbDToken.add_trace(trace_dUSDPaid, 1, 1)
            figNbDToken.add_trace(trace_dUSDburnedFee, 1, 1)
            figNbDToken.add_trace(trace_nbDToken, 1, 1)
        else:
            trace_nbDToken = dict(type='scatter', name='number circulating dTokens', x=data['sumLoan'+representation].dropna().index, y=data['sumLoan'+representation].dropna(),
                                     mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:,.f}')
            figNbDToken.add_trace(trace_nbDToken, 1, 1)

        figNbDToken.update_yaxes(title_text='number dTokens in Loans', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figNbDToken.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d',
                               range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figNbDToken.update_layout(xaxis=dict(
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

        figNbDToken.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))

        figNbDToken.update_layout(margin={"t": 60, "l": 0, "b": 0, "r": 0},
                                barmode='stack',
                                hovermode='x unified',
                                hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                legend=dict(orientation="h",
                                            yanchor="top",
                                            y=-0.12,
                                            xanchor="right",
                                            x=1),
                                )
        figNbDToken.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figNbDToken.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figNbDToken.layout.legend.font.color = '#6c757d'  # font color legend
        return figNbDToken


    @staticmethod
    def getNbDTokenExplanation():
        dTokenPricesCardExplanation = [html.P(['Everyone can mint dTokens on DefiChain by putting a collateral in form of DFI or other crypto coins into a vault. This graph shows'
                                               ' the number of dTokens for the selected ticker symbol with a loan in the background, which means the vault is still active and '
                                               'not in liquidation. '],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return dTokenPricesCardExplanation