import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

class redditViewClass:

    def getRedditMembersContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Reddit Members"),
                              dbc.ModalBody(self.getRedditMemberExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoRedditMember", className="ml-auto"))], id="modalRedditMember", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Reddit Members statistics']),
                                          html.Table([html.Tr([html.Td('Select member graph:'),
                                                               html.Td(dcc.Dropdown(id='communityRedditMemberSelection',
                                                                                    options=[{'label': 'Absolute number', 'value': 'nbAbsolute'},
                                                                                             {'label': 'Abs. daily diff of Members', 'value': 'absDailyDiff'},
                                                                                             {'label': 'Rel. daily diff of Members', 'value': 'relDailyDiff'}],
                                                                                    value='nbAbsolute', clearable=False, style=dict(width='235px', verticalAlign="bottom")))])]),
                                          dcc.Graph(id='figureRedditMember', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoRedditMember")))]))]
        return content


    @staticmethod
    def createRedditMemberGraph(data, bgImage):
        figRedditMember = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        lastValidDate = datetime.strptime(data['Follower'].dropna().index.values[-1], '%Y-%m-%d')
        date30DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=30)

        trace_Member = dict(type='scatter', name='members', x=data['usersReddit'].dropna().index, y=data['usersReddit'].dropna(),
                                mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate='%{y:,.0f}')

        figRedditMember.add_trace(trace_Member, 1, 1)

        figRedditMember.update_yaxes(title_text='Number of Reddit members', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figRedditMember.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                            row=1, col=1)       # select 14 days range: range=[date30DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate]

        # Add range slider
        figRedditMember.update_layout(xaxis=dict(
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
        figRedditMember.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.25))

        figRedditMember.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                         yanchor="top",
                                         y=-0.12,
                                         xanchor="right",
                                         x=1),
                             )
        figRedditMember.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figRedditMember.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figRedditMember.layout.legend.font.color = '#6c757d'  # font color legend
        figRedditMember.layout.hoverlabel.bgcolor = 'white'
        return figRedditMember

    @staticmethod
    def createDiffRedditMemberGraph(data, bgImage, representation):
        figRedditMembersChange = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        if representation == 'relative':
            denominator = data['usersReddit']/100
            formatHover = '%{y:,.2f}%'
            yAxisLabel = 'Relative change Reddit members'
            yAxisTick = ",.1f"
        else:
            denominator = 1
            formatHover = '%{y:,.0f}'
            yAxisLabel = 'Absolute change Reddit members'
            yAxisTick = ",.0f"

        lastValidDate = datetime.strptime(data['usersReddit'].dropna().index.values[-1], '%Y-%m-%d')
        date30DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(days=30)

        trace_diff = dict(type='scatter', name='Daily change', x=data['usersReddit'].diff().dropna().index,
                          y=(data['usersReddit'].diff()/denominator).dropna(),
                          mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate=formatHover)
        figRedditMembersChange.add_trace(trace_diff, 1, 1)

        figRedditMembersChange.update_yaxes(title_text=yAxisLabel, tickformat=yAxisTick, gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figRedditMembersChange.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                            row=1, col=1)       # select 14 days range: range=[date30DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate]

        # Add range slider
        figRedditMembersChange.update_layout(xaxis=dict(
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
        figRedditMembersChange.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.25))

        figRedditMembersChange.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                         yanchor="top",
                                         y=-0.12,
                                         xanchor="right",
                                         x=1),
                             )
        figRedditMembersChange.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figRedditMembersChange.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figRedditMembersChange.layout.legend.font.color = '#6c757d'  # font color legend
        figRedditMembersChange.layout.hoverlabel.bgcolor = 'white'
        return figRedditMembersChange

    @staticmethod
    def getRedditMemberExplanation():
        redditMemberExplanation = [html.P(['Reddit is a social news aggregation and discussion website. A lot of blockchain projects have their own subreddit to discuss topics inside the commmunity. ',
                                       'Here I want to track the DefiChain subreddit members.'],style={'text-align': 'justify'}),
                               html.P(['In addition to the pure representation of the absolute number, the daily rate of change is also evaluated. '
                                       'This difference can be shown as an asbolute number or in relation to the existing members number. With growing members the last one can be used to compare different time ranges. '],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return redditMemberExplanation