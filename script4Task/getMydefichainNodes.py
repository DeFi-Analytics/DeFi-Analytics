import glob

import numpy as np
import pandas as pd

from datetime import datetime


scriptPath = __file__
path = scriptPath[:-35] + '/data/'
filepath = path+'extractedDFIdata.csv'
filepathMydefichain = path+'mydefichainOperatornodes.xlsx'

dfDFIData = pd.read_csv(filepath)
dfMydefichainData = pd.read_excel(filepathMydefichain, sheet_name='listmasternodes')
dfMydefichainData = dfMydefichainData[dfMydefichainData['Spalte1']=='mydefichain']

pathRichlist = scriptPath[:-35] + '/data/Richlist/'
listCSVFiles = glob.glob(pathRichlist+"*_01-*.csv")
foundRichlistFiles = [richlistDate for richlistDate in listCSVFiles]

dfRichlistFiles = pd.DataFrame({'fileList': foundRichlistFiles})
dfRichlistFiles['Date'] = dfRichlistFiles.fileList.str[-32:-22]

for index, row in dfRichlistFiles[dfRichlistFiles.Date >'2021-03-08'].iterrows():
    conditionDate = dfDFIData['date'] == row.Date
    print('File ' + row.fileList + '...')
    rawRichlist = pd.read_csv(row.fileList)
    rawRichlist['mnAddressMyDefichain'] = rawRichlist['address'].isin(dfMydefichainData['Value.ownerAuthAddress'])

    dfDFIData.loc[conditionDate, 'nbMydefichainId'] = rawRichlist[rawRichlist.mnAddressMyDefichain & rawRichlist.mnAddressAPI].mnAddressMyDefichain.sum()
    dfDFIData.loc[conditionDate, 'mnMydefichainDFI'] = rawRichlist[rawRichlist.mnAddressMyDefichain & rawRichlist.mnAddressAPI].balance.sum()


dfDFIData = dfDFIData.sort_values(by=['date'])
dfDFIData.to_csv(filepath, index = False)