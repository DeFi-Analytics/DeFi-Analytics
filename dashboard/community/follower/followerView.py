import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
from datetime import datetime
import dateutil.relativedelta

class followerViewClass:

    def getTwitterFollowerContent(self):
        content = [dbc.Modal([dbc.ModalHeader("Info Twitter Follower"),
                              dbc.ModalBody(self.getTwitterFollowerExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoTwitterFollower", className="ml-auto"))], id="modalTwitterFollower", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Twitter Follower statistics']),
                                          html.Table([html.Tr([html.Td('Select follower graph:'),
                                                               html.Td(dcc.Dropdown(id='communityFollowerSelection',
                                                                                    options=[{'label': 'Absolute number', 'value': 'nbAbsolute'},
                                                                                             {'label': 'Daily difference of Followers', 'value': 'dailyDiff'}],
                                                                                    value='nbAbsolute', clearable=False, style=dict(width='235px', verticalAlign="bottom")))])]),
                                          dcc.Graph(id='figureTwitterFollower', config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoTwitterFollower")))]))]
        return content


    @staticmethod
    def createFollowerGraph(data, bgImage):
        figTwitterFollower = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        lastValidDate = datetime.strptime(data['Follower'].dropna().index.values[-1], '%Y-%m-%d')
        date2MonthsBack = lastValidDate - dateutil.relativedelta.relativedelta(days=30)

        trace_Follower = dict(type='scatter', name='followers', x=data['Follower'].dropna().index, y=data['Follower'].dropna(),
                                mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate='%{y:,.0f}')

        figTwitterFollower.add_trace(trace_Follower, 1, 1)

        figTwitterFollower.update_yaxes(title_text='Number of DefiChain-Followers', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figTwitterFollower.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                            row=1, col=1)       # select 14 days range: range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate]

        # Add range slider
        figTwitterFollower.update_layout(xaxis=dict(
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
        figTwitterFollower.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.25))

        figTwitterFollower.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                         yanchor="top",
                                         y=-0.12,
                                         xanchor="right",
                                         x=1),
                             )
        figTwitterFollower.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figTwitterFollower.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figTwitterFollower.layout.legend.font.color = '#6c757d'  # font color legend
        figTwitterFollower.layout.hoverlabel.bgcolor = 'white'
        return figTwitterFollower

    @staticmethod
    def createDiffFollowerGraph(data, bgImage):
        figTwitterFollowerChange = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        lastValidDate = datetime.strptime(data['Follower'].dropna().index.values[-1], '%Y-%m-%d')
        date2MonthsBack = lastValidDate - dateutil.relativedelta.relativedelta(days=30)

        trace_diff = dict(type='scatter', name='Daily change', x=(data['followedToday']-data['unfollowedToday']).dropna().index,
                          y=(data['followedToday']-data['unfollowedToday']).dropna(),
                          mode='lines', line=dict(color='#ff2ebe'), line_width=3, hovertemplate='%{y:,.0f}')
        trace_followed = dict(type='scatter', name='New followers', x=data['followedToday'].dropna().index, y=data['followedToday'].dropna(),
                          mode='lines', line=dict(color='#90dba8'), line_width=3, hovertemplate='%{y:,.0f}', fill='tozeroy')
        trace_unfollowed = dict(type='scatter', name='Gone followers', x=data['unfollowedToday'].dropna().index, y=-data['unfollowedToday'].dropna(),
                          mode='lines', line=dict(color='#ec9b98'), line_width=3, hovertemplate='%{y:,.0f}', fill='tozeroy')

        figTwitterFollowerChange.add_trace(trace_followed, 1, 1)
        figTwitterFollowerChange.add_trace(trace_unfollowed, 1, 1)
        figTwitterFollowerChange.add_trace(trace_diff, 1, 1)

        figTwitterFollowerChange.update_yaxes(title_text='Change DefiChain-Followers', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                            zerolinecolor='#6c757d', row=1, col=1)
        figTwitterFollowerChange.update_xaxes(title_text="Date", gridcolor='#6c757d', showticklabels=True, color='#6c757d', zerolinecolor='#6c757d',
                            row=1, col=1)       # select 14 days range: range=[date14DaysBack.strftime('%Y-%m-%d %H:%M:%S.%f'), lastValidDate]

        # Add range slider
        figTwitterFollowerChange.update_layout(xaxis=dict(
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
        figTwitterFollowerChange.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.25))

        figTwitterFollowerChange.update_layout(margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d"),
                             legend=dict(orientation="h",
                                         yanchor="top",
                                         y=-0.12,
                                         xanchor="right",
                                         x=1),
                             )
        figTwitterFollowerChange.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figTwitterFollowerChange.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figTwitterFollowerChange.layout.legend.font.color = '#6c757d'  # font color legend
        figTwitterFollowerChange.layout.hoverlabel.bgcolor = 'white'
        return figTwitterFollowerChange

    @staticmethod
    def getTwitterFollowerExplanation():
        twitterFollowerExplanation = [html.P(['One social media platform to reach more people is Twitter. Especially the bigger coins have a hugh community, spreading news and information about their project. ',
                                       'Here I want to track the DefiChain follower number.'],style={'text-align': 'justify'}),
                               html.P(['In addition to the pure representation of the absolute number, the daily rate of change is also evaluated. Therefore the list of all follower ID is saved '
                                       'for the next day. A comparison of the list data delivers the new followers and the gone ones. The difference is the daily change rate of DefiChain followers.'],style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return twitterFollowerExplanation