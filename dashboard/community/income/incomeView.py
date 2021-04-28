import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class incomeViewClass:

    def getIncomeContent(self, data, bgImage):
        content = [dbc.Card(dbc.CardBody([html.H4(['Community Project: Defichain-Income']),
                                          html.P(['Defichain has a great community. More and more persons create their own projects to help others and bring value into the ecosystem.',html.Br(),
                                                  'The Website DefiChain-Income was set up to calculate and track your revenues from defichain. It started with calculating your liquidity mining rewards '
                                                     'based on your holdings of liquidity token or just simpler by giving your DFI address holding the token. All information is get from public APIs '
                                                  'and so running a node from user side is not needed.',
                                                  html.Br(),
                                                  'You want to know more? Have a look on: ',
                                                  html.A('https://www.defichain-income.com/', href='https://www.defichain-income.com/', target='_blank', className='defiLink')],
                                                 style={'text-align': 'justify'}),
                                          dcc.Graph(figure=self.createVisitsIncome(data, bgImage), id='figureVisitsIncome', config={'displayModeBar': False})]))]
        return content

    @staticmethod
    def createVisitsIncome(data, bgImage):
        figVisits = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        trace_IncomeVisits = dict(type='scatter', name='Visits', x=data['incomeVisits'].dropna().index, y=data['incomeVisits'].dropna(),
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate='%{y:.f}', fill='tozeroy')
        figVisits.add_trace(trace_IncomeVisits, 1, 1)
        figVisits.update_yaxes(title_text='Visits/day', tickformat=".f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figVisits.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', row=1, col=1)

        figVisits.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))



        figVisits.update_layout(margin={"t": 20, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figVisits.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figVisits.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figVisits.layout.legend.font.color = '#6c757d'  # font color legend
        return figVisits
