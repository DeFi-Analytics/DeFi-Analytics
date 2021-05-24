import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class mnMonitorViewClass:

    def getmnMonitorContent(self, data, bgImage):
        content = [dbc.Card(dbc.CardBody([html.H4(['Community Project: Masternode Monitor']),
                                          html.P(['Defichain has a great community. More and more persons create their own projects to help others and bring value into the ecosystem.',html.Br(),
                                                  'Masternode Monitor is an application for tracking the minting activities of your DeFiChain masternodes. This helps you getting an overview '
                                                  'of how they perform and keep track of their activities in the past. It uses public APIs with your collateral address. The privacy is ensured, because data '
                                                  'is only stored im browser',
                                                  html.Br(),
                                                  'You want to know more? Have a look on: ',
                                                  html.A('https://www.defichain-masternode-monitor.com/', href='https://www.defichain-masternode-monitor.com/', target='_blank', className='defiLink')],
                                                 style={'text-align': 'justify'}),
                                          dcc.Graph(figure=self.createNodesAccounts(data, bgImage), id='figureVisitsIncome', config={'displayModeBar': False})]))]
        return content

    @staticmethod
    def createNodesAccounts(data, bgImage):
        figMonitor = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        trace_monitorNbMN = dict(type='scatter', name='Masternodes', x=data['nbMasternodes'].dropna().index, y=data['nbMasternodes'].dropna(),
                                  mode='lines', line=dict(color='#ff7fd7'), line_width=3, hovertemplate='%{y:.f}')
        figMonitor.add_trace(trace_monitorNbMN, 1, 1)

        trace_monitorNbAccounts = dict(type='scatter', name='Accounts', x=data['nbAccounts'].dropna().index, y=data['nbAccounts'].dropna(),
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:.f}')
        figMonitor.add_trace(trace_monitorNbAccounts, 1, 1)

        figMonitor.update_yaxes(title_text='Number', tickformat=".f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figMonitor.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', row=1, col=1)

        figMonitor.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))



        figMonitor.update_layout(margin={"t": 20, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figMonitor.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figMonitor.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figMonitor.layout.legend.font.color = '#6c757d'  # font color legend
        return figMonitor
