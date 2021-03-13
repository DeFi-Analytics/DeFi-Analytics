from defichainAnalyticsController import defichainAnalyticsControllerClass

defichainAnalyticsController = defichainAnalyticsControllerClass()
app = defichainAnalyticsController.getApp()

if __name__ == "__main__":
    app.run_server(debug=False)
