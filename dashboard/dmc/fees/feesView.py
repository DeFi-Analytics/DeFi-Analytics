import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import dateutil.relativedelta
import pandas as pd

class feesViewClass:

    def getFeesContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info DMC fees"),
                              dbc.ModalBody(self.getDMCFeesExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoDMCfees", className="ml-auto"))], id="modalDMCfees", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['DMC fees']),
                                          html.Table([html.Tr([html.Td('Select representation:'),
                                          html.Td(dcc.Dropdown(id='defiDMCfees',options=[{'label': 'Overall', 'value': 'all'},
                                                                                          {'label': 'Daily paid fees', 'value': 'D'},
                                                                                          {'label': 'Weekly paid fees', 'value': 'W'}],
                                                               value='all', clearable=False, style=dict(width='150px',verticalAlign="bottom")))])]),
                                          dcc.Graph(id = 'figureDMCfees', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoDMCfees")))]))]
        return content


    @staticmethod
    def createFeesGraph(data, bgImage, selectedGraph, ):
        if selectedGraph == 'D' or selectedGraph == 'W':
            burnedFee = data['DMCfeeBurned'].ffill().groupby(pd.Grouper(freq=selectedGraph)).first().diff().shift(-1)
            priorityFee = data['DMCfeePriority'].ffill().groupby(pd.Grouper(freq=selectedGraph)).first().diff().shift(-1)
        else:
            burnedFee = data['DMCfeeBurned']
            priorityFee = data['DMCfeePriority']


        hoverTemplateRepresenation = '$%{y:,.0f}'
        yAxisLabel = 'Fee amount in DFI'
        lastValidDate = datetime.utcfromtimestamp(data['DMCfeeBurned'].dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        # Plotting long term price
        figDMCfee = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))


        # generate fee sum line
        trace_FeeSum = dict(type='scatter', name='Overall', x=(burnedFee+priorityFee).dropna().index, y=(burnedFee+priorityFee).dropna(),
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:,.f}')

        # generate specific addresses
        trace_burnedFee = dict(type='scatter', name='Burned base fee',x=burnedFee.dropna().index, y=burnedFee.dropna(),
                                 mode='lines', line=dict(color='#ff7fd7'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f}', fill='tozeroy')

        trace_priorityFee = dict(type='scatter', name='Priority fee', x=priorityFee.dropna().index, y=priorityFee.dropna(),
                                    mode='lines', line=dict(color='#ffbfeb'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f}', fill='tonexty')

        figDMCfee.add_trace(trace_burnedFee, 1, 1)
        figDMCfee.add_trace(trace_priorityFee, 1, 1)
        figDMCfee.add_trace(trace_FeeSum, 1, 1)

        figDMCfee.update_yaxes(title_text=yAxisLabel, tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figDMCfee.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                            range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figDMCfee.update_layout(xaxis=dict(
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
        figDMCfee.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.25))

        figDMCfee.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                         yanchor="top",
                                         y=-0.12,
                                         xanchor="right",
                                         x=1),
                             )
        figDMCfee.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDMCfee.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDMCfee.layout.legend.font.color = '#6c757d'  # font color legend

        return figDMCfee

    @staticmethod
    def getDMCFeesExplanation():
        fsValueExplanation = [html.P(['The EVM layer (MetaChain) needs DFI for paying the transaction fees. Like on Ethereum the base fee is burned and these DFI are removed from the circulating supply forever. '
                                      'If you are paying higher fees to get your transaction into the block, this priority fee will be paid to the masternode minting the corresponding block. '],style={'text-align': 'justify'}),
                                   html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                                  ]
        return fsValueExplanation