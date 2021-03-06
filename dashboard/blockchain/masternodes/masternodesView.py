import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import dateutil.relativedelta

class masternodesViewClass:

    def getMasternodesContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Number enabled masternodes"),
                              dbc.ModalBody(self.getMasternodesExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoMN", className="ml-auto"))], id="modalMN", size='xl'),

                   dbc.Card(dbc.CardBody([html.H4(['Number enabled masternodes']),
                                          html.Table([html.Tr([html.Td('Select representation:'),
                                                               html.Td(dcc.Dropdown(id='mnRepresentation', options=[{'label': 'absolute', 'value': 'absolute'},
                                                                                                                   {'label': 'relative', 'value': 'relative'}],
                                                                                    value='absolute', clearable=False, style=dict(width='200px', verticalAlign="bottom")))])]),
                                          dcc.Graph(id='figureMasternodes', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoMN")))]))]
        return content

    @staticmethod
    def createMasternodesGraph(data, selectRepresentation, bgImage):
        lastValidDate = datetime.strptime(data['nbMnId'].dropna().index.values[-1], '%Y-%m-%d')
        date2MonthsBack = lastValidDate - dateutil.relativedelta.relativedelta(days=30)

        figMN = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True)
        if selectRepresentation == 'relative':
            sigNameMNCake = 'nbMnCakeIdRelative'
            sigNameMNOther = 'nbMNOtherRelative'
            sigNameMydefichain = 'nbMydefichainRelative'
            hoverTemplateRepresenation = '%{y:,.3f}%'
            yLabelText = 'Part of enabled masternodes in %'
            yTickRepresentation = ",.2f"
        else:
            sigNameMNCake = 'nbMnCakeId'
            sigNameMNOther = 'nbMNOther'
            sigNameMydefichain = 'nbMydefichainId'
            hoverTemplateRepresenation = '%{y:,.0f}'
            yTickRepresentation = ",.0f"
            yLabelText = 'Number of masternodes'


            # single MN graphs
        trace_MNCake = dict(type='scatter', name='Cake', x=data[sigNameMNCake].dropna().index, y=data[sigNameMNCake].dropna(),
                            stackgroup='one', mode='lines', line=dict(color='#5b10ff'), line_width=0, hovertemplate=hoverTemplateRepresenation, visible='legendonly', fill='tozeroy')
        trace_MNMydefichain = dict(type='scatter', name='MyDefichain', x=data[sigNameMydefichain].dropna().index, y=data[sigNameMydefichain].dropna(),
                             stackgroup='one', mode='lines', line=dict(color='#ff9800'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')
        trace_MNOther = dict(type='scatter', name='Other', x=data[sigNameMNOther].dropna().index, y=data[sigNameMNOther].dropna(),
                             stackgroup='one', mode='lines', line=dict(color='#22b852'), line_width=0, hovertemplate=hoverTemplateRepresenation, fill='tonexty')

        # total number of MN
        trace_MNOverall = dict(type='scatter', name='Overall', x=data['nbMnId'].dropna().index, y=data['nbMnId'].dropna(),
                                mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate=hoverTemplateRepresenation, visible='legendonly')

        figMN.add_trace(trace_MNCake, 1, 1)
        figMN.add_trace(trace_MNMydefichain, 1, 1)
        figMN.add_trace(trace_MNOther, 1, 1)
        if selectRepresentation == 'absolute':
            figMN.add_trace(trace_MNOverall, 1, 1)

        figMN.update_yaxes(title_text=yLabelText, tickformat=yTickRepresentation, gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figMN.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                            range=[date2MonthsBack.strftime('%Y-%m-%d'), lastValidDate], row=1, col=1)

        # Add range slider
        figMN.update_layout(xaxis=dict(
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
        figMN.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.25))

        figMN.update_layout( margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                         yanchor="top",
                                         y=-0.12,
                                         xanchor="right",
                                         x=1),
                             )
        figMN.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figMN.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figMN.layout.legend.font.color = '#6c757d'  # font color legend

        return figMN



    @staticmethod
    def getMasternodesExplanation():
        masternodesCardExplanation = [
            html.P(['This graphic shows the number of enabled masternodes on a daily base. I think the most people are interested in the non-Cake hosted ones on defichain. So, '
                    'in the standard configuration the cake and overall graphs are hidden. Just click on the according legend entry to make them visible.', html.Br(),
                    'Beside the absolute number representation the relative parts could be more of interest. They could be interpreted as a measure of decentralization.'], style={'text-align': 'justify'}),
            html.P(['A list of all masternodes can be get with a full-node and the command line interface. This is routed to an API by Bernd Mack and used here.', html.Br(),
                html.A('http://api.mydeficha.in/v1/listmasternodes/?state=ENABLED', href='http://api.mydeficha.in/v1/listmasternodes/?state=ENABLED', target='_blank', className='defiLink')]),
            html.P(['The second data source is a cake API giving me the addresses of masternodes hosted on their side.', html.Br(),
                         html.A('https://poolapi.cakedefi.com/nodes?order=status&orderBy=DESC', href='https://poolapi.cakedefi.com/nodes?order=status&orderBy=DESC', target='_blank', className='defiLink')]),
            html.P([html.B('Hint:'), ' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                     ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                   style={'text-align': 'justify', 'fontSize': '0.7rem', 'color': '#6c757d'})
            ]
        return masternodesCardExplanation
