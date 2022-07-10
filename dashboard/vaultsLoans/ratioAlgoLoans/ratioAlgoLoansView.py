import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

import pandas as pd

class ratioAlgoLoansViewClass:

    def getRatioAlgoLoansContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Relative part of algo to circulating dToken"),
                              dbc.ModalBody(self.getRatioAlgoLoanExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoAlgoRatioLoans", className="ml-auto"))],
                                    id="modalAlgoRatioLoans", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Relative part of algo to circulating dToken']),
                                          html.Table([html.Tr([html.Td('Select dToken for evaluation:'),
                                                               html.Td(dcc.Dropdown(id='vaultsLoansAlgoRatioLoans', options=[{'label': 'dUSD', 'value': 'DUSD'},
                                                                                                                         {'label': 'AAPL', 'value': 'AAPL'},
                                                                                                                         {'label': 'AMZN', 'value': 'AMZN'},
                                                                                                                         {'label': 'ARKK', 'value': 'ARKK'},
                                                                                                                         {'label': 'BABA', 'value': 'BABA'},
                                                                                                                         {'label': 'BRK.B', 'value': 'BRK.B'},
                                                                                                                         {'label': 'COIN', 'value': 'COIN'},
                                                                                                                         {'label': 'CS', 'value': 'CS'},
                                                                                                                         {'label': 'DIS', 'value': 'DIS'},
                                                                                                                         {'label': 'EEM', 'value': 'EEM'},
                                                                                                                         {'label': 'FB', 'value': 'FB'},
                                                                                                                         {'label': 'GLD', 'value': 'GLD'},
                                                                                                                         {'label': 'GSG', 'value': 'GSG'},
                                                                                                                         {'label': 'GME', 'value': 'GME'},
                                                                                                                         {'label': 'GOOGL', 'value': 'GOOGL'},
                                                                                                                         {'label': 'INTC', 'value': 'INTC'},
                                                                                                                         {'label': 'KO', 'value': 'KO'},
                                                                                                                         {'label': 'MCHI', 'value': 'MCHI'},
                                                                                                                         {'label': 'MSFT', 'value': 'MSFT'},
                                                                                                                         {'label': 'MSTR', 'value': 'MSTR'},
                                                                                                                         {'label': 'NFLX', 'value': 'NFLX'},
                                                                                                                         {'label': 'NVDA', 'value': 'NVDA'},
                                                                                                                         {'label': 'PDBC', 'value': 'PDBC'},
                                                                                                                         {'label': 'PG', 'value': 'PG'},
                                                                                                                         {'label': 'PLTR', 'value': 'PLTR'},
                                                                                                                         {'label': 'PYPL', 'value': 'PYPL'},
                                                                                                                         {'label': 'QQQ', 'value': 'QQQ'},
                                                                                                                         {'label': 'SAP', 'value': 'SAP'},
                                                                                                                         {'label': 'SLV', 'value': 'SLV'},
                                                                                                                         {'label': 'SPY', 'value': 'SPY'},
                                                                                                                         {'label': 'TLT', 'value': 'TLT'},
                                                                                                                         {'label': 'TSLA', 'value': 'TSLA'},
                                                                                                                         {'label': 'URA', 'value': 'URA'},
                                                                                                                         {'label': 'URTH', 'value': 'URTH'},
                                                                                                                         {'label': 'VNQ', 'value': 'VNQ'},
                                                                                                                         {'label': 'VOO', 'value': 'VOO'},],
                                                                                    value='DUSD', clearable=False, style=dict(width='150px', verticalAlign="bottom")))])]),
                                          dcc.Graph(id='figureAlgoRatioLoans', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoAlgoRatioLoans")))
                                          ]))]
        return content


    @staticmethod
    def createAlgoRatioLoans(data, bgImage, representation):
        figAlgoRatioLoans = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        lastValidDate = datetime.utcfromtimestamp(data['sumLoan'+representation].dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        # calculate circulating amount
        basisGraph = data['sumLoan' + representation].interpolate(method='pad', limit_direction='forward').dropna()
        dTokenCircAmount = basisGraph
        if 'DFIPFuture_minted_' + representation in data.columns:
            dataFutureMinted = data['DFIPFuture_minted_' + representation].interpolate(method='pad', limit_direction='forward').fillna(0).cummax()
            dataFutureMinted = dataFutureMinted.loc[basisGraph.index]
            dTokenCircAmount = dTokenCircAmount + dataFutureMinted
        if representation == 'DUSD':
            dataDUSDpaidDFI = data['DUSDpaidDFI'].interpolate(method='pad', limit_direction='forward').fillna(0).cummax()
            dataDUSDpaidDFI = dataDUSDpaidDFI.loc[basisGraph.index]
            dTokenCircAmount = dTokenCircAmount + dataDUSDpaidDFI
        if 'DFIPFuture_burned_' + representation in data.columns:
            dataFutureBurned = data['DFIPFuture_burned_' + representation].interpolate(method='pad', limit_direction='forward').fillna(0).cummax()
            dataFutureBurned = dataFutureBurned.loc[basisGraph.index]
            dTokenCircAmount = dTokenCircAmount - dataFutureBurned
        else:
            dataFutureBurned = basisGraph*0
        if 'burned' + representation + 'DEX' in data.columns:
            dataBurned = data['burned' + representation + 'DEX'].interpolate(method='pad', limit_direction='forward').fillna(0).cummax()
            dataBurned = dataBurned.loc[basisGraph.index]
            dTokenCircAmount = dTokenCircAmount - dataBurned
        if 'DFIPFuture_current_' + representation in data.columns:
            dataFutureCurrent = pd.concat([data['DFIPFuture_current_' + representation].interpolate(method='pad', limit_direction='forward').fillna(0), dataFutureBurned]).max(level=0)
            dataFutureCurrent = dataFutureCurrent.loc[basisGraph.index]
            if 'DFIPFuture_burned_' + representation in data.columns:
                dTokenLocked = dataFutureCurrent - dataFutureBurned
            else:
                dTokenLocked = dataFutureCurrent
            dTokenCircAmount = dTokenCircAmount - dTokenLocked

        dataRatio = (dTokenCircAmount-basisGraph)/dTokenCircAmount*100

        trace_ratioAlgoLoan = dict(type='scatter', name='relative Part',
                              x=dataRatio.dropna().index, y=dataRatio.dropna(),
                              mode='lines', line=dict(color='#ff00af'),  line_width=3, hovertemplate='%{y:,.4f}%', fill='none')

        # plot circulating supply
        figAlgoRatioLoans.add_trace(trace_ratioAlgoLoan, 1, 1)

        figAlgoRatioLoans.update_yaxes(title_text='Relative part of algo to circulating dToken in %', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figAlgoRatioLoans.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d',
                               range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figAlgoRatioLoans.update_layout(xaxis=dict(
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

        figAlgoRatioLoans.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))

        figAlgoRatioLoans.update_layout(margin={"t": 60, "l": 0, "b": 0, "r": 0},
                                barmode='stack',
                                hovermode='x unified',
                                hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                legend=dict(orientation="h",
                                            yanchor="top",
                                            y=-0.12,
                                            xanchor="right",
                                            x=1),
                                )
        figAlgoRatioLoans.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figAlgoRatioLoans.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figAlgoRatioLoans.layout.legend.font.color = '#6c757d'  # font color legend
        return figAlgoRatioLoans


    @staticmethod
    def getRatioAlgoLoanExplanation():
        ratioAlgoLoanExplanation = [html.P(['The dToken system on DeFiChain is a hybrid decentralized asset system. That means on the one hand the user can mint dTokens with '
                                            'the vault and loan feature. These dTokens are backed by their loans. On the other hand the Future Swap was introduced to handle the premium/discount '
                                            'of the assets compared to the real world. With this feature dTokens are minted (and burned) without any loan in the background (=algo dToken).'],style={'text-align': 'justify'}),
                                    html.P(['This evaluation shows the relative part of the algo dToken with respect to the circulating supply. In case of dUSD this number is used to determine the DEX '
                                            'stabilizing fee.'],
                                           style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return ratioAlgoLoanExplanation