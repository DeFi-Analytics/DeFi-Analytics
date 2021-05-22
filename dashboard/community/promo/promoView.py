import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class promoViewClass:

    def getPromoContent(self, data, bgImage):
        content = [dbc.Card(dbc.CardBody([html.H4(['Community Project: DefiChain Promo']),
                                          html.P(['Defichain has a great community. More and more persons create their own projects to help others and bring value into the ecosystem.',html.Br(),
                                                  'The Website Defichain Promo was set up to help others in promoting DefiChain on social media platforms. It started with providing Tweets as a quick-reply to existing Tweets. ',
                                                  'In the second stage they started collecting media to make more valuable posts. It is a really easy-to-use platform and a look worth. I also use it to save time in answering Tweets.',
                                                  html.Br(),
                                                  'You want to know more? Have a look on: ',
                                                  html.A('https://www.defichain-promo.com/', href='https://www.defichain-promo.com/', target='_blank', className='defiLink')],
                                                 style={'text-align': 'justify'}),
                                          html.Table([html.Tr([html.Td('Select graph for evaluation:'),
                                          html.Td(dcc.Dropdown(id='promoSelectGraph', options=[{'label': 'Daily incentive points', 'value': 'incentivePoints'},
                                                                                              {'label': 'Database posts/media', 'value': 'database'}],
                                                               value='incentivePoints', clearable=False, style=dict(verticalAlign="bottom")))])]),
                                          dcc.Graph(id='figurePromoDatabase', config={'displayModeBar': False})]))]
        return content

    @staticmethod
    def createPromoDatabaseFigure(data, bgImage):
        figPromoDB = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        trace_activePosts = dict(type='scatter', name='Available Twitter Posts', x=data['postActive'].dropna().index, y=data['postActive'].dropna(),
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:.f}')
        trace_activeMedia = dict(type='scatter', name='Available Media', x=data['mediaActive'].dropna().index, y=data['mediaActive'].dropna(),
                                  mode='lines', line=dict(color='#7f50ff'), line_width=3, hovertemplate='%{y:.f}')

        figPromoDB.add_trace(trace_activePosts, 1, 1)
        figPromoDB.add_trace(trace_activeMedia, 1, 1)


        figPromoDB.update_yaxes(title_text='Number elements', tickformat=".f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figPromoDB.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', row=1, col=1)

        figPromoDB.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))



        figPromoDB.update_layout(margin={"t": 20, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figPromoDB.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figPromoDB.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figPromoDB.layout.legend.font.color = '#6c757d'  # font color legend
        return figPromoDB

    @staticmethod
    def createPromoIncentiveFigure(data, bgImage):
        figPromoIncentive = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        trace_incentivePoints = dict(type='scatter', name='Daily overall incentive points', x=data['incentivePointsToday'].dropna().index, y=data['incentivePointsToday'].dropna(),
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:.0f}')

        figPromoIncentive.add_trace(trace_incentivePoints, 1, 1)



        figPromoIncentive.update_yaxes(title_text='Daily incentive promo points (all users)', tickformat=".f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figPromoIncentive.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', row=1, col=1)

        figPromoIncentive.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))



        figPromoIncentive.update_layout(margin={"t": 20, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figPromoIncentive.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figPromoIncentive.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figPromoIncentive.layout.legend.font.color = '#6c757d'  # font color legend
        return figPromoIncentive