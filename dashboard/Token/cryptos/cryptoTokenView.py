import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class crpytoTokenViewClass:

    def getTokenContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info DeFi Asset Token (DAT)"),
                              dbc.ModalBody(self.getTokenExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoToken", className="ml-auto"))], id="modalToken", size='xl'),
                   dbc.Card(dbc.CardBody([html.Td('Select a wrapped token to have a look at: '),
                                         html.Td(dcc.Dropdown(id='tokenCryptosCoin',options=[
                                          {'label': 'BTC', 'value': 'BTC'},
                                          {'label': 'ETH', 'value': 'ETH'},
                                          {'label': 'USDT', 'value': 'USDT'},
                                          {'label': 'DOGE', 'value': 'DOGE'},
                                          {'label': 'LTC', 'value': 'LTC'},
                                          {'label': 'BCH', 'value': 'BCH'}],
                                            value='BTC', style=dict(width='200px', verticalAlign="bottom"))),
                   dbc.Col(dcc.Graph(id='tokenCryptosGraph', config={'displayModeBar': False})),
                   dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoToken")))]))]
        return content

    @staticmethod
    def createTokenGraph(data, selectedCoin, bgImage):
        figTokenData = make_subplots(
            rows=2, cols=1,
            vertical_spacing=0.15,
            row_width=[0.5, 0.5],  # from bottom to top
            specs=[[{}],
                   [{}]],
            shared_xaxes=True,
            subplot_titles=(['Difference minted Token and collateral', 'Tokens/Coins on blockchain']))
        figTokenData.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figTokenData.layout.annotations[0].font.size = 20
        figTokenData.layout.annotations[1].font.color = '#6c757d'
        figTokenData.layout.annotations[1].font.size = 20

        if selectedCoin == 'ETH':
            selectedCoinColor = '#617dea'
            y1Range = [-50, 550]
            y1dTick = 100
            nameCollateralBlockchain = 'Ethereum'
        elif selectedCoin == 'USDT':
            selectedCoinColor = '#22b852'
            y1Range = [-50000, 300000]
            y1dTick = 50000
            nameCollateralBlockchain = 'Ethereum'
        elif selectedCoin == 'DOGE':
            selectedCoinColor = '#c2a634'
            y1Range = [-100000, 1000000]
            y1dTick = 200000
            nameCollateralBlockchain = 'Dogechain'
        elif selectedCoin == 'LTC':
            selectedCoinColor = '#ff2ebe'
            y1Range = [-100, 1000]
            y1dTick = 200
            nameCollateralBlockchain = 'Litecoinchain'
        elif selectedCoin == 'BCH':
            selectedCoinColor = '#410eb2'
            y1Range = [-100, 1000]
            y1dTick = 200
            nameCollateralBlockchain = 'Bitcoin-Cash Chain'
        else:
            selectedCoinColor = '#da3832'
            y1Range = [-10, 60]
            y1dTick = 10
            nameCollateralBlockchain = 'Bitcoin'

        # definition of traces
        trace_diff = dict(type='scatter', name='Difference', x=data[selectedCoin+'_diffToken'].dropna().index, y=data[selectedCoin+'_diffToken'].dropna(),
                          mode='lines', line=dict(color=selectedCoinColor), line_width=2, hovertemplate='%{y:,.4f} ' + selectedCoin)
        trace_defiChain = dict(type='scatter', name='DefiChain', x=data[selectedCoin+'_tokenDefiChain'].dropna().index, y=data[selectedCoin+'_tokenDefiChain'].dropna(),
                               mode='lines', line=dict(color=selectedCoinColor, dash='dash'), line_width=2, hovertemplate='%{y:,.4f} ' + selectedCoin)
        trace_collateral = dict(type='scatter', name=nameCollateralBlockchain, x=data[selectedCoin+'_Collateral'].dropna().index, y=data[selectedCoin+'_Collateral'].dropna(),
                                mode='lines', line=dict(color=selectedCoinColor, dash='dot'), line_width=2, hovertemplate='%{y:,.4f} ' + selectedCoin)
        tickFormatYAxis = ",.0f"

        y1Labeling = 'Difference in ' + selectedCoin
        y2Labeling = selectedCoin + ' on Blockchain'
        figTokenData.add_trace(trace_diff, 1, 1)
        figTokenData.add_trace(trace_defiChain, 2, 1)
        figTokenData.add_trace(trace_collateral, 2, 1)

        figTokenData.update_yaxes(title_text=y1Labeling, tickformat=",.1f", gridcolor='#6c757d', color='#6c757d',
                                  zerolinecolor='#6c757d', range=y1Range, dtick=y1dTick, row=1, col=1)
        figTokenData.update_yaxes(title_text=y2Labeling, tickformat=tickFormatYAxis, gridcolor='#6c757d', color='#6c757d',
                                  zerolinecolor='#6c757d', row=2, col=1)
        figTokenData.update_xaxes(gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figTokenData.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=2, col=1)

        # add background picture
        figTokenData.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.785, sizex=0.45, sizey=0.45,  xanchor="center", yanchor="middle", opacity=0.2))
        figTokenData.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.21, sizex=0.45, sizey=0.45, xanchor="center", yanchor="middle", opacity=0.2))

        figTokenData.update_layout(height=770,
                                   margin={"t": 40, "l": 120, "b": 20, "r": 20},
                                   hovermode='x unified',
                                   hoverlabel=dict(font_color="#6c757d"),
                                   legend=dict(orientation="h",
                                               yanchor="bottom",
                                               y=-0.15,
                                               xanchor="right",
                                               x=1),
                                   )
        figTokenData.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figTokenData.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figTokenData.layout.legend.font.color = '#6c757d'  # font color legend

        return figTokenData

    def getTokenExplanation(self):
        coinAddressCardExplanation = [
                               html.P(['The native coin of DefiChain is DFI. All other tokens are wrapped ones, means these are tokens on DefiChain with the same value than the underlying asset. '
                                       'To ensure this for BTC, ETH and USDT Cake has transferred native coins/tokens on addresses of the Bitcoin/Ethereum blockchain. ' 
                                       'The amount on these addresses must be always equal or greater than the created (minted) tokens on DefiChain. If DATs are no longer needed on DefiChain they will be burned, whichs is a transfer to an address without private key. ',html.Br(),
                                       'In this graphic I am tracking and comparing these amounts. ',
                                       'The easy check is to look on the upper graphic, which must not have negative values.'],style={'text-align': 'justify'}),
                               html.P(['The burning address on DefiChain is',html.Br(),
                                       html.B('8defichainDSTBurnAddressXXXXaCAuTq'),html.Br(),
                                       'Here you can see all burned tokens with the DEX-Explorer (',html.A('Link',href='https://dex.defichain.com/mainnet/address/8defichainDSTBurnAddressXXXXaCAuTq',target='_blank'),')'],style={'text-align': 'justify'}),

                               html.P(['The Bitcoin address holding the real BTC for the DefiChain-BTC is',html.Br(),
                                       html.B('38pZuWUti3vSQuvuFYs8Lwbyje8cmaGhrT'),html.Br(),
                                       'and I am using the following API for getting the data (',html.A('API-Link',href='https://blockchain.info/q/addressbalance/38pZuWUti3vSQuvuFYs8Lwbyje8cmaGhrT',target='_blank'),')'],style={'text-align': 'justify'}),
                               html.P(['The ETH and USDT are both deposited on one Ethereum address, which is',html.Br(),
                                       html.B('0x94fa70d079d76279e1815ce403e9b985bccc82ac'),html.Br(),
                                       'and can be get via Etherscan API (no Link because of individual key for access)',],style={'text-align': 'justify'}),
                               html.P(['The Dogecoin address holding the real DOGE is',html.Br(),
                                       html.B('D7jrXDgPYck8jL9eYvRrc7Ze8n2e2Loyba'),html.Br(),
                                       'You can track them with the following API (',html.A('API-Link',href=' https://sochain.com/api/v2/get_address_balance/DOGE/D7jrXDgPYck8jL9eYvRrc7Ze8n2e2Loyba',target='_blank'),')'],style={'text-align': 'justify'}),
                               html.P(['The Litecoin address holding the real LTC is',html.Br(),
                                       html.B('MLYQxJfnUfVqRwfYXjDJfmLbyA77hqzSXE'),html.Br(),
                                       'You can track them with the following API (',html.A('API-Link',href='https://sochain.com/api/v2/get_address_balance/LTC/MLYQxJfnUfVqRwfYXjDJfmLbyA77hqzSXE',target='_blank'),')'],style={'text-align': 'justify'}),

                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return coinAddressCardExplanation

