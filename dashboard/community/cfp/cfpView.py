import dash_html_components as html
import dash_bootstrap_components as dbc



from dash_table.Format import Format, Group
from dash_table import DataTable

class cfpViewClass:

    def getCFPContent(self, data):
        content = [dbc.Card(dbc.CardBody([dbc.Row(dbc.Col(self.createCFPTableContent(data)))]))]
        return content

    @staticmethod
    def createCFPTableContent(data):
        data['Link'] = 'Link'
        ChangeTableData = DataTable(
                    id='table',
            #columns=[{"name": i, "id": i} for i in tableData.columns],
            columns=[{"name": '#', "id": 'nb'},
                     {"name": 'Date', "id": 'Date'},
                     {"name": 'Title', "id": 'Title'},
                     {"name": 'Requester', "id": 'Requester'},
                     {"name": 'Github', "id": 'Link'},
                     dict(name='DFI', id='DFI', type='numeric', format=Format().group(True)),
                     {"name": 'Result', "id": 'result'},],
            data=data.to_dict('records'),
            # style_table={
            #        'padding':'20px'},
            style_data={
                'font-size': '14px',
                'font-family': 'monospace',
                # 'width': '100px',
                # 'maxWidth': '100px',
                # 'minWidth': '100px',
                'whiteSpace': 'pre-line',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'height': 'auto',
                },
            style_data_conditional=[
                {'if': {'row_index': 'odd',
                        'column_id': 'nb'},
                 'backgroundColor': '#f0f0f0'},
                {'if': {'row_index': 'odd',
                        'column_id': 'Date'},
                 'backgroundColor': '#f0f0f0'},
                {'if': {'row_index': 'odd',
                        'column_id': 'Title'},
                 'backgroundColor': '#f0f0f0'},
                {'if': {'row_index': 'odd',
                        'column_id': 'Requester'},
                 'backgroundColor': '#f0f0f0'},
                {'if': {'row_index': 'odd',
                        'column_id': 'Link'},
                 'backgroundColor': '#f0f0f0'},
                {'if': {'row_index': 'odd',
                        'column_id': 'DFI'},
                 'backgroundColor': '#f0f0f0'},
                {'if': {'column_id': 'Link'},
                 'textDecoration': 'underline',
                 'textAlign': 'left'},
            ],
            style_cell_conditional=[
                {'if': {'column_id': 'nb'},
                 'width': '30px',
                 'maxWidth': '30px',
                 'minWidth': '30px'},
                {'if': {'column_id': 'Date'},
                 'width': '75px',
                 'maxWidth': '75px',
                 'minWidth': '75px'},
                {'if': {'column_id': 'Title'},
                 'width': '60%',
                 'textAlign': 'left'},
                {'if': {'column_id': 'Requester'},
                 'width': '40%',
                 'textAlign': 'left'},
                {'if': {'column_id': 'Link'},
                 'width': '60px',
                 'maxWidth': '60px',
                 'minWidth': '60px',
                 'color': '#1d9bf0'},
                {'if': {'column_id': 'DFI'},
                 'width': '85px',
                 'maxWidth': '85px',
                 'minWidth': '85px'},
                {'if': {'column_id': 'result'},
                 'width': '80px',
                 'maxWidth': '80px',
                 'minWidth': '80px',
                 'textAlign': 'left'},
                {'if': {'column_id': 'result',
                        'filter_query': '{result} = declined'},
                 'backgroundColor': 'red',
                 'color': 'white'},
                {'if': {'column_id': 'result',
                        'filter_query': '{result} = passed'},
                 'backgroundColor': 'green',
                 'color': 'white'},
            ],

            style_header={
                'backgroundColor': '#c5c5c5',
                'color': "000",
                'fontWeight': 'bold',
                'textAlign': 'left'},

                )

        contentChangelog = [html.H4("CFP List"),
                            ChangeTableData]
        return contentChangelog