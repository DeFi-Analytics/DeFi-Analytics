import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

class interestViewClass:

    def getInterestContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Accumulated open interest in loans"),
                              dbc.ModalBody(self.getInterestExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoInterest", className="ml-auto"))],
                                    id="modalInterest", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Accumulated open interest in loans']),
                                          html.Table([html.Tr([html.Td('Select currency for the representation:'),
                                                               html.Td(dcc.Dropdown(id='vaultsLoansInterest', options=[{'label': 'USD', 'value': 'USD'},
                                                                                                                         {'label': 'DFI', 'value': 'DFI'},],
                                                                                    value='USD', clearable=False, style=dict(width='150px', verticalAlign="bottom")))])]),
                                          dcc.Graph(id='figureInterest', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoInterest")))
                                          ]))]
        return content


    @staticmethod
    def createInterest(data, bgImage, representation):
        figNbDToken = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        if representation == 'DFI':
            price = 1/data['USDT-DFI_DFIPrices']
        else:
            price = data['USDT-DFI_DFIPrices']/data['USDT-DFI_DFIPrices']


        lastValidDate = datetime.utcfromtimestamp(data['sumInterest'].dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        trace_nbDToken = dict(type='scatter', name='DEX price in dUSD', x=(data['sumInterest']*price).dropna().index, y=(data['sumInterest']*price).dropna(),
                                 mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:.f}')

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
    def getInterestExplanation():
        interestCardExplanation = [html.P(['Depending on the loan scheme every user has to pay an interest for minted dTokens. They are accumulated in the loan and will be paid back first. '
                                           'This graph shows the current accumulated and open interest in all loans. The user can also select the if the value should be shown in USD or in DFI. '
                                           'After paying the interest the corresponding dTokens will be swapped to DFI and be burned. '],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return interestCardExplanation