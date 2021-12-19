import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

class coinViewClass:

    def getCoinContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info Coins"),
                              dbc.ModalBody(self.getCoinExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoCoin", className="ml-auto"))],
                                    id="modalCoin", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Coin distribution and development']),
                                          html.Table([html.Tr([html.Td('Select representation of coin graphic:'),
                                                               html.Td(dcc.Dropdown(id='coinsSelectionGraphic', options=[{'label': 'Absolute', 'value': 'absolute'},
                                                                                                                   {'label': 'Relative to Circulating Supply', 'value': 'relativeCirc'},
                                                                                                                   {'label': 'Relative to Total Supply', 'value': 'relativeTotal'}],
                                                                                    value='absolute', clearable=False, style=dict(verticalAlign="bottom")))])]),
                                          dbc.Row(dbc.Col(dcc.Graph(config={'displayModeBar': False}, id='figureCoin'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoCoin")))
                                          ]))]
        return content


    @staticmethod
    def createCoinFigure(data, selection, bgImage):
        figDFI = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True)

        tempData = data.loc[:, ['otherDFI', 'mnDFI', 'lmDFI', 'tokenDFI', 'erc20DFI', 'fundDFI', 'foundationDFI', 'burnedDFI', 'circDFI', 'totalDFI','nbMNlocked5','nbMNlocked10','vaultDFI']]
        tempData.index = pd.to_datetime(tempData.index)
        tempData.sort_index(inplace=True)
        tempData.interpolate(method='pad', inplace=True)


        hoverRepresentation = '%{y:,.0f}'
        if selection == 'relativeCirc':
            tempData = tempData.divide(tempData['circDFI'], axis=0)*100
            hoverRepresentation = '%{y:,.2f}%'
        elif selection == 'relativeTotal':
            tempData = tempData.divide(tempData['totalDFI'], axis=0)*100
            hoverRepresentation = '%{y:,.2f}%'

        lastValidDate = datetime.strptime(data['otherDFI'].dropna().index.values[-1], '%Y-%m-%d')
        date2MonthsBack = lastValidDate - dateutil.relativedelta.relativedelta(months=2)

        # absolut DFI representation
        trace_otherDFI = dict(type='scatter', name='Other', x=tempData['otherDFI'].dropna().index,
                              y=tempData['otherDFI'].dropna(), mode='lines', line=dict(color='#410eb2'), line_width=0,
                              hovertemplate=hoverRepresentation, stackgroup='one', fill='tozeroy')
        trace_mnDFI = dict(type='scatter', name='Masternodes', x=(tempData['mnDFI']-(tempData['nbMNlocked10'] + tempData['nbMNlocked5']).fillna(0) * 20000).dropna().index,
                           y=(tempData['mnDFI']-(tempData['nbMNlocked10'] + tempData['nbMNlocked5']).fillna(0) * 20000).dropna(),
                           mode='lines', line=dict(color='#da3832'), line_width=0, hovertemplate=hoverRepresentation, stackgroup='one', fill='tonexty') #visible='legendonly')
        trace_lmDFI = dict(type='scatter', name='Liquidity pool', x=tempData['lmDFI'].dropna().index, y=tempData['lmDFI'].dropna(),
                           mode='lines', line=dict(color='#ff2ebe'), line_width=0, hovertemplate=hoverRepresentation, stackgroup='one', fill='tonexty')
        trace_tokenDFI = dict(type='scatter', name='DFI Token', x=tempData['tokenDFI'].dropna().index, y=tempData['tokenDFI'].dropna(),
                           mode='lines', line=dict(color='#00fffb'), line_width=0, hovertemplate=hoverRepresentation, stackgroup='one', fill='tonexty')
        trace_erc20DFI = dict(type='scatter', name='ERC20 Collateral', x=tempData['erc20DFI'].dropna().index, y=tempData['erc20DFI'].dropna(),
                           mode='lines', line=dict(color='#adff2f'), line_width=0, hovertemplate=hoverRepresentation, stackgroup='one', fill='tonexty')
        trace_vault20DFI = dict(type='scatter', name='Vaults Collateral', x=tempData['vaultDFI'].dropna().index, y=tempData['vaultDFI'].dropna(),
                           mode='lines', line=dict(color='#808000'), line_width=0, hovertemplate=hoverRepresentation, stackgroup='one', fill='tonexty')

        trace_lockedMN = dict(type='scatter', name='Locked Masternodes', x=((tempData['nbMNlocked10'] + tempData['nbMNlocked5']).fillna(0) * 20000).dropna().index,
                              y=((tempData['nbMNlocked10'] + tempData['nbMNlocked5']).fillna(0) * 20000).dropna(),
                             mode='lines', line=dict(color='#711714'), line_width=0, hovertemplate=hoverRepresentation, stackgroup='one', fill='tonexty')
        trace_fundDFI = dict(type='scatter', name='Community fund', x=tempData['fundDFI'].dropna().index, y=tempData['fundDFI'].dropna(),
                             mode='lines', line=dict(color='#ff9800'), line_width=0, hovertemplate=hoverRepresentation, stackgroup='one', fill='tonexty')
        trace_foundationDFI = dict(type='scatter', name='Foundation', x=tempData['foundationDFI'].dropna().index,
                                   y=tempData['foundationDFI'].dropna(),mode='lines', line=dict(color='#22b852'), line_width=0,
                                   hovertemplate=hoverRepresentation, stackgroup='one', fill='tonexty')
        trace_burnedDFI = dict(type='scatter', name='Burned DFI', x=tempData['burnedDFI'].dropna().index,
                                   y=tempData['burnedDFI'].dropna(),mode='lines', line=dict(color='#5d5d5d'), line_width=0,
                                   hovertemplate=hoverRepresentation, stackgroup='one', fill='tonexty')

        figDFI.add_trace(trace_otherDFI, 1, 1)
        figDFI.add_trace(trace_mnDFI, 1, 1)
        figDFI.add_trace(trace_lmDFI, 1, 1)
        figDFI.add_trace(trace_tokenDFI, 1, 1)
        figDFI.add_trace(trace_erc20DFI, 1, 1)
        figDFI.add_trace(trace_vault20DFI, 1, 1)

        # if the graphic is not relative circulating supply, than plot fund, foundation and burned coins
        if (selection != 'relativeCirc'):
            figDFI.add_trace(trace_lockedMN, 1, 1)
            figDFI.add_trace(trace_fundDFI, 1, 1)
            figDFI.add_trace(trace_foundationDFI, 1, 1)
            figDFI.add_trace(trace_burnedDFI, 1, 1)

        # curves of circulating and total supply is only relevant in absolute representation
        if (selection != 'relativeCirc') & (selection != 'relativeTotal'):
            trace_circSupply = dict(type='scatter', name='Circulating Supply', x=tempData['circDFI'].dropna().index,
                                    y=tempData['circDFI'].dropna(), mode='lines', line=dict(color='#ff00af'), line_width=4, hovertemplate='%{y:,.0f}')

            trace_totalSupply = dict(type='scatter', name='Total Supply', x=tempData['totalDFI'].dropna().index,
                                     y=tempData['totalDFI'].dropna(), mode='lines', line=dict(color='#4c0034'), line_width=4, hovertemplate='%{y:,.0f}')
            figDFI.add_trace(trace_circSupply, 1, 1)
            figDFI.add_trace(trace_totalSupply, 1, 1)

        figDFI.update_yaxes(title_text='DFI amount', tickformat=",.f", gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figDFI.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date2MonthsBack.strftime('%Y-%m-%d'), lastValidDate], row=1, col=1)

        figDFI.update_layout(xaxis=dict(
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
        figDFI.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.45, sizey=0.45,  xanchor="center", yanchor="middle", opacity=0.2))


        figDFI.update_layout(height=750,
                             margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )
        figDFI.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDFI.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDFI.layout.legend.font.color = '#6c757d'  # font color legend

        return figDFI

    @staticmethod
    def getCoinExplanation():
        coinCardExplanation = [html.P(['For tracking the amount of DFI and their distribution a snapshot of the DeFiChain richlist is made once a day (in the night).', html.Br(),
                                       html.A('http://explorer.defichain.io/#/DFI/mainnet/rich-list', href='http://explorer.defichain.io/#/DFI/mainnet/rich-list', target='_blank', className='defiLink')],
                                      style={'text-align': 'justify'}),

                               html.P('The first diagram shows the absolute number of coins and their allocation.', style={'text-align': 'justify'}),
                               html.P([ 'The second diagram uses the same data base, but is a relative representation. Due to the fact that the DefiChain foundation no '
                                        'longer has masternodes their relative share is now steadily decreasing'],
                                      style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),
                                       ' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on '
                                       'the corresponding legend entry.'],
                                      style={'text-align': 'justify', 'fontSize': '0.7rem', 'color': '#6c757d'})]
        return coinCardExplanation