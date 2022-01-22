import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class dfxViewClass:

    def getDFXContent(self):
        content = [dbc.Card(dbc.CardBody([html.H4(['Community Project: DFX']),
                                          html.P(['Defichain has a great community. More and more persons create their own projects to help others and bring value into the ecosystem.',html.Br(),
                                                  'The service of DFX was set up to have an easy entry to the DefiChain ecosystem. You can buy any defichain token with a simple SEPA bank transfer. ',
                                                  'The company in the background will buy your wished tokens and transfer them directly to your wallet. So, you will be the owner of the private keys. ',
                                                  'The idea is to have the opportunity to create different saving plans for the upcoming decentralized assets and cryptos. ',
                                                  html.Br(),
                                                  'You want to know more? Have a look on: ',
                                                  html.A('https://dfx.swiss/', href='https://dfx.swiss/', target='_blank', className='defiLink')],
                                                 style={'text-align': 'justify'}),
                                          html.Table([html.Tr([html.Td('Select graph for evaluation:'),
                                          html.Td(dcc.Dropdown(id='dfxSelectGraph', options=[{'label': 'Total DFI volume', 'value': 'totalDFIvolume'},
                                                                                               {'label': 'Daily DFI volume', 'value': 'dailyDFIvolume'}],
                                                               value='totalDFIvolume', clearable=False, style=dict(verticalAlign="bottom")))])]),
                                          dcc.Graph(id='figureDFXdata', config={'displayModeBar': False})]))]
        return content

    @staticmethod
    def createDFXFigure(data, bgImage, representation):
        figDFX = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        if representation=='dailyDFIvolume':
            nameBuyVolume = 'Daily volume'
            temp = data['dfxBuyVolume'].dropna()
            xdata = temp.groupby(temp.index.floor('d')).last().diff().index
            ydata = temp.groupby(temp.index.floor('d')).last().diff()
        else:
            nameBuyVolume = 'Overall volume'
            xdata = data['dfxBuyVolume'].dropna().index
            ydata = data['dfxBuyVolume'].dropna()


        trace_buyVolume = dict(type='scatter', name=nameBuyVolume, x=xdata, y=ydata,
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:,.4f}')


        figDFX.add_trace(trace_buyVolume, 1, 1)


        figDFX.update_yaxes(title_text='Buy volume in DFI', tickformat=",.f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figDFX.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', row=1, col=1)

        figDFX.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))



        figDFX.update_layout(margin={"t": 20, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figDFX.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDFX.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDFX.layout.legend.font.color = '#6c757d'  # font color legend
        return figDFX

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


    @staticmethod
    def createPromoUsersFigure(data, bgImage):
        figPromoUser = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        trace_incentivePoints = dict(type='scatter', name='Defichain Promo users', x=data['incentiveUsers'].dropna().index, y=data['incentiveUsers'].dropna(),
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:.0f}')

        figPromoUser.add_trace(trace_incentivePoints, 1, 1)



        figPromoUser.update_yaxes(title_text='Number incentive program users', tickformat=".f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figPromoUser.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', row=1, col=1)

        figPromoUser.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))



        figPromoUser.update_layout(margin={"t": 20, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figPromoUser.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figPromoUser.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figPromoUser.layout.legend.font.color = '#6c757d'  # font color legend
        return figPromoUser