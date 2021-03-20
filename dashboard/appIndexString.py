class appIndexStringClass:
    @staticmethod
    def getAppIndexString():
        #the index string adds information to the html code like meta-tags, google-analytics or scripts.
        #the brackets{%xxx%} merge the content generated at another place to the defined html
        index_string = '''
        <!DOCTYPE html>
        <html>
            <head> 
                {%metas%}
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
