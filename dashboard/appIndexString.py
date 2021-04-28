class appIndexStringClass:
    @staticmethod
    def getAppIndexString():
        #the index string adds information to the html code like meta-tags, google-analytics or scripts.
        #the brackets{%xxx%} merge the content generated at another place to the defined html
        index_string = '''
        <!DOCTYPE html>
        <html>
            <head> 
                <script async src="https://www.googletagmanager.com/gtag/js?id=UA-194128823-1"></script>
                <script>
                  window.dataLayer = window.dataLayer || [];
                  function gtag(){dataLayer.push(arguments);}
                  gtag('js', new Date());
                
                  gtag('config', 'UA-194128823-1');
                </script>
                {%metas%}
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta property="og:image" content="https://www.defichain-analytics.com/static/images/analyticsPortraitBlack.png">
                <meta name="description" content="Keys and figures about DefiChain. Tracking and analyzing blockchain data for more insights.">
                <title>DefiChain Analytics Dashboard</title>
                <meta name="twitter:card" content="summary_large_image">
                <meta name="twitter:title" content="DefiChain Analytics Dashboard">
                <meta name="twitter:description" content="Keys and figures about DefiChain. Tracking and analyzing blockchain data for more insights.">
                <meta name="twitter:image" content="https://www.defichain-analytics.com/static/images/analyticsTwitterCard.png">
                {%favicon%}
                {%css%}
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
        '''
        return index_string
