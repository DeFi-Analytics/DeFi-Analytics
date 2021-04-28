import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class portfolioViewClass:

    def getPortfolioContent(self, data, bgImage):
        content = [dbc.Card(dbc.CardBody([html.H4(['Community Project: Portfolio App']),
                                          html.P(['Defichain has a great community. More and more persons create their own projects to help others and bring value into the ecosystem.',html.Br(),
                                                  'The Portfolio App is a standalone tool to import and prepare your reward data on DefiChain. It needs the local Wallet and Node to get the '
                                                  'complete transaction and reward list. They are sum up on a daily base. Also the corresponding coin price is get via coingecko API.',
                                                  html.Br(),
                                                  'You want to know more? Have a look on: ',
                                                  html.A('https://defichain-wiki.com/wiki/DeFiChain-Portfolio', href='https://defichain-wiki.com/wiki/DeFiChain-Portfolio', target='_blank', className='defiLink')],
                                                 style={'text-align': 'justify'}),
                                          dcc.Graph(figure=self.createPortfolioDownloads(data, bgImage), id='figurePortfolioDownloads', config={'displayModeBar': False})]))]
        return content

    @staticmethod
    def createPortfolioDownloads(data, bgImage):
        figDownloads = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        allDownloadData = data['PortfolioWindows']+data['PortfolioMac']+data['PortfolioLinux']

        trace_downloadWindows = dict(type='scatter', name='Windows', x=data['PortfolioWindows'].dropna().index, y=data['PortfolioWindows'].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#ff00af'), line_width=0, hovertemplate='%{y:.f}', fill='tozeroy')
        trace_downloadMac = dict(type='scatter', name='Mac', x=data['PortfolioMac'].dropna().index, y=data['PortfolioMac'].dropna(), stackgroup='one',
                            mode='lines', line=dict(color='#ff7fd7'), line_width=0, hovertemplate='%{y:.f}', fill='tonexty')
        trace_downloadLinux = dict(type='scatter', name='Linux', x=data['PortfolioLinux'].dropna().index, y=data['PortfolioLinux'].dropna(), stackgroup='one',
                             mode='lines', line=dict(color='#ffbfeb'), line_width=0, hovertemplate='%{y:.f}', fill='tonexty')


        trace_allDownloads = dict(type='scatter', name='Overall', x=allDownloadData.dropna().index, y=allDownloadData.dropna(),
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:.f}')

        figDownloads.add_trace(trace_downloadWindows, 1, 1)
        figDownloads.add_trace(trace_downloadMac, 1, 1)
        figDownloads.add_trace(trace_downloadLinux, 1, 1)

        figDownloads.add_trace(trace_allDownloads, 1, 1)

        figDownloads.update_yaxes(title_text='Number downloads', tickformat=".f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figDownloads.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', row=1, col=1)

        figDownloads.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))



        figDownloads.update_layout(margin={"t": 20, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figDownloads.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDownloads.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDownloads.layout.legend.font.color = '#6c757d'  # font color legend
        return figDownloads
