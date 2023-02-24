import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import dateutil.relativedelta

class emissionViewClass:

    def getEmissionContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info DFI Emission & Inflation"),
                              dbc.ModalBody(self.getEmissionExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoEmission", className="ml-auto"))], id="modalEmission", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['DFI Emission & Inflation']),
                                          html.Table([html.Tr([html.Td('Select evaluation:'),
                                          html.Td(dcc.Dropdown(id='selectEmission',options=[{'label': 'DFI emission per Block', 'value': 'emission'},
                                                                                             {'label': 'Inflation w/ circ. supply', 'value': 'inflationCirc'},],
                                                               value='emission', clearable=False, style=dict(verticalAlign="bottom")))])]),
                                          dcc.Graph(id = 'figureEmission', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoEmission")))]))]
        return content

    @staticmethod
    def createEmissionGraph(data, currencySelection, bgImage):
        if currencySelection == 'inflationCirc':
            lineName = 'Inflation'
            yAxisLabel = 'Yearly inflation rate in %'
            yAxisRange = [0, 100]
            lineData = data['totalEmission']*2880*365*100 / data['circDFI']
            hoverTemplateRepresenation = '%{y:,.2f}%'
        elif currencySelection == 'inflationCircMN':
            lineName = 'Inflation'
            yAxisLabel = 'Yearly inflation rate in %'
            yAxisRange = [0, 100]
            lineData = data['totalEmission']*2880*365*100 / (data['circDFI'] + (data['nbMNlocked10']+data['nbMNlocked5'])*20000)
            hoverTemplateRepresenation = '%{y:,.2f}%'
        else:
            lineName = 'Total block emission'
            yAxisLabel = 'DFI coins'
            yAxisRange = [0, 310]
            lineData = data['totalEmission']
            hoverTemplateRepresenation = '%{y:,.2f} DFI'

        lastValidDate = datetime.strptime(data['otherDFI'].dropna().index.values[-1], '%Y-%m-%d')
        date2MonthsBack = lastValidDate - dateutil.relativedelta.relativedelta(months=2)

        # Plotting long term price
        figEmission = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        # single emission graphs
        trace_MN = dict(type='scatter', name='MN block reward', x=data['masternodeEmission'].dropna().index, y=data['masternodeEmission'].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#da3832'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tozeroy')
        trace_DEX = dict(type='scatter', name='Crypto liquidity provider', x=data['dexEmission'].dropna().index, y=data['dexEmission'].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#617dea'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_dToken = dict(type='scatter', name='dToken liquidity provider', x=data['dTokenEmission'].dropna().index, y=(data['dTokenEmission']).dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#ff9800'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_Fund = dict(type='scatter', name='Community Fund', x=data['communityEmission'].dropna().index, y=data['communityEmission'].dropna(), stackgroup='one',
                             mode='lines', line=dict(color='#22b852'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_Anchor = dict(type='scatter', name='Anchoring', x=data['anchorEmission'].dropna().index, y=data['anchorEmission'].dropna(), stackgroup='one',
                             mode='lines', line=dict(color='#c2a634'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_Burn = dict(type='scatter', name='Burned (unused)', x=data['burnedEmission'].dropna().index, y=data['burnedEmission'].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#5d5d5d'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_dUSDBot = dict(type='scatter', name='dUSD burn bot 2', x=data['dUSDBurnBotEmission'].dropna().index, y=data['dUSDBurnBotEmission'].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#ff2ebe'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')

        # line graph
        trace_Line = dict(type='scatter', name=lineName, x=lineData.dropna().index, y=lineData.dropna(),
                                mode='lines', line=dict(color='#410eb2'), line_width=3, hovertemplate=hoverTemplateRepresenation)

        if currencySelection == 'emission':
            figEmission.add_trace(trace_MN, 1, 1)
            figEmission.add_trace(trace_DEX, 1, 1)
            figEmission.add_trace(trace_dToken, 1, 1)
            figEmission.add_trace(trace_Fund, 1, 1)
            figEmission.add_trace(trace_Anchor, 1, 1)
            figEmission.add_trace(trace_Burn, 1, 1)
            figEmission.add_trace(trace_dUSDBot, 1, 1)

        figEmission.add_trace(trace_Line, 1, 1)

        figEmission.update_yaxes(title_text=yAxisLabel, tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', range = yAxisRange,
                            zerolinecolor='#6c757d', row=1, col=1)
        figEmission.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d', row=1, col=1) #range=[date2MonthsBack.strftime('%Y-%m-%d'), lastValidDate],

        # Add range slider
        figEmission.update_layout(xaxis=dict(
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
        figEmission.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.25))

        figEmission.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                             legend=dict(orientation="h",
                                         yanchor="top",
                                         y=-0.12,
                                         xanchor="right",
                                         x=1),
                             )
        figEmission.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figEmission.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figEmission.layout.legend.font.color = '#6c757d'  # font color legend

        return figEmission

    @staticmethod
    def getEmissionExplanation():
        emissionCardExplanation = [html.P(['DefiChain emissions new DFI with each minted blocks (like nearly all other blockchains). These coins are used to incentivize different features on the blockchain like minting blocks (masternodes), '
                                           'providing liquidity on the DEX or just to fill up the community fund for upcoming CFPs. Every 32,690 blocks the rewards are reduced by 1.658%. '
                                           'This ensures that in about 10 years we will reach the max. supply of 1.2 billion DFI. The first graph shows the DFI per block and their allocation.'],style={'text-align': 'justify'}),
                                   html.P(['The user can also select the inflation graph, which calculates the annual inflation based on the current DFI emission. The theoretical value of 2880 blocks per days is used for this purpose. '
                                           'The basis is also the current amount of circulating DFI coins with and without the locked masternodes (hard to tell if the DFI are ciruclating or not).'], style={'text-align': 'justify'}),
                                   html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                                  ]
        return emissionCardExplanation