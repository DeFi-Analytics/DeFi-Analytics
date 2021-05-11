from dash.dependencies import Input, Output, State


class promoCallbacksClass:
    def __init__(self, defichainAnalyticsModel, promoView, app):

        @app.callback(Output('figurePromoDatabase', 'figure'),
                      [Input('promoSelectGraph', 'value')])
        def selectGraph(selectedRepresentation):
            if selectedRepresentation == 'database':
                figPromo = promoView.createPromoDatabaseFigure(defichainAnalyticsModel.dailyData, defichainAnalyticsModel.figBackgroundImage)
            else:
                figPromo = promoView.createPromoIncentiveFigure(defichainAnalyticsModel.dailyData, defichainAnalyticsModel.figBackgroundImage)
            return figPromo

