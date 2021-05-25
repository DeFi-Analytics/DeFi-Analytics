import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class analyticsViewClass:

    def getAnalyticsContent(self, data, bgImage):
        content = [dbc.Card(dbc.CardBody([html.H4(['Community Project: Defichain-Analytics']),
                                          html.P(['Defichain has a great community. More and more persons create their own projects to help others and bring value into the ecosystem.',html.Br(),
                                                  'As all other community projects I am tracking my own Dashboard regarding the daily visits. My personal goal is bringing more and more people '
                                                  'facts and figures about the value of DefiChain.'],
                                                 style={'text-align': 'justify'}),
                                          dcc.Graph(figure=self.createAnalyticsIncome(data, bgImage), id='figureAnalyticsIncome', config={'displayModeBar': False})]))]
        return content

    @staticmethod
    def createAnalyticsIncome(data, bgImage):
        figVisits = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        trace_IncomeVisits = dict(type='scatter', name='Visits', x=data['analyticsVisits'].dropna().index, y=data['analyticsVisits'].dropna(),
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
