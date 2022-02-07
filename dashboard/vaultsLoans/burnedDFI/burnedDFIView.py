import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

class burnedDFIViewClass:
    def __init__(self):
        None

    def getBurnedDFIContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info Burned DFI Vaults & Loans"),
                              dbc.ModalBody(self.getBurnedDFIExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoBurnedDFI", className="ml-auto"))],
                                    id="modalBurnedDFI", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Burned DFI Vaults & Loans']),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createBurnedDFIFigure(data, bgImage), config={'displayModeBar': False}, id='figureBurnedDFI'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoBurnedDFI")))
                                          ]))]
        return content

    @staticmethod
    def createBurnedDFIFigure(data, bgImage):
        figBurnedDFI = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        lastValidDate = datetime.utcfromtimestamp(data['burnedAuction'].dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        # generate over addresses
        trace_OverallBurned = dict(type='scatter', name='Overall', x=(data['burnedAuction']+data['burnedPayback']+data['burnedDFIPayback'].fillna(0)).dropna().index,
                                                                   y=(data['burnedAuction']+data['burnedPayback']+data['burnedDFIPayback'].fillna(0)).dropna(),
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:,.f} DFI')

        # generate specific addresses
        trace_DFIPaybackBurn = dict(type='scatter', name='dUSD payback with DFI',x=data['burnedDFIPayback'].dropna().index, y=(data['burnedDFIPayback']*(1+99)).dropna(),
                                 mode='lines', line=dict(color='#f800aa'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f} DFI', fill='tozeroy')

        trace_AuctionBurned = dict(type='scatter', name='Auction fee',x=data['burnedAuction'].dropna().index, y=data['burnedAuction'].dropna(),
                                 mode='lines', line=dict(color='#ff7fd7'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f} DFI', fill='tonexty')

        trace_PaybackBurn = dict(type='scatter', name='Interest dToken payback', x=data['burnedPayback'].dropna().index, y=(data['burnedPayback']-data['burnedDFIPayback'].fillna(0)*99).dropna(),
                                    mode='lines', line=dict(color='#ffbfeb'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f} DFI', fill='tonexty')

        figBurnedDFI.add_trace(trace_DFIPaybackBurn, 1, 1)
        figBurnedDFI.add_trace(trace_AuctionBurned, 1, 1)
        figBurnedDFI.add_trace(trace_PaybackBurn, 1, 1)
        figBurnedDFI.add_trace(trace_OverallBurned, 1, 1)

        figBurnedDFI.update_yaxes(title_text='Burned DFI', tickformat=",.f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figBurnedDFI.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d',
                               range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        figBurnedDFI.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        # Add range slider
        figBurnedDFI.update_layout(xaxis=dict(
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

        figBurnedDFI.update_layout(margin={"t": 20, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d"),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figBurnedDFI.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figBurnedDFI.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figBurnedDFI.layout.legend.font.color = '#6c757d'  # font color legend
        return figBurnedDFI

    @staticmethod
    def getBurnedDFIExplanation():
        burnedDFICardExplanation = [html.P(['The vaults and loans feature on DefiChain has two different DFI burn mechanisms implemented:',
                                            html.Ul([html.Li('Auction fee: Everyone bidding on a vault has to pay a fee of 5% in form of the dToken in the corresponding loan. These '
                                                             'dToken will be swapped into DFI and burned.'),
                                                     html.Li('Interest dToken payback: With selection of the loan scheme the user chooses an interest rate. The accumulated interests must be paid before paying back the loan. '
                                                             'These dToken will be swapped into DFI and burned.'),
                                                     html.Li('dUSD payback with DFI: With Fort Canning Hill update user can payback their dUSD loans with DFI. The complete amount (loan+interest+fee) of DFI will be burned.')
                                                     ]),
                                            ], style={'text-align': 'justify'}),
                                  html.P([html.B('Hint:'),
                                          ' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                          ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                         style={'text-align': 'justify', 'fontSize': '0.7rem', 'color': '#6c757d'})
                                  ]
        return burnedDFICardExplanation
