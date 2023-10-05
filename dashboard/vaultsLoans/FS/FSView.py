import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import dateutil.relativedelta

class fsValueViewClass:

    def getFSValueContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Futures Swap USD value"),
                              dbc.ModalBody(self.getFSValueExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoFSValue", className="ml-auto"))], id="modalFSValue", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Futures Swap USD value']),
                                          html.Table([html.Tr([html.Td('Select dToken for evaluation:'),
                                          html.Td(dcc.Dropdown(id='defiFSValueDToken',options=[{'label': 'Overall', 'value': 'all'},
                                                                                             {'label': 'dUSD', 'value': 'DUSD'},
                                                                                             {'label': 'dToken', 'value': 'dToken'}],
                                                               value='all', clearable=False, style=dict(width='150px',verticalAlign="bottom")))])]),
                                          dcc.Graph(id = 'figureFSValue', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoFSValue")))]))]
        return content


    @staticmethod
    def createFSValueGraph(data, dTokenSelection, bgImage):
        hoverTemplateRepresenation = '$%{y:,.0f}'
        yAxisLabel = 'Value in USD'
        lastValidDate = datetime.utcfromtimestamp(data['FSMinted_USD_DUSD'].dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        # Plotting long term price
        figFSValue = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))


        if (dTokenSelection == 'DUSD') | (dTokenSelection == 'dToken'):
            trace_FSminted = dict(type='scatter', name='Minted', x=(data['FSMinted_USD_'+dTokenSelection]).dropna().index, y=(data['FSMinted_USD_'+dTokenSelection]).dropna(), stackgroup='one',
                                mode='lines', line=dict(color='#90dba8'), line_width=2, hovertemplate=hoverTemplateRepresenation, fill='tozeroy')
            trace_FSburned = dict(type='scatter', name='Burned', x=(data['FSBurned_USD_'+dTokenSelection]).dropna().index, y=(-data['FSBurned_USD_'+dTokenSelection]).dropna(), stackgroup='two',
                                mode='lines', line=dict(color='#ec9b98'), line_width=2, hovertemplate=hoverTemplateRepresenation, fill='tozeroy')
            trace_FSDiff = dict(type='scatter', name='Diff', x=(data['FSBurned_USD_'+dTokenSelection]).dropna().index,
                                y=(data['FSMinted_USD_'+dTokenSelection]).dropna()-(data['FSBurned_USD_'+dTokenSelection]).dropna(),
                                mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate=hoverTemplateRepresenation)

            figFSValue.add_trace(trace_FSminted, 1, 1)
            figFSValue.add_trace(trace_FSburned, 1, 1)
            figFSValue.add_trace(trace_FSDiff, 1, 1)

        else:
            trace_FSminted_dUSD = dict(type='scatter', name='Minted dUSD', x=(data['FSMinted_USD_DUSD']).dropna().index, y=(data['FSMinted_USD_DUSD']).dropna(), stackgroup='one',
                                mode='lines', line=dict(color='#1a522c'), line_width=2, hovertemplate=hoverTemplateRepresenation, fill='tozeroy')
            trace_FSminted_dToken = dict(type='scatter', name='Minted dToken', x=(data['FSMinted_USD_dToken']).dropna().index, y=(data['FSMinted_USD_dToken']).dropna(), stackgroup='one',
                                mode='lines', line=dict(color='#90dba8'), line_width=2, hovertemplate=hoverTemplateRepresenation, fill='tonexty')

            trace_FSburned_dUSD = dict(type='scatter', name='Burned dUSD', x=(data['FSBurned_USD_DUSD']).dropna().index, y=(-data['FSBurned_USD_DUSD']).dropna(), stackgroup='two',
                                mode='lines', line=dict(color='#c42924'), line_width=2, hovertemplate=hoverTemplateRepresenation, fill='tozeroy')
            trace_FSburned_dToken = dict(type='scatter', name='Burned dToken', x=(data['FSBurned_USD_dToken']).dropna().index, y=(-data['FSBurned_USD_dToken']).dropna(), stackgroup='two',
                                mode='lines', line=dict(color='#ec9b98'), line_width=2, hovertemplate=hoverTemplateRepresenation, fill='tonexty')


            trace_FSDiff = dict(type='scatter', name='Diff', x=(data['FSMinted_USD_DUSD']).dropna().index,
                                y=(data['FSMinted_USD_DUSD']).dropna()+(data['FSMinted_USD_dToken']).dropna()-(data['FSBurned_USD_DUSD']).dropna()-(data['FSBurned_USD_dToken']).dropna(),
                                mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate=hoverTemplateRepresenation)

            figFSValue.add_trace(trace_FSminted_dUSD, 1, 1)
            figFSValue.add_trace(trace_FSminted_dToken, 1, 1)
            figFSValue.add_trace(trace_FSburned_dUSD, 1, 1)
            figFSValue.add_trace(trace_FSburned_dToken, 1, 1)
            figFSValue.add_trace(trace_FSDiff, 1, 1)

        figFSValue.update_yaxes(title_text=yAxisLabel, tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figFSValue.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                            range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        # Add range slider
        figFSValue.update_layout(xaxis=dict(
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
        figFSValue.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.25))

        figFSValue.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                         yanchor="top",
                                         y=-0.12,
                                         xanchor="right",
                                         x=1),
                             )
        figFSValue.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figFSValue.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figFSValue.layout.legend.font.color = '#6c757d'  # font color legend

        return figFSValue

    @staticmethod
    def getFSValueExplanation():
        fsValueExplanation = [html.P(['The ....'],style={'text-align': 'justify'}),
                                   html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                                  ]
        return fsValueExplanation