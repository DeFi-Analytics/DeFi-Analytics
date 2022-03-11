import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

import pandas as pd


class inflationViewClass:
    def getInflationContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Inflation Circulating Supply"),
                              dbc.ModalBody(self.getInflationExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoInflation", className="ml-auto"))],
                                    id="modalInflation", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Inflation Circulating Supply']),
                                          html.Table([html.Tr([html.Td('Select time base for representation:'),
                                                               html.Td(dcc.Dropdown(id='inflationSelection',
                                                                                    options=[{'label': 'Daily Inflation', 'value': 'D'},
                                                                                             {'label': 'Weekly Inflation', 'value': 'W'}],
                                                                                    value='D', clearable=False, style=dict(width='180px', verticalAlign="bottom")))])]),
                                          dbc.Row(dbc.Col(dcc.Graph(config={'displayModeBar': False}, id='figureInflation'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoInflation")))
                                          ]))]
        return content


    @staticmethod
    def createInflationGraph(dataDaily, dataHourly, bgImage, representation):
        figInflation = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        formatHover = '%{y:,.2f} DFI'
        lastValidDate = datetime.strptime(dataDaily['nbBlocks'].dropna().index.values[-1], '%Y-%m-%d')
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)
        yAxisRange = [-2000000, 1000000]

        emissionDFI = ((dataDaily['masternodeEmission'] + dataDaily['dexEmission'] + dataDaily['dTokenEmission'] + dataDaily['anchorEmission']) * dataDaily['nbBlocks']).dropna().drop_duplicates().iloc[:-1]
        burnedDFIHourly = (dataHourly['burnedAuction'] + dataHourly['burnedPayback'] + dataHourly['burnedDFIPayback'].fillna(0)).dropna()
        burnedDFIHourly.groupby(burnedDFIHourly.index.floor('d')).first()
        burnedDFIDaily = burnedDFIHourly.groupby(burnedDFIHourly.index.floor('d')).first().diff().shift(-1)
        emissionDFI.index = pd.to_datetime(emissionDFI.index)

        if representation == 'W':
            emissionDFI=emissionDFI.groupby(pd.Grouper(freq=representation)).sum()
            burnedDFIDaily = burnedDFIDaily.groupby(pd.Grouper(freq=representation)).sum()
            yAxisRange = [-10000000, 10000000]
            date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(months=2)

        diffInflationDFI = emissionDFI - burnedDFIDaily

        trace_diff = dict(type='scatter', name='Effective inflation',x=diffInflationDFI.dropna().index, y=diffInflationDFI.dropna(),
                          mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate=formatHover)
        trace_emission = dict(type='scatter', name='DFI emissioned to circ cupply', x=emissionDFI.dropna().index, y=emissionDFI.dropna(),
                              mode='lines', line=dict(color='#90dba8'), line_width=3, hovertemplate=formatHover, fill='tozeroy')
        trace_burned = dict(type='scatter', name='DFI burned via vaults&loans', x=burnedDFIDaily.dropna().index, y=-burnedDFIDaily.dropna(),
                              mode='lines', line=dict(color='#ec9b98'), line_width=3, hovertemplate=formatHover, fill='tozeroy')


        figInflation.add_trace(trace_emission, 1, 1)
        figInflation.add_trace(trace_burned, 1, 1)
        figInflation.add_trace(trace_diff, 1, 1)

        figInflation.update_yaxes(title_text='Daily DFI change', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                                  range=yAxisRange, zerolinecolor='#6c757d', row=1, col=1)
        figInflation.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                                  range=[date14DaysBack, lastValidDate], row=1, col=1)       # select 14 days range: range=[date30DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate]

        # Add range slider
        figInflation.update_layout(barmode='stack',
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

        # add background picture
        figInflation.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.25))

        figInflation.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                                               hovermode='x unified',
                                               hoverlabel=dict(font_color="#6c757d"),
                                               legend=dict(orientation="h",
                                                           yanchor="top",
                                                           y=-0.12,
                                                           xanchor="right",
                                                           x=1),
                                               )
        figInflation.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figInflation.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figInflation.layout.legend.font.color = '#6c757d'  # font color legend
        figInflation.layout.hoverlabel.bgcolor = 'white'
        return figInflation

    @staticmethod
    def getInflationExplanation():
        DEXVolumeCardExplanation = [html.P(['The calculation of the effective inflation of the circulating DFI supply needs two different information:',
                                            html.Ul([html.Li('The DFI amount emissioned with each minted block, which are for the masternodes, crypto liquidity mining, dToken liquidity mining and anchoring rewards'),
                                                     html.Li('The DFI amount burned by the vaults & loans feature, which includes loan interests, auction fees and dUSD payback with DFI')])], style={'text-align': 'justify'}),
                                    html.P(['The evaluation shows you the DFI emission (green area) und burn (red area) for the selected intervall. The corresponding inflation is the difference between these two (pink line).'], style={'text-align': 'justify'}),
                                     html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                                   ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                                    style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'}) ]
        return DEXVolumeCardExplanation