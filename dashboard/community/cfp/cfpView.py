import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash_table.Format import Format, Group
from dash_table import DataTable

class cfpViewClass:

    def getCFPContent(self):
        contentCFP = dbc.Card(dbc.CardBody([html.H4("CFP List"),
                                html.Table([html.Tr([html.Td(['Sort list by column: ']), html.Td(dcc.Dropdown(id='sortCFPColumnSelection', options=[{'label': 'Number', 'value': '#'},
                                                                                                                {'label': 'Requester', 'value': 'Requester'},
                                                                                                                {'label': 'DFI amount', 'value': 'dfi'},
                                                                                                                {'label': 'Result', 'value': 'result'}],
                                                                                                        value='#', clearable=False, style=dict(width='150px', verticalAlign="bottom")))]),
                                            html.Tr([html.Td(['Sorting order: ']), html.Td(dcc.Dropdown(id='sortCFPDirectionSelection', options=[{'label': 'Ascending', 'value': True},
                                                                                                                {'label': 'Descending', 'value': False}],
                                                                                                        value=False, clearable=False, style=dict(width='150px', verticalAlign="bottom")))])
                                ], style={'margin-bottom': 25}),
                               html.Span(id='cfpDataTable')]))

        return contentCFP

    @staticmethod
    def createCFPTable(data, sortCFPColumnSelection, sortCFPDirectionSelection):
        listLinks = []
        listResult = []
        listDFI = []

        data2Use = data.sort_values(by=sortCFPColumnSelection, ascending=sortCFPDirectionSelection)

        for index, row in data2Use.iterrows():
            listLinks.append(html.A(html.P('Link'),href=data2Use.loc[index,'Link to github'],target='_blank', className='defiLink'))
            if data2Use.loc[index,'result'] == 'passed':
                listResult.append(html.B(data2Use.loc[index, 'result'], style={'color': 'green'}))
            else:
                listResult.append(html.B(data2Use.loc[index,'result'],style={'color': 'red'}))
            listDFI.append(html.Div("{:,.0f}".format(data2Use.loc[index,'dfi']), style={'text-align': 'end'}))

        data2Use['Github'] = listLinks
        data2Use['Result'] = listResult
        data2Use['DFI'] = listDFI

        data2Show = data2Use[['#','Date','Title','Requester','Github','DFI','Result']]

        cfpDataTable = dbc.Table.from_dataframe(data2Show, striped=True, bordered=True, hover=True)

        return cfpDataTable