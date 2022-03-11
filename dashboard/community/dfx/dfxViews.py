import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta


class dfxViewClass:

    def getDFXContent(self):
        content = [dbc.Card(dbc.CardBody([html.H4(['Community Project: DFX']),
                                          html.P(['Defichain has a great community. More and more persons create their own projects to help others and bring value into the ecosystem.',html.Br(),
                                                  'The service of DFX was set up to have an easy entry to the DefiChain ecosystem. You can buy any defichain token with a simple SEPA bank transfer. ',
                                                  'The company in the background will buy your wished tokens and transfer them directly to your wallet. So, you will be the owner of the private keys. ',
                                                  'The idea is to have the opportunity to create different saving plans for the upcoming decentralized assets and cryptos. ',
                                                  html.Br(),
                                                  'You want to know more? Have a look on: ',
                                                  html.A('https://dfx.swiss/', href='https://dfx.swiss/', target='_blank', className='defiLink')],
                                                 style={'text-align': 'justify'}),
                                          html.Table([html.Tr([html.Td('Select graph for evaluation:'),
                                          html.Td(dcc.Dropdown(id='dfxSelectGraph', options=[{'label': 'Total volume', 'value': 'totalVolume'},
                                                                                               {'label': 'Daily volume', 'value': 'dailyVolume'}],
                                                               value='totalVolume', clearable=False, style=dict(verticalAlign="bottom")))])]),
                                          dcc.Graph(id='figureDFXdata', config={'displayModeBar': False})]))]
        return content

    @staticmethod
    def createDFXFigure(data, bgImage, representation):
        figDFX = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        if representation=='dailyVolume':
            ydataBuy = data['dfxBuyVolume'].groupby(data['dfxBuyVolume'].index.floor('d')).last().diff()
            ydataSell = data['dfxSellVolume'].groupby(data['dfxSellVolume'].index.floor('d')).last().diff()
        else:
            ydataBuy = data['dfxBuyVolume'].dropna()
            ydataSell = data['dfxSellVolume'].dropna()

        lastValidDate = datetime.utcfromtimestamp(data['dfxBuyVolume'].dropna().index.values[-1].tolist() / 1e9)
        dateGoBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)
        formatHover = '%{y:,.2f}€'

        trace_diff = dict(type='scatter', name='Difference', x=(ydataBuy-ydataSell).dropna().index, y=(ydataBuy-ydataSell).dropna(),
                          mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate=formatHover)
        trace_buy = dict(type='scatter', name='Buy orders', x=ydataBuy.dropna().index, y=ydataBuy.dropna(),
                          mode='lines', line=dict(color='#90dba8'), line_width=3, hovertemplate=formatHover, fill='tozeroy')
        trace_sell = dict(type='scatter', name='Sell orders', x=ydataSell.dropna().index, y=-ydataSell.dropna(),
                          mode='lines', line=dict(color='#ec9b98'), line_width=3, hovertemplate=formatHover, fill='tozeroy')

        figDFX.add_trace(trace_buy, 1, 1)
        figDFX.add_trace(trace_sell, 1, 1)
        figDFX.add_trace(trace_diff, 1, 1)


        figDFX.update_yaxes(title_text='Volume in EUR', tickformat=",.f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figDFX.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', range=[dateGoBack, lastValidDate], row=1, col=1)

        figDFX.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))

        # Add range slider
        figDFX.update_layout(barmode='stack',
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

        figDFX.update_layout(margin={"t": 50, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figDFX.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDFX.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDFX.layout.legend.font.color = '#6c757d'  # font color legend
        return figDFX

