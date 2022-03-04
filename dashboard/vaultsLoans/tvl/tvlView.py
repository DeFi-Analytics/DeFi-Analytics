import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import dateutil.relativedelta

class tvlVaultsViewClass:

    def getTVLContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Total Value Locked (TVL) as Collateral"),
                              dbc.ModalBody(self.getTVLExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoTVLVaults", className="ml-auto"))], id="modalTVLVaults", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Total value locked (TVL)']),
                                          html.Table([html.Tr([html.Td('Select currency for TVL representation:'),
                                          html.Td(dcc.Dropdown(id='defiTVLVaultsCurrency',options=[{'label': 'USD', 'value': 'USD'},
                                                                                             {'label': 'BTC', 'value': 'BTC'},
                                                                                             {'label': 'DFI', 'value': 'DFI'}],
                                                               value='USD', clearable=False, style=dict(width='150px',verticalAlign="bottom")))])]),
                                          dcc.Graph(id = 'figureTVLVaults', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoTVLVaults")))]))]
        return content

    @staticmethod
    def createTVLGraph(data, currencySelection, bgImage):
        if currencySelection == 'BTC':
            DFIPrice = data['BTC-DFI_DFIPrices'].fillna(0)       # choose BTC-pool DFI-price in BTC
            yAxisLabel = 'Value in BTC'
            hoverTemplateRepresenation = '%{y:,.3f}BTC'
        elif currencySelection == 'DFI':
            DFIPrice = 1                                        # use DFI as the currency
            yAxisLabel = 'Value in DFI'
            hoverTemplateRepresenation = '%{y:,.0f}DFI'
        else:
            DFIPrice = data['USDT-DFI_DFIPrices'].fillna(0)       # choose USDT-pool for DFI-price in BTC
            yAxisLabel = 'Value in $'
            hoverTemplateRepresenation = '$%{y:,.0f}'

        TVLOverall = (data['sumBTC'] / data['BTC-DFI_reserveA/reserveB'] + \
                          data['sumDFI'] + \
                          data['sumUSDC'] / data['USDC-DFI_reserveA/reserveB'] + \
                          data['sumUSDT'] / data['USDT-DFI_reserveA/reserveB'] + \
                          data['sumDUSD'].fillna(0) / data['DUSD-DFI_reserveA/reserveB'].fillna(0)) * DFIPrice

        lastValidDate = datetime.utcfromtimestamp(data['BTC-DFI_lockedDFI'].dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        # Plotting long term price
        figTVL = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        # single TVL graphs
        trace_TVLDFI = dict(type='scatter', name='DFI', x=data['sumDFI'].dropna().index, y=(data['sumDFI'] * DFIPrice).dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#ff9800'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tozeroy')

        trace_TVLBTC = dict(type='scatter', name='BTC', x=(data['sumBTC'] / data['BTC-DFI_reserveA/reserveB'] * DFIPrice).dropna().index,
                            y=(data['sumBTC'] / data['BTC-DFI_reserveA/reserveB'] * DFIPrice).dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#da3832'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')

        trace_TVLUSDT = dict(type='scatter', name='USDT', x=(data['sumUSDT'] / data['USDT-DFI_reserveA/reserveB'] * DFIPrice).dropna().index,
                             y=(data['sumUSDT'] / data['USDT-DFI_reserveA/reserveB'] * DFIPrice).dropna(), stackgroup='one',
                             mode='lines', line=dict(color='#22b852'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')

        trace_TVLUSDC = dict(type='scatter', name='USDC', x=(data['sumUSDC'] / data['USDC-DFI_reserveA/reserveB']).dropna().index,
                             y=(data['sumUSDC'] / data['USDC-DFI_reserveA/reserveB'] * DFIPrice).dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#7f4c00'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')

        trace_TVLDUSD = dict(type='scatter', name='dUSD', x=(data['sumDUSD'] / data['DUSD-DFI_reserveA/reserveB']).dropna().index,
                             y=(data['sumDUSD'] / data['DUSD-DFI_reserveA/reserveB'] * DFIPrice).dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#ff2ebe'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')

        # overall TVL graph
        trace_TVLOverall = dict(type='scatter', name='Overall', x=TVLOverall.dropna().index, y=TVLOverall.dropna(),
                                mode='lines', line=dict(color='#410eb2'), line_width=3, hovertemplate=hoverTemplateRepresenation)

        figTVL.add_trace(trace_TVLDFI, 1, 1)
        figTVL.add_trace(trace_TVLBTC, 1, 1)
        figTVL.add_trace(trace_TVLUSDT, 1, 1)
        figTVL.add_trace(trace_TVLUSDC, 1, 1)
        figTVL.add_trace(trace_TVLDUSD, 1, 1)

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

        # add background picture
        figTVL.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.25))

        figTVL.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                         yanchor="top",
                                         y=-0.12,
                                         xanchor="right",
                                         x=1),
                             )
        figTVL.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figTVL.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figTVL.layout.legend.font.color = '#6c757d'  # font color legend

        return figTVL

    @staticmethod
    def getTVLExplanation():
        coinTVLCardExplanation = [html.P(['The total value locked is a key figure, that describes the value (here e.g. in Dollar) stored in the vaults as collateral for the minted dTokens.'],style={'text-align': 'justify'}),
                                  html.P(['The purple line represents the overall value of the vaults on Defichain and the different coins are represented as stacked areas.'],style={'text-align': 'justify'}),

                                  html.P(['Normally the TVL is shown in USD. But in this presentation the value can be influenced by new invested capital and by the coinprices. With beginning of Liquidity Mining we see a big price increase for DFI. ',
                                       'So, maybe the reprensentation in BTC or DFI is also interesting for giving some information of the TVL.'],style={'text-align': 'justify'}),
                                   html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                                  ]
        return coinTVLCardExplanation