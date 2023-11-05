import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import dateutil.relativedelta
import pandas as pd

class tokenViewClass:

    def getTokensContent(self, listAvailableToken):
        optionsList = []
        for token in listAvailableToken:
            optionsList = optionsList + [{'label': token, 'value': token}]

        content = [dbc.Modal([dbc.ModalHeader("Info DMC token"),
                              dbc.ModalBody(self.getDMCTokensExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoDMCtoken", className="ml-auto"))], id="modalDMCtoken", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['DAT-token on DMC']),
                                          html.Table([html.Tr([html.Td('Select representation:'),
                                                               html.Td(dcc.Dropdown(options=optionsList, value='DFI', id='defiDMCtoken', clearable=False, style=dict(width='150px',verticalAlign="bottom")))
                                                               ])
                                                      ]),
                                          dcc.Graph(id='figureDMCtoken', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoDMCtoken")))]))]
        return content


    @staticmethod
    def createTokensGraph(data, bgImage, selectedToken, ):
        hoverTemplateRepresenation = '%{y:,.2f}'
        yAxisLabel = 'Amount of ' + selectedToken

        lastValidDate = datetime.utcfromtimestamp(data['DMCtoken_DVM_'+selectedToken].dropna().index.values[-1].tolist() / 1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        # Plotting long term price
        figToken = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        trace_movedEVM = dict(type='scatter', name='Transferred to DMC', x=(data['DMCtoken_EVM_' + selectedToken]).dropna().index, y=(data['DMCtoken_EVM_' + selectedToken]).dropna(),
                              stackgroup='one',
                              mode='lines', line=dict(color='#90dba8'), line_width=2, hovertemplate=hoverTemplateRepresenation, fill='tozeroy')
        trace_removedEVM = dict(type='scatter', name='Removed from DMC', x=(data['DMCtoken_DVM_' + selectedToken]).dropna().index, y=(-data['DMCtoken_DVM_' + selectedToken]).dropna(),
                              stackgroup='two',
                              mode='lines', line=dict(color='#ec9b98'), line_width=2, hovertemplate=hoverTemplateRepresenation, fill='tozeroy')
        trace_diffEVM = dict(type='scatter', name='Diff', x=(data['DMCtoken_EVM_' + selectedToken]).dropna().index,
                            y=(data['DMCtoken_EVM_' + selectedToken]).dropna() - (data['DMCtoken_DVM_' + selectedToken]).dropna(),
                            mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate=hoverTemplateRepresenation)

        figToken.add_trace(trace_movedEVM, 1, 1)
        figToken.add_trace(trace_removedEVM, 1, 1)
        figToken.add_trace(trace_diffEVM, 1, 1)


        figToken.update_yaxes(title_text=yAxisLabel, tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                                zerolinecolor='#6c757d', row=1, col=1)
        figToken.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                                range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figToken.update_layout(xaxis=dict(
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
        figToken.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6, xanchor="center", yanchor="middle", opacity=0.25))

        figToken.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d"),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figToken.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figToken.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figToken.layout.legend.font.color = '#6c757d'  # font color legend

        return figToken


    @staticmethod
    def getDMCTokensExplanation():
        fsValueExplanation = [html.P(['MetaChain is an EVM layer on top of the UTXO blockchain of DeFiChain. There is one connection between the native blockchain and MetaChain called transferdomain. '
                                      'With this command DAT tokens can be transferred between the two layers. For each token created on the EVM layer the corresponding amount is removed from native side. '
                                      'Only after the transfer back it will exist again on native DeFiChain. This evaluation tracks the amount of token transferred to and removed from MetaChain layer.'],style={'text-align': 'justify'}),
                                   html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                                  ]
        return fsValueExplanation