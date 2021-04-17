import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class twitterViewClass:

    def getTwitterContent(self, data, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info Twitter Activity"),
                              dbc.ModalBody(self.getTwitterExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfoTwitter", className="ml-auto"))], id="modalTwitter", size='xl'),
                   dbc.Card(dbc.CardBody([html.H4(['Twitter statistics']),
                                          dcc.Graph(figure=self.createTweetLikeGraph(data, bgImage), id='socialmediaTwitterTweetGraph', config={'displayModeBar': False}),
                                          dcc.Graph(figure=self.createTwitterUniqueUserGraph(data, bgImage), id='socialmediaTwitterUserGraph',config={'displayModeBar': False}),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfoTwitter")))]))]
        return content

    @staticmethod
    def createTweetLikeGraph(data, bgImage):
        figTwitter = make_subplots(
            rows=2, cols=1,
            vertical_spacing=0.15,
            row_width=[0.5, 0.5],  # from bottom to top
            specs=[[{}],
                   [{}]],
            shared_xaxes=True,
            subplot_titles=(['DefiChain Twitter activity', 'Likes for DefiChain-Tweets']))
        figTwitter.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figTwitter.layout.annotations[0].font.size = 20
        figTwitter.layout.annotations[1].font.color = '#6c757d'
        figTwitter.layout.annotations[1].font.size = 20

        # Tweets on Twitter
        trace_overall = dict(type='scatter', name='all', x=data['overall_Activity'].dropna().index.values[:-1], y=data['overall_Activity'].dropna().values[:-1],
                             mode='lines', line=dict(color='#da3832'), line_width=2, hovertemplate='%{y:.0f}')
        trace_defichain = dict(type='scatter', name='tagged with @defichain', x=data['defichain_Activity'].dropna().index.values[:-1], y=data['defichain_Activity'].dropna().values[:-1],
                               mode='lines', line=dict(color='#617dea'), line_width=2, hovertemplate='%{y:.0f}')
        trace_dfi = dict(type='scatter', name='tagged with $DFI', x=data['dfi_Activity'].dropna().index.values[:-1], y=data['dfi_Activity'].dropna().values[:-1],
                         mode='lines', line=dict(color='#22b852'), line_width=2, hovertemplate='%{y:.0f}')
        figTwitter.add_trace(trace_overall, 1, 1)
        figTwitter.add_trace(trace_defichain, 1, 1)
        figTwitter.add_trace(trace_dfi, 1, 1)

        # Likes of Defichain-tweets
        trace_likes = dict(type='scatter', name='Overall Likes', x=data['overall_Likes'].dropna().index.values[:-1], y=data['overall_Likes'].dropna().values[:-1],
                           mode='lines', line=dict(color='#ff9800'), line_width=2, hovertemplate='%{y:.0f}')
        figTwitter.add_trace(trace_likes, 2, 1)

        # add background picture
        figTwitter.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.79, sizex=0.5, sizey=0.5,  xanchor="center", yanchor="middle", opacity=0.2))
        figTwitter.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.21, sizex=0.5, sizey=0.5,  xanchor="center", yanchor="middle", opacity=0.2))

        figTwitter.update_yaxes(title_text='# tweets / day', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)  # ,range=[-50, 200]
        figTwitter.update_yaxes(title_text='# likes / day', tickformat=",.2f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=2, col=1)  # ,range=[-200000, 1000000]
        figTwitter.update_xaxes(gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figTwitter.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=2, col=1)
        figTwitter.update_layout(height=680,
                                 margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d"),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figTwitter.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figTwitter.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figTwitter.layout.legend.font.color = '#6c757d'  # font color legend
        return figTwitter

    @staticmethod
    def createTwitterUniqueUserGraph(data, bgImage):
        figTwitter = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=(['Unique users with DefiChain-Tweets']))
        figTwitter.layout.annotations[0].font.color = '#6c757d'  # subplot title font color
        figTwitter.layout.annotations[0].font.size = 20

        # Tweets on Twitter
        trace_overall = dict(type='scatter', name='overall', x=data['overall_UniqueUserOverall'].dropna().index.values[:-1], y=data['overall_UniqueUserOverall'].dropna().values[:-1],
                             mode='lines', line=dict(color='#410eb2'), line_width=2, hovertemplate='%{y:.0f}')
        trace_tweet = dict(type='scatter', name='with Tweets', x=data['overall_UniqueUserTweet'].dropna().index.values[:-1], y=data['overall_UniqueUserTweet'].dropna().values[:-1],
                           mode='lines', line=dict(color='#ff2ebe'), line_width=2, hovertemplate='%{y:.0f}', visible='legendonly')
        trace_reply = dict(type='scatter', name='with Replies', x=data['overall_UniqueUserReply'].dropna().index.values[:-1], y=data['overall_UniqueUserReply'].dropna().values[:-1],
                           mode='lines', line=dict(color='#00fffb'), line_width=2, hovertemplate='%{y:.0f}', visible='legendonly')
        trace_retweet = dict(type='scatter', name='with Retweets', x=data['overall_UniqueUserRetweet'].dropna().index.values[:-1], y=data['overall_UniqueUserRetweet'].dropna().values[:-1],
                             mode='lines', line=dict(color='#c2a634'), line_width=2, hovertemplate='%{y:.0f}', visible='legendonly')
        figTwitter.add_trace(trace_overall, 1, 1)
        figTwitter.add_trace(trace_tweet, 1, 1)
        figTwitter.add_trace(trace_reply, 1, 1)
        figTwitter.add_trace(trace_retweet, 1, 1)

        figTwitter.update_yaxes(title_text='# users / day', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                                zerolinecolor='#6c757d', row=1, col=1)  # ,range=[-50, 200]

        figTwitter.update_xaxes(gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figTwitter.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)

        # add background picture
        figTwitter.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.5, sizey=0.5,  xanchor="center", yanchor="middle", opacity=0.2))

        figTwitter.update_layout(height=350,
                                 margin={"t": 60, "l": 0, "b": 0, 'r': 0},
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d"),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.25,
                                             xanchor="right",
                                             x=1),
                                 )
        figTwitter.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figTwitter.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figTwitter.layout.legend.font.color = '#6c757d'  # font color legend
        return figTwitter

    @staticmethod
    def getTwitterExplanation():
        coinAddressCardExplanation = [html.P(['One social media platform to reach more people is Twitter. Especially the bigger coins have a hugh community, spreading news and information about their project. ',
                                       'Here I want to track the activity regarding DefiChain.'],style={'text-align': 'justify'}),
                               html.P(['The first diagram shows the number of tweets per day, regardless of the type (tweets, retweets and replies are captured). ',
                                       'However, it differs between the type of being tagged.'],style={'text-align': 'justify'}),
                               html.P(['The second diagram visualizes the number of likes per day for all DefiChain related tweets.']),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return coinAddressCardExplanation
