import requests

import pandas as pd


link = 'http://api.mydeficha.in/v1/listmasternodes/?state=ENABLED'
siteContent = requests.get(link)
dfMNList = pd.read_json(siteContent.text).transpose()
print('Finished getting masternode list')

print('Number of 5 years MN: '+str(dfMNList[dfMNList.timelock=='5 years'].shape[0]))
print('Number of 10 years MN: '+str(dfMNList[dfMNList.timelock=='10 years'].shape[0]))