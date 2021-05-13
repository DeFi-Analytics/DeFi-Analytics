import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from datetime import datetime
import dateutil.relativedelta

from plotly.subplots import make_subplots


class marketcapViewClass:

    def getMarketcapContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info DefiChain Market Cap"),
                              dbc.ModalBody(self.getMarketcapExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoMarketcap", className="ml-auto"))],
                                    id="modalMarketcap", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['DefiChain Market Cap']),
                                          html.Table([html.Tr([html.Td('Select currency for Market Cap representation:'),
                                                               html.Td(dcc.Dropdown(id='marketCapCurrencySelection', options=[{'label': 'USD', 'value': 'USD'},
                                                                                                                   {'label': 'BTC', 'value': 'BTC'}],
                                                                                    value='USD', clearable=False, style=dict(width='150px', verticalAlign="bottom")))])]),
                                          dbc.Col(dcc.Graph(config={'displayModeBar': False}, id='figureMarketcap')),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoMarketcap")))
                                          ]))]
        return content

    @staticmethod
    def createMarketCapFig(data, selection, bgImage):
        figMarketcap = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))
        if selection == 'BTC':
            columnName = 'marketCapBTC'
            yAxisLabel = 'Market Cap in BTC'
            hoverTemplateRepresenation = '%{y:,.2f}BTC'
        else:
            columnName = 'marketCapUSD'
            yAxisLabel = 'Market Cap in $'
            hoverTemplateRepresenation = '$%{y:,.0f}'

        lastValidDate = datetime.strptime(data[columnName].dropna().index.values[-2], '%Y-%m-%d')
        date2MonthsBack = lastValidDate - dateutil.relativedelta.relativedelta(months=2)

        trace_marketcap = dict(type='scatter', name='DAA',
                         x=data[columnName].dropna().index.values[:-1], y=data[columnName].dropna().values[:-1],
                         mode='lines', line=dict(color='#ff00af'), line_width=2, hovertemplate=hoverTemplateRepresenation)
        figMarketcap.add_trace(trace_marketcap, 1, 1)

        figMarketcap.update_yaxes(title_text=yAxisLabel, tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1,
                            col=1)  # ,range=[-50, 200]
        figMarketcap.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date2MonthsBack.strftime('%Y-%m-%d'), lastValidDate], row=1, col=1)

        # Add range slider
        figMarketcap.update_layout(xaxis=dict(
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
        figMarketcap.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figMarketcap.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d",
                                             bgcolor='#ffffff', ),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )
        figMarketcap.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figMarketcap.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figMarketcap.layout.legend.font.color = '#6c757d'  # font color legend

        return figMarketcap

    @staticmethod
    def getMarketcapExplanation():
        mcCardExplanation = [html.P(['The market cap of a cryptocurrency coin is the product of the circulating coin amount and the coin price. It is used to compare coins against each other, '
                                     'because the price alone has no meaning. Beside the common used USD representation, you can also choose a BTC representation. Due to the strong correlation '
                                     'of DFI and BTC, this could give more insights in the development of DefiChain.' ],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return mcCardExplanation