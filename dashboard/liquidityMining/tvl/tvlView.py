import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import dateutil.relativedelta

class tvlViewClass:

    def getTVLContent(self, data):
        content = [dbc.Modal([dbc.ModalHeader("Info Total Value Locked (TVL)"),
                              dbc.ModalBody(self.getTVLExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoTVL", className="ml-auto"))], id="modalTVL", size='xl'),
                   dbc.Card(dbc.CardBody([html.Table([html.Tr([html.Td('Select currency for TVL representation:'),
                                          html.Td(dcc.Dropdown(id='defiTVLCurrency',options=[{'label': 'USD', 'value': 'USD'},
                                                                                             {'label': 'BTC', 'value': 'BTC'},
                                                                                             {'label': 'DFI', 'value': 'DFI'}],
                                            value='USD', style=dict(width='200px',verticalAlign="bottom")))])]),
                        dbc.Col(dcc.Graph(id = 'dexTVL', config={'displayModeBar': False})),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoTVL")))]))]
        return content

    @staticmethod
    def createTVLGraph(data, currencySelection):
        if currencySelection == 'BTC':
            DFIPrice = data['BTC-DFI_DFIPrices']       # choose BTC-pool DFI-price in BTC
            columnName = 'lockedBTC'
            yAxisLabel = 'Value in BTC'
            hoverTemplateRepresenation = '%{y:,.3f}BTC'
        elif currencySelection == 'DFI':
            DFIPrice = 1                                        # use DFI as the currency
            columnName = 'lockedDFI'
            yAxisLabel = 'Value in DFI'
            hoverTemplateRepresenation = '%{y:,.0f}DFI'
        else:
            DFIPrice = data['USDT-DFI_DFIPrices']       # choose USDT-pool for DFI-price in BTC
            columnName = 'lockedUSD'
            yAxisLabel = 'Value in $'
            hoverTemplateRepresenation = '$%{y:,.0f}'

        TVLOverall = (data['BTC-DFI_lockedDFI']+data['ETH-DFI_lockedDFI']+data['USDT-DFI_lockedDFI']+ \
                      data['DOGE-DFI_lockedDFI'].fillna(0)+data['LTC-DFI_lockedDFI'].fillna(0)) * DFIPrice  # DFI is USD is highest price of the 3

        lastValidDate = datetime.utcfromtimestamp(data.index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        # Plotting long term price
        figTVL = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=(['Total value locked (TVL) in DEX']))
        figTVL.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figTVL.layout.annotations[0].font.size = 20

        # single TVL graphs
        trace_TVLBTC = dict(type='scatter', name='BTC', x=data['BTC-DFI_'+columnName].dropna().index, y=data['BTC-DFI_'+columnName].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#da3832'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tozeroy')
        trace_TVLETH = dict(type='scatter', name='ETH', x=data['ETH-DFI_'+columnName].dropna().index, y=data['ETH-DFI_'+columnName].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#617dea'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_TVLUSDT = dict(type='scatter', name='USDT', x=data['USDT-DFI_'+columnName].dropna().index, y=data['USDT-DFI_'+columnName].dropna(), stackgroup='one',
                             mode='lines', line=dict(color='#22b852'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_TVLDOGE = dict(type='scatter', name='DOGE', x=data['DOGE-DFI_'+columnName].dropna().index, y=data['DOGE-DFI_'+columnName].dropna(), stackgroup='one',
                             mode='lines', line=dict(color='#c2a634'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_TVLLTC = dict(type='scatter', name='LTC', x=data['LTC-DFI_'+columnName].dropna().index, y=data['LTC-DFI_'+columnName].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#ff2ebe'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')

        # overall TVL graph
        trace_TVLOverall = dict(type='scatter', name='Overall', x=TVLOverall.index, y=TVLOverall.values,
                                mode='lines', line=dict(color='#410eb2'), line_width=3, hovertemplate=hoverTemplateRepresenation)

        figTVL.add_trace(trace_TVLBTC, 1, 1)
        figTVL.add_trace(trace_TVLETH, 1, 1)
        figTVL.add_trace(trace_TVLUSDT, 1, 1)
        figTVL.add_trace(trace_TVLDOGE, 1, 1)
        figTVL.add_trace(trace_TVLLTC, 1, 1)
        figTVL.add_trace(trace_TVLOverall, 1, 1)

        figTVL.update_yaxes(title_text=yAxisLabel, tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figTVL.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                            range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figTVL.update_layout(xaxis=dict(
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

        figTVL.update_layout(height=765,
                             margin={"t": 40, "l": 130, "b": 20},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                         yanchor="bottom",
                                         y=-0.15,
                                         xanchor="right",
                                         x=1),
                             )
        figTVL.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figTVL.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figTVL.layout.legend.font.color = '#6c757d'  # font color legend

        return figTVL

    @staticmethod
    def getTVLExplanation():
        coinTVLCardExplanation = [html.P(['The total value locked is a key figure, that describes the Fiat value (here in Dollar) stored in the DEX.'],style={'text-align': 'justify'}),
                                  html.P(['The purple line represents the overall value of the DefiChain-DEX and the single pool-pairs are represented as stacked areas.',html.Br(),
                                       ' All values are calculated with the help of the DEX-API (',html.A('API-Link',href='https://api.defichain.io/v1/listpoolpairs?start=0&limit=500&network=mainnet&including_start=false',target='_blank'),
                                       ') and the Coingecko price feed. So, the TVL can be different if you use a single Exchange for the DFI-price.'],style={'text-align': 'justify'}),
                                  html.P(['Normally the TVL is shown in USD. But in this presentation the value can be influenced by new invested capital and by the coinprices. With beginning of Liquidity Mining we see a big price increase for DFI. ',
                                       'So, maybe the reprensentation in BTC or DFI is also interesting for giving some information of the TVL.'],style={'text-align': 'justify'}),
                                   html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                                  ]
        return coinTVLCardExplanation