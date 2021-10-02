import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class dfiSignalViewClass:

    def getDFISignalContent(self, data, bgImage):
        content = [dbc.Card(dbc.CardBody([html.H4(['Community Project: DFI Signal']),
                                          html.P(['Defichain has a great community. More and more persons create their own projects to help others and bring value into the ecosystem.',html.Br(),
                                                  'DFI-Signal is a Telegram bot, which informs you about your masternode. You will get a message, when a new block is minted or you request some statistics. ',
                                                  'They also work together with Masternode Monitor, so you can easily use the same sync key.',
                                                  html.Br(),
                                                  'You want to know more? Have a look on: ',
                                                  html.A('https://dfi-signal.com/', href='https://dfi-signal.com/', target='_blank', className='defiLink')],
                                                 style={'text-align': 'justify'}),
                                          dcc.Graph(figure=self.createUserMNCount(data, bgImage), id='figureDFISignal', config={'displayModeBar': False})]))]
        return content

    @staticmethod
    def createUserMNCount(data, bgImage):
        figSignal = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        trace_signalUsers = dict(type='scatter', name='Users', x=data['user_count'].dropna().index, y=data['user_count'].dropna(),
                                  mode='lines', line=dict(color='#ff7fd7'), line_width=3, hovertemplate='%{y:.f}')
        figSignal.add_trace(trace_signalUsers, 1, 1)

        trace_signalMN = dict(type='scatter', name='Masternodes', x=data['masternode_count'].dropna().index, y=data['masternode_count'].dropna(),
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:.f}')
        figSignal.add_trace(trace_signalMN, 1, 1)

        figSignal.update_yaxes(title_text='Number', tickformat=".f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figSignal.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', row=1, col=1)

        figSignal.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))



        figSignal.update_layout(margin={"t": 20, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figSignal.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figSignal.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figSignal.layout.legend.font.color = '#6c757d'  # font color legend
        return figSignal
