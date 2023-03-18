import requests
import ast

import pandas as pd

scriptPath = __file__
path = scriptPath[:-26] + '/data/'
filepathTxList = path +'dUSDBornBotTx.csv'
filepathBurnAmount = path +'dUSDBornBotAmounts.csv'

######### get all swaps #########

dfBurnBotOldTxList = pd.read_csv(filepathTxList, index_col=0)
dfBurnBotOldTxList.index = pd.to_datetime(dfBurnBotOldTxList.index)

# get the first 200 entries of burn bot listaccounthistory
link = 'https://ocean.defichain.com/v0/mainnet/address/df1qa6qjmtuh8fyzqyjjsrg567surxu43rx3na7yah/history?size=20'
siteContent = requests.get(link)
apiContentAsDict = ast.literal_eval(siteContent.text)
dfBurnBotTxList = pd.DataFrame(apiContentAsDict['data'])

dfBurnBotTxList = dfBurnBotTxList[~dfBurnBotTxList['txid'].isin(dfBurnBotOldTxList['txid'])]

if dfBurnBotTxList.shape[0]>0:
    # get the rest of listaccounthistory
    while ('page' in apiContentAsDict) & (dfBurnBotTxList.shape[0].__mod__(20) == 0):
        link = 'https://ocean.defichain.com/v0/mainnet/address/df1qa6qjmtuh8fyzqyjjsrg567surxu43rx3na7yah/history?size=200&next='+apiContentAsDict['page']['next']
        siteContent = requests.get(link)
        apiContentAsDict = ast.literal_eval(siteContent.text)
        dfBurnBotTxList = dfBurnBotTxList.append(pd.DataFrame(apiContentAsDict['data']))

    dfBurnBotTxList.reset_index(inplace=True, drop=True)
    dfBurnBotTxList = pd.concat([dfBurnBotTxList,dfBurnBotTxList['block'].apply(pd.Series)], axis=1)
    dfBurnBotTxList.drop(columns=['owner', 'txn', 'block','hash'],inplace=True)
    dfBurnBotTxList = dfBurnBotTxList[dfBurnBotTxList['type']=='PoolSwap']

    # screen burn address for corresponding dUSD amount
    # get the first 200 entries of burn bot listaccounthistory
    link = 'https://ocean.defichain.com/v0/mainnet/address/8defichainBurnAddressXXXXXXXdRQkSm/history?size=200'
    siteContent = requests.get(link)
    apiContentAsDict = ast.literal_eval(siteContent.text)
    dfBurnAddressTxList = pd.DataFrame(apiContentAsDict['data'])
    dfBurnBotTxList = dfBurnBotTxList.merge(dfBurnAddressTxList[['txid','amounts']], left_on='txid', right_on='txid', how='left')
    dfBurnBotTxList['amounts_y'] = pd.to_numeric(dfBurnBotTxList['amounts_y'].astype(str).str[2:-7]).fillna(0)

    # get the rest of listaccounthistory
    while ('page' in apiContentAsDict) & dfBurnBotTxList['amounts_y'].eq(0).any():
        link = 'https://ocean.defichain.com/v0/mainnet/address/8defichainBurnAddressXXXXXXXdRQkSm/history?size=200&next='+apiContentAsDict['page']['next']
        siteContent = requests.get(link)
        apiContentAsDict = ast.literal_eval(siteContent.text)
        dfBurnAddressTxList = pd.DataFrame(apiContentAsDict['data'])
        dfBurnBotTxList = dfBurnBotTxList.merge(dfBurnAddressTxList[['txid', 'amounts']], left_on='txid', right_on='txid', how='left')
        dfBurnBotTxList['amounts'] = pd.to_numeric(dfBurnBotTxList['amounts'].astype(str).str[2:-7])
        dfBurnBotTxList['amounts_y'] = dfBurnBotTxList['amounts_y'].fillna(0)+dfBurnBotTxList['amounts'].fillna(0)
        dfBurnBotTxList.drop(columns=['amounts'], inplace=True)

    dfBurnBotTxList['amounts_x'] = pd.to_numeric(dfBurnBotTxList['amounts_x'].astype(str).str[2:-6])
    dfBurnBotTxList.set_index(pd.to_datetime(dfBurnBotTxList['time'],utc=True,unit='s'),inplace=True)
    dfBurnBotTxList.rename(columns={"time": "timeRaw"}, inplace=True)
dfBurnBotTxList = dfBurnBotOldTxList.append(dfBurnBotTxList)
dfBurnBotTxList.sort_values(by=['height'], ascending=False, inplace=True)
dfBurnBotTxList.to_csv(filepathTxList)

######### extract burned amount on hourly base #########
dfBurnedAmount = pd.DataFrame()
dfBurnedAmount['DUSDBurnBot_DFIAmount'] = dfBurnBotTxList['amounts_x'].groupby(pd.Grouper(freq='H')).sum()
dfBurnedAmount['DUSDBurnBot_DUSDAmount'] = dfBurnBotTxList['amounts_y'].groupby(pd.Grouper(freq='H')).sum()
dfBurnedAmount['DUSDBurnBot_SumDUSDAmount'] = dfBurnedAmount['DUSDBurnBot_DUSDAmount'].cumsum()
dfBurnedAmount.index = dfBurnedAmount.index+np.timedelta64(1, 'h')
dfBurnedAmount.to_csv(filepathBurnAmount)

