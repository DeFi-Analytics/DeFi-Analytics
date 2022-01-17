import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

class schemeViewClass:

    def getSchemeContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Loan scheme distribution"),
                              dbc.ModalBody(self.getSchemeExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeSchemeCoin", className="ml-auto"))],
                                    id="modalScheme", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['Loan scheme distribution']),
                                          html.Table([html.Tr([html.Td('Select representation of loan scheme graphic:'),
                                                               html.Td(dcc.Dropdown(id='coinsSchemeGraphic', options=[{'label': 'Absolute', 'value': 'absolute'},
                                                                                                                   {'label': 'Relative', 'value': 'relative'}],
                                                                                    value='absolute', clearable=False, style=dict(verticalAlign="bottom")))])]),
                                          dbc.Row(dbc.Col(dcc.Graph(config={'displayModeBar': False}, id='figureScheme'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoScheme")))
                                          ]))]
        return content


    @staticmethod
    def createSchemeFigure(data, selection, bgImage):
        figScheme = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True)

        # tempData = data.loc[:, ['otherDFI', 'mnDFI', 'lmDFI', 'tokenDFI', 'erc20DFI', 'fundDFI', 'foundationDFI', 'burnedDFI', 'circDFI', 'totalDFI','nbMNlocked5','nbMNlocked10','vaultDFI']]
        # tempData.index = pd.to_datetime(tempData.index)
        # tempData.sort_index(inplace=True)
        # tempData.interpolate(method='pad', inplace=True)

        # IN1000,MIN200,MIN350,MIN500,MIN150,MIN175

        hoverRepresentation = '%{y:,.0f}'
        if selection == 'relative':
            # tempData = tempData.divide(tempData['circDFI'], axis=0)*100
            hoverRepresentation = '%{y:,.2f}%'
            yAxisLabel = 'Relative part of loan scheme'
        else:
            # tempData = tempData.divide(tempData['totalDFI'], axis=0)*100
            hoverRepresentation = '%{y:,.f}'
            yAxisLabel = 'Number loan schemes'

        lastValidDate = datetime.utcfromtimestamp(data['MIN500'].dropna().index.values[-1].tolist()/1e9)
        date14DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=14)

        # absolut DFI representation
        trace_Min150 = dict(type='scatter', name='150%', x=data['MIN150'].dropna().index, y=data['MIN150'].dropna(), mode='lines', line=dict(color='#410eb2'), line_width=2,
                              hovertemplate=hoverRepresentation)
        trace_MIN175 = dict(type='scatter', name='175%', x=data['MIN175'].dropna().index, y=data['MIN175'].dropna(), mode='lines', line=dict(color='#da3832'), line_width=2,
                              hovertemplate=hoverRepresentation)
        trace_MIN200 = dict(type='scatter', name='200%', x=data['MIN200'].dropna().index, y=data['MIN200'].dropna(), mode='lines', line=dict(color='#ff2ebe'), line_width=2,
                              hovertemplate=hoverRepresentation)
        trace_MIN350 = dict(type='scatter', name='350%', x=data['MIN350'].dropna().index, y=data['MIN350'].dropna(), mode='lines', line=dict(color='#22b852'), line_width=2,
                              hovertemplate=hoverRepresentation)
        trace_MIN500 = dict(type='scatter', name='500%', x=data['MIN500'].dropna().index, y=data['MIN500'].dropna(), mode='lines', line=dict(color='#ff9800'), line_width=2,
                              hovertemplate=hoverRepresentation)
        trace_MIN1000 = dict(type='scatter', name='1000%', x=data['MIN1000'].dropna().index, y=data['MIN1000'].dropna(), mode='lines', line=dict(color='#711714'), line_width=2,
                              hovertemplate=hoverRepresentation)

        figScheme.add_trace(trace_Min150, 1, 1)
        figScheme.add_trace(trace_MIN175, 1, 1)
        figScheme.add_trace(trace_MIN200, 1, 1)
        figScheme.add_trace(trace_MIN350, 1, 1)
        figScheme.add_trace(trace_MIN500, 1, 1)
        figScheme.add_trace(trace_MIN1000, 1, 1)


        # curves of circulating and total supply is only relevant in absolute representation
        # if (selection != 'relativeCirc') & (selection != 'relativeTotal'):
        #     trace_circSupply = dict(type='scatter', name='Circulating Supply', x=tempData['circDFI'].dropna().index,
        #                             y=tempData['circDFI'].dropna(), mode='lines', line=dict(color='#ff00af'), line_width=4, hovertemplate='%{y:,.0f}')
        #     figScheme.add_trace(trace_circSupply, 1, 1)
        #     figScheme.add_trace(trace_totalSupply, 1, 1)

        figScheme.update_yaxes(title_text=yAxisLabel, tickformat=",.f", gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figScheme.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate], row=1, col=1)

        figScheme.update_layout(xaxis=dict(
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
        figScheme.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.45, sizey=0.45,  xanchor="center", yanchor="middle", opacity=0.2))


        figScheme.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )

        figScheme.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figScheme.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figScheme.layout.legend.font.color = '#6c757d'  # font color legend

        return figScheme

    @staticmethod
    def getSchemeExplanation():
        schemeCardExplanation = [html.P([''],
                                      style={'text-align': 'justify'}),
                                 html.P([html.B('Hint:'),
                                       ' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on '
                                       'the corresponding legend entry.'],
                                      style={'text-align': 'justify', 'fontSize': '0.7rem', 'color': '#6c757d'})]
        return schemeCardExplanation