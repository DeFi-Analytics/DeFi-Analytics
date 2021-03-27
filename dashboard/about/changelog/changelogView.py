import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table


class changelogViewClass:

    def getChangelogContent(self, data):
        content = [dbc.Card(dbc.CardBody([dbc.Row(dbc.Col(self.createChangelogContent(data)))]))]
        return content

    @staticmethod
    def createChangelogContent(data):
        ChangeTableData = dash_table.DataTable(
                    id='table',
            #columns=[{"name": i, "id": i} for i in tableData.columns],
            columns=[{"name": 'Date', "id": 'Date'},
                     {"name": 'Version', "id": 'Version'},
                     {"name": 'Changes', "id": 'Changes'}],
            data=data.to_dict('records'),
            style_table={
                    'padding':'20px'},
            style_cell_conditional=[
                    {'if': {'column_id': 'Version'}, 'width': '5%'},
                    {'if': {'column_id': 'Changes'}, 'width': '85%'}],
            style_data={
                'width': '100px',
                'maxWidth': '100px',
                'minWidth': '100px',
                'whiteSpace': 'pre-line',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'height': 'auto',
                'backgroundColor': 'white',
                'color': "#6c757d",
                'textAlign': 'left'},
            style_header={
                'backgroundColor': '#f4f3f8',
                'color': "000",
                'fontWeight': 'bold',
                'textAlign': 'left'},

                )

        contentChangelog = [html.H4("Changelog"),
                            ChangeTableData]
        return contentChangelog