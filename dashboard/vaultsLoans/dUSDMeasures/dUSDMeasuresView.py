import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd

from datetime import datetime
import dateutil.relativedelta

from plotly.subplots import make_subplots


class dUSDMeasuresViewClass:

    def getdUSDMeasuresContent(self, dailyData, hourlyData, bgImage):
        content = [dbc.Modal([dbc.ModalHeader("Info dUSD Measures"),
                              dbc.ModalBody(self.getdUSDMeasuresExplanation()),
                              dbc.ModalFooter(dbc.Button("close", id="closeInfodUSDMeasures", className="ml-auto"))],
                                    id="modaldUSDMeasures", size='xl'),
                   html.Div(id='hidden', style = {'display':'none'}),
                   dbc.Card(dbc.CardBody([html.H4(['dUSD Measures']),
                                          html.Div(['On this page all introduced measures to move the dUSD value towards 1 USD are evaluated.'], style={'margin-bottom': '30px'}),
                                          html.H5(['dUSD burn rate']),
                                          html.Table([html.Tr([html.Td('Select time base for representation:'),
                                                               html.Td(dcc.Dropdown(id='dUSDBurnTimeSelection',
                                                                                    options=[{'label': 'Hourly burn rate', 'value': 'H'},
                                                                                             {'label': 'Daily burn rate', 'value': 'D'},
                                                                                             {'label': 'Weekly burn rate', 'value': 'W'}],
                                                                                    value='D', clearable=False, style=dict(width='200px', verticalAlign="bottom")))])]),
                                          dbc.Row(dbc.Col(dcc.Graph(config={'displayModeBar': False}, id='figureDUSDBurn'))),
                                          html.H5(['DEX stabilizing fee'], style={'margin-top': '30px'}),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createDUSDStabFeeFig(dailyData, bgImage), config={'displayModeBar': False}, id='figureDUSDStabFee'))),
                                          html.H5(['dUSD Negative interest rate'], style={'margin-top': '30px'}),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createDUSDNegativeInterestFig(dailyData, bgImage), config={'displayModeBar': False}, id='figureDUSDNegInterest'))),
                                          html.H5(['Block reward dUSD burn bot'], style={'margin-top': '30px'}),
                                          dbc.Row(dbc.Col(dcc.Graph(figure=self.createDUSDBurnBlockRewardFig(dailyData, bgImage), config={'displayModeBar': False}, id='figureDUSDBurnBlockReward'))),
                                          dbc.Row(dbc.Col(dbc.Button("Info/Explanation", id="openInfodUSDMeasures")))
                                          ]))]
        return content



    @staticmethod
    def createDUSDStabFeeFig(data, bgImage):
        figDUSDFee = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))


        lastValidDate = datetime.strptime(data['sellDUSDFee'].dropna().index.values[-1], '%Y-%m-%d')
        date30DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(months=2)


        trace_dUSDStabFee = dict(type='scatter', name='DEX stabilizing fee',
                         x=data['sellDUSDFee'].dropna().index, y=data['sellDUSDFee'].dropna()*100,
                         mode='lines', line=dict(color='#ff00af'), line_width=2, hovertemplate='%{y:,.2f}%')
        figDUSDFee.add_trace(trace_dUSDStabFee, 1, 1)

        figDUSDFee.update_yaxes(title_text='DEX stabilizing fee in %', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d', row=1, col=1)  # ,range=[-50, 200]
        figDUSDFee.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date30DaysBack, lastValidDate], row=1, col=1)

        # Add range slider
        figDUSDFee.update_layout(xaxis=dict(
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
        figDUSDFee.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figDUSDFee.update_layout(margin={"t": 40, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d",
                                             bgcolor='#ffffff', ),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )
        figDUSDFee.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDUSDFee.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDUSDFee.layout.legend.font.color = '#6c757d'  # font color legend

        return figDUSDFee

    @staticmethod
    def createDUSDNegativeInterestFig(data, bgImage):
        figDUSDNegativeInterest = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))


        lastValidDate = datetime.strptime(data['interestDUSDLoans'].dropna().index.values[-1], '%Y-%m-%d')
        date30DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(months=2)


        trace_dUSDNegInterest = dict(type='scatter', name='Negative interest rate',
                         x=data['interestDUSDLoans'].dropna().index, y=data['interestDUSDLoans'].dropna(),
                         mode='lines', line=dict(color='#ff00af'), line_width=2, hovertemplate='%{y:,.2f}%')
        figDUSDNegativeInterest.add_trace(trace_dUSDNegInterest, 1, 1)

        figDUSDNegativeInterest.update_yaxes(title_text='Negative interest rate for dUSD loans in %', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                                             autorange="reversed", zerolinecolor='#6c757d', row=1, col=1)  # ,range=[-50, 200]
        figDUSDNegativeInterest.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date30DaysBack, lastValidDate], row=1, col=1)

        # Add range slider
        figDUSDNegativeInterest.update_layout(xaxis=dict(
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
        figDUSDNegativeInterest.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figDUSDNegativeInterest.update_layout(margin={"t": 40, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d",
                                             bgcolor='#ffffff', ),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )
        figDUSDNegativeInterest.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDUSDNegativeInterest.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDUSDNegativeInterest.layout.legend.font.color = '#6c757d'  # font color legend

        return figDUSDNegativeInterest

    @staticmethod
    def createDUSDBurnBlockRewardFig(data, bgImage):
        figDUSDBurnBlockReward = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))


        lastValidDate = datetime.strptime(data['rewardDUSDBurnBot'].dropna().index.values[-1], '%Y-%m-%d')
        date30DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(months=2)


        trace_dUSDBurnBlockReward = dict(type='scatter', name='Block reward burn bot',
                         x=data['rewardDUSDBurnBot'].dropna().index, y=data['rewardDUSDBurnBot'].dropna()*100,
                         mode='lines', line=dict(color='#ff00af'), line_width=2, hovertemplate='%{y:,.2f}%')
        figDUSDBurnBlockReward.add_trace(trace_dUSDBurnBlockReward, 1, 1)

        figDUSDBurnBlockReward.update_yaxes(title_text='Part dToken block reward for burn bot in %', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                                              zerolinecolor='#6c757d', row=1, col=1)  # ,range=[-50, 200]
        figDUSDBurnBlockReward.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                            range=[date30DaysBack, lastValidDate], row=1, col=1)

        # Add range slider
        figDUSDBurnBlockReward.update_layout(xaxis=dict(
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
        figDUSDBurnBlockReward.add_layout_image(dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6,  xanchor="center", yanchor="middle", opacity=0.2))

        figDUSDBurnBlockReward.update_layout(margin={"t": 40, "l": 0, "b": 0, 'r': 0},
                             hovermode='x unified',
                             hoverlabel=dict(font_color="#6c757d",
                                             bgcolor='#ffffff', ),
                             legend=dict(orientation="h",
                                             yanchor="top",
                                             y=-0.12,
                                             xanchor="right",
                                             x=1),
                             )
        figDUSDBurnBlockReward.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDUSDBurnBlockReward.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDUSDBurnBlockReward.layout.legend.font.color = '#6c757d'  # font color legend

        return figDUSDBurnBlockReward

    @staticmethod
    def createDUSDBurnFig(data, bgImage, selectedGraph):
        figDUSDBurnedBot = make_subplots(
            rows=1, cols=1,
            vertical_spacing=0.15,
            row_width=[1],  # from bottom to top
            specs=[[{}]],
            shared_xaxes=True,
            subplot_titles=([]))
        dataSumDEXBurn = data['burnedDUSDDEX'] - data['DUSDBurnBot_SumDUSDAmount'] - data['DUSDBurnBot2_SumDUSDAmount']

        burnedBotData = data['DUSDBurnBot_SumDUSDAmount'].groupby(pd.Grouper(freq=selectedGraph)).first().diff().shift(-1)
        burnedBot2Data = data['DUSDBurnBot2_SumDUSDAmount'].groupby(pd.Grouper(freq=selectedGraph)).first().diff().shift(-1)
        burnedDEXData = dataSumDEXBurn.groupby(pd.Grouper(freq=selectedGraph)).first().diff().shift(-1)

        dataOverallBurned = burnedBotData+burnedBot2Data+burnedDEXData


        lastValidDate = datetime.strptime(str(burnedBotData.dropna().index.values[-1])[:10], '%Y-%m-%d')
        date30DaysBack = lastValidDate - dateutil.relativedelta.relativedelta(months=2)

        trace_dTokenBurnBot = dict(type='scatter', name='dUSD burned via Bot', x=burnedBotData.dropna().index, y=burnedBotData.dropna(),
                                   mode='lines', line=dict(color='#711714'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f} dUSD', fill='tozeroy')
        figDUSDBurnedBot.add_trace(trace_dTokenBurnBot, 1, 1)
        trace_dTokenBurnBot2 = dict(type='scatter', name='dUSD burned via Bot 2 (free DFI rewards)', x=burnedBot2Data.dropna().index, y=burnedBot2Data.dropna(),
                                   mode='lines', line=dict(color='#270806'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f} dUSD', fill='tonexty')
        figDUSDBurnedBot.add_trace(trace_dTokenBurnBot2, 1, 1)
        trace_dTokenFeeBurn = dict(type='scatter', name='dUSD burned via DEX-Fee', x=burnedDEXData.dropna().index, y=burnedDEXData.dropna(),
                                   mode='lines', line=dict(color='#696969'), line_width=0, stackgroup='one', hovertemplate='%{y:,.f} dUSD', fill='tonexty')
        figDUSDBurnedBot.add_trace(trace_dTokenFeeBurn, 1, 1)


        trace_overallBurned = dict(type='scatter', name='Overall burned dUSD',
                                         x=dataOverallBurned.dropna().index, y=dataOverallBurned.dropna(),
                                         mode='lines', line=dict(color='#ff00af'), line_width=2, hovertemplate='%{y:,.2f} dUSD')
        figDUSDBurnedBot.add_trace(trace_overallBurned, 1, 1)

        figDUSDBurnedBot.update_yaxes(title_text='Daily dUSD burn', tickformat=",.0f", gridcolor='#6c757d', color='#6c757d',
                                            zerolinecolor='#6c757d', row=1, col=1)  # ,range=[-50, 200]
        figDUSDBurnedBot.update_xaxes(title_text="Date", gridcolor='#6c757d', color='#6c757d', zerolinecolor='#6c757d',
                                            range=[date30DaysBack, lastValidDate], row=1, col=1)

        # Add range slider
        figDUSDBurnedBot.update_layout(xaxis=dict(
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
        figDUSDBurnedBot.add_layout_image(
            dict(source=bgImage, xref="paper", yref="paper", x=0.5, y=0.5, sizex=0.6, sizey=0.6, xanchor="center", yanchor="middle", opacity=0.2))

        figDUSDBurnedBot.update_layout(margin={"t": 40, "l": 0, "b": 0, 'r': 0},
                                             hovermode='x unified',
                                             hoverlabel=dict(font_color="#6c757d",
                                                             bgcolor='#ffffff', ),
                                             legend=dict(orientation="h",
                                                         yanchor="top",
                                                         y=-0.12,
                                                         xanchor="right",
                                                         x=1),
                                             )
        figDUSDBurnedBot.layout.plot_bgcolor = '#ffffff'  # background plotting area
        figDUSDBurnedBot.layout.paper_bgcolor = 'rgba(0,0,0,0)'  # background around plotting area
        figDUSDBurnedBot.layout.legend.font.color = '#6c757d'  # font color legend

        return figDUSDBurnedBot

    @staticmethod
    def getdUSDMeasuresExplanation():
        dUSDMeasuresCardExplanation = [html.P(['Different measures were introduce on DeFiChain to increase the value of dUSD. On this evaluation the current active ones are represented:',
                                            html.Ul([html.Li([html.B('DEX stabilizing fee: '), 'This fee must be paid in case of selling dUSD to any crypto assets (e.g. DFI) and was introduced to ',
                                                              'make shorting dUSD unattractive.']),
                                                     html.Li([html.B('dUSD Negative interest rate: '), 'Half of the paid DEX stablizing fee is distributed to dUSD loan owners. ',
                                                              'With the negative interest rate opening a dUSD loan is more attractive and this increased the demand of DFI and dUSD.']),
                                                     html.Li([html.B('Block reward dUSD burn bot: '), 'A dUSD burn bot was installed to buy dUSD with some DFI block rewards and burn them. ',
                                                              'The DFI block rewards are part of the 30% dToken rewards and were taken from the DFI-dUSD pool.']),
                                                     html.Li([html.B('Daily dUSD burn via bot: '), 'The dUSD burn bot continuously swaps DFI to dUSD and burn them. ',
                                                              'This graph shows the daily burn, where the value depends on the used block rewards and the dUSD-DFI pool ratio.']),])],
                                    style={'text-align': 'justify'}),
                               html.P([html.B('Hint:'),' The presented diagrams are interactive. You can zoom in (select range with mouse) and rescale (double-click in diagram) as you like.'
                                       ' For specific questions it could be helpful to only show a selection of the available data. To exclude entries from the graph click on the corresponding legend entry.'],
                                        style={'text-align': 'justify', 'fontSize':'0.7rem','color':'#6c757d'})
                               ]
        return dUSDMeasuresCardExplanation