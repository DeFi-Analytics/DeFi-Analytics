import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

class aprViewClass:

    def getAPRContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info APR Rates"),
                              dbc.ModalBody(self.getAPRExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoAPR", className="ml-auto"))], id="modalAPR", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['APR rates liquidity mining']),
                                          html.Table([html.Tr([html.Td('Select pool for plotting apr rate:'),
                                          html.Td(dcc.Dropdown(id='APRSelection',options=[
                                            {'label':'BTC','value':'BTC-DFI'},
                                            {'label':'ETH','value':'ETH-DFI'},
                                            {'label':'USDT','value':'USDT-DFI'},
                                            {'label':'DOGE','value':'DOGE-DFI'},
                                            {'label':'LTC','value':'LTC-DFI'},
                                            {'label':'BCH','value':'BCH-DFI'},
                                            {'label':'USDC','value':'USDC-DFI'},
                                            {'label': 'dUSD', 'value': 'DUSD-DFI'},
                                            {'label': 'AAPL', 'value': 'AAPL-DUSD'},
                                            {'label': 'AMZN', 'value': 'AMZN-DUSD'},
                                            {'label': 'ARKK', 'value': 'ARKK-DUSD'},
                                            {'label': 'BABA', 'value': 'BABA-DUSD'},
                                            {'label': 'COIN', 'value': 'COIN-DUSD'},
                                            {'label': 'EEM', 'value': 'EEM-DUSD'},
                                            {'label': 'FB', 'value': 'FB-DUSD'},
                                            {'label': 'GLD', 'value': 'GLD-DUSD'},
                                            {'label': 'GME', 'value': 'GME-DUSD'},
                                            {'label': 'GOOGL', 'value': 'GOOGL-DUSD'},
                                            {'label': 'MSFT', 'value': 'MSFT-DUSD'},
                                            {'label': 'NFLX', 'value': 'NFLX-DUSD'},
                                            {'label': 'NVDA', 'value': 'NVDA-DUSD'},
                                            {'label': 'PDBC', 'value': 'PDBC-DUSD'},
                                            {'label': 'PLTR', 'value': 'PLTR-DUSD'},
                                            {'label': 'QQQ', 'value': 'QQQ-DUSD'},
                                            {'label': 'SLV', 'value': 'SLV-DUSD'},
                                            {'label': 'SPY', 'value': 'SPY-DUSD'},
                                            {'label': 'TLT', 'value': 'TLT-DUSD'},
                                            {'label': 'TSLA', 'value': 'TSLA-DUSD'},
                                            {'label': 'URTH', 'value': 'URTH-DUSD'},
                                            {'label': 'VNQ', 'value': 'VNQ-DUSD'},
                                            {'label': 'VOO', 'value': 'VOO-DUSD'},
                                          ],
                                            value='BTC-DFI', clearable=False, style=dict(width='200px',verticalAlign="bottom")))])]),
                            dbc.Col(dcc.Graph(id = 'figureAPRRate', config={'displayModeBar': False})),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoAPR")))]))]
        return content

    @staticmethod
    def createAPRGraph(data, selectedCoin, bgImage):
        figAPR = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        lastValidDate = datetime.utcfromtimestamp(data['BTC-DFI_lockedDFI'].dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        # complete APR rate
        trace_APR = dict(type='scatter', name='Overall', x=(data[selectedCoin+'_APRblock']+data[selectedCoin+'_APRcommission']).dropna().index,
                         y=(data[selectedCoin+'_APRblock']+data[selectedCoin+'_APRcommission']).dropna()*100,
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:,.2f}%')
        # individual apr rates
        trace_Block = dict(type='scatter', name='Block rewards',x=data[selectedCoin+'_APRblock'].dropna().index, y=data[selectedCoin+'_APRblock'].dropna()*100,
                                 mode='lines', line=dict(color='#ff7fd7'), line_width=0, stackgroup='one', hovertemplate='%{y:,.2f}%', fill='tozeroy')
        trace_Commission = dict(type='scatter', name='Commissions', x=data[selectedCoin+'_APRcommission'].dropna().index, y=data[selectedCoin+'_APRcommission'].dropna()*100,
                                    mode='lines', line=dict(color='#ffbfeb'), line_width=0, stackgroup='one', hovertemplate='%{y:,.2f}%', fill='tonexty')

        figAPR.add_trace(trace_Block, 1, 1)
        figAPR.add_trace(trace_Commission, 1, 1)
        figAPR.add_trace(trace_APR, 1, 1)

        figAPR.update_yaxes(title_text='APR rate in % for ' + selectedCoin + ' pool', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                                       zerolinecolor='#6c757d', row=1, col=1)
        figAPR.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                                       range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figAPR.update_layout(xaxis=dict(
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
        figAPR.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6, xanchor="center", yanchor="middle", opacity=0.2))

        figAPR.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                                        hovermode='x unified',
                                        hoverlabel=dict(font_color="#6c757d",
                                                        bgcolor='#ffffff', ),
                                        legend=dict(orientation="h",
                                                    yanchor="top",
                                                    y=-0.12,
                                                    xanchor="right",
                                                    x=1),
                                        )

        figAPR.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figAPR.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figAPR.layout.legend.font.color = '#6c757d'  # font color legend

        return figAPR

    @staticmethod
    def getAPRExplanation():
        aprExplanation = [html.P(['An incentive is created for providing liquidity in the DEX pools by two factors:',
                                  html.Ul([html.Li(['DFI block rewards emissioned by the consensus algorithm. This part will go down over time (see emission evaluation).', html.Br(),
                                           'The crypto pools have a fix ratio, while the dTokens are reallocated after listing new dTokens.']),
                                           html.Li('Commissions, which are the fees paid by the DEX users. This part increases with DEX usage and will be the incentive when block rewards are (nearly) zero.')])
                                  ],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return aprExplanation