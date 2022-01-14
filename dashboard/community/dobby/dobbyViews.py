import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots


class dobbyViewClass:

    def getDobbyContent(self):
        content = [dbc.Card(dbc.CardBody([html.H4(['Community Project: Dobby']),
                                          html.P(['Defichain has a great community. More and more persons create their own projects to help others and bring value into the ecosystem.',html.Br(),
                                                  'The service of Dobby was set up to monitor the liquidation risk of your vault. You can define a collateralization level where you get '
                                                  'a warning message via telegram.',
                                                  html.Br(),
                                                  'You want to know more? Have a look on: ',
                                                  html.A('https://defichain-dobby.com/', href='https://defichain-dobby.com/', target='_blank', className='defiLink')],
                                                 style={'text-align': 'justify'}),
                                          html.Table([html.Tr([html.Td('Select graph for evaluation:'),
                                          html.Td(dcc.Dropdown(id='dobbySelectGraph', options=[{'label': 'Users & Vaults', 'value': 'usersVaults'},
                                                                                             {'label': 'Collateral & Loans', 'value': 'collateralLoan'},
                                                                                             {'label': 'Messages', 'value': 'messages'},],
                                                               value='usersVaults', clearable=False, style=dict(verticalAlign="bottom")))])]),
                                          dcc.Graph(id='figureDobbydata', config={'displayModeBar': False})]))]
        return content

    @staticmethod
    def createDobbyFigure(data, bgImage, representation):
        figDobby = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))

        if representation=='messages':
            name1 = 'messages'
            xdata1 = data['sum_messages'].dropna().index
            ydata1 = data['sum_messages'].dropna()
            name2 = '...'
            xdata2 = xdata1
            ydata2 = ydata1
            ylabel = 'Number'
            hoverRepresentation = '%{y:.f}'
            tickRepresentation = ".f"
        if representation=='collateralLoan':
            name1 = 'Loans'
            xdata1 = data['sum_loan'].dropna().index
            ydata1 = data['sum_loan'].dropna()
            name2 = 'Collateral'
            xdata2 = data['sum_collateral'].dropna().index
            ydata2 = data['sum_collateral'].dropna()
            ylabel = 'USD value'
            hoverRepresentation = '%{y:,.f}'
            tickRepresentation = ",.f"
        else:
            name1 = 'Vaults'
            xdata1 = data['vault_count'].dropna().index
            ydata1 = data['vault_count'].dropna()
            name2 = 'Users'
            xdata2 = data['user_count'].dropna().index
            ydata2 = data['user_count'].dropna()
            ylabel = 'Number'
            hoverRepresentation = '%{y:.f}'
            tickRepresentation = ".f"



        trace1 = dict(type='scatter', name=name1, x=xdata1, y=ydata1,
                                  mode='lines', line=dict(color='#ff7fd7'), line_width=3, hovertemplate=hoverRepresentation)


        trace2 = dict(type='scatter', name=name2, x=xdata2, y=ydata2,
                                  mode='lines', line=dict(color='#ff00af'), line_width=3, hovertemplate=hoverRepresentation)

        figDobby.add_trace(trace1, 1, 1)
        if representation != 'messages':
            figDobby.add_trace(trace2, 1, 1)

        figDobby.update_yaxes(title_text=ylabel, tickformat=tickRepresentation, gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)
        figDobby.update_xaxes(title_text="Date", gridcolor='#6c757d', zerolinecolor='#6c757d', color='#6c757d', row=1, col=1)

        figDobby.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.35, sizey=0.35,  xanchor="center", yanchor="middle", opacity=0.2))



        figDobby.update_layout(margin={"t": 20, "l": 0, "b": 0, "r": 0},
                                 barmode='stack',
                                 hovermode='x unified',
                                 hoverlabel=dict(font_color="#6c757d", bgcolor='#ffffff'),
                                 legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                                 )
        figDobby.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDobby.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDobby.layout.legend.font.color = '#6c757d'  # font color legend
        return figDobby

