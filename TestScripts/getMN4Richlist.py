import glob

import numpy as np
import pandas as pd
import requests

from datetime import datetime


scriptPath = __file__
path = scriptPath[:-30] + '/data/'
pathRichlist = scriptPath[:-30] + '/data/Richlist/'
filepath = pathRichlist+'2021-05-17_01-01-10_Richlist.csv'

rawRichlist = pd.read_csv(filepath)

link = 'http://api.mydefichain.com/v1/listmasternodes/?state=ENABLED'
siteContent = requests.get(link)
dfMNList = pd.read_json(siteContent.text).transpose()
rawRichlist['mnAddressAPI'] = rawRichlist['address'].isin(dfMNList.ownerAuthAddress)

rawRichlist.to_csv(filepath, index=False)