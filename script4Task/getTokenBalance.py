import requests
import pandas as pd
import ast
import json


# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-30] + '/data/'
filepath = path + 'TokenData.csv'


# minted token on defichain
link='https://api.defichain.io/v1/listtokens?network=mainnet&start=0&including_start=true'
siteContent = requests.get(link)
dfTokenData = pd.read_json(siteContent.text).transpose()
dfTokenData = dfTokenData[['symbol','minted','creationTx','creationHeight','collateralAddress']].iloc[[1,2,3,7,9,11,13]]
dfTokenData['Time'] = pd.Timestamp.now()
    
# burned token on defichain
link='https://api.defichain.io/v1/getaccount?start=0&limit=500&network=mainnet&including_start=true&owner=8defichainBurnAddressXXXXXXXdRQkSm'
siteContent = requests.get(link)
dfTempData = pd.read_json(siteContent.text)
dfBurnedTokenData = pd.DataFrame(dfTempData[0].str.split('@',1).tolist(),columns = ['amount','coin'])
dfBurnedTokenData.set_index('coin',inplace=True)

dfTokenData['Burned'] = None
if 'BTC' in dfBurnedTokenData.index:
    dfTokenData.loc[2,'Burned']=dfBurnedTokenData.loc['BTC','amount']
if 'ETH' in dfBurnedTokenData.index:
    dfTokenData.loc[1,'Burned']=dfBurnedTokenData.loc['ETH','amount']
if 'USDT' in dfBurnedTokenData.index:
    dfTokenData.loc[3,'Burned']=dfBurnedTokenData.loc['USDT','amount']
if 'DOGE' in dfBurnedTokenData.index:
    dfTokenData.loc[7,'Burned']=dfBurnedTokenData.loc['DOGE','amount']
if 'LTC' in dfBurnedTokenData.index:
    dfTokenData.loc[9,'Burned']=dfBurnedTokenData.loc['LTC','amount']
if 'BCH' in dfBurnedTokenData.index:
    dfTokenData.loc[11,'Burned']=dfBurnedTokenData.loc['BCH','amount']
if 'USDC' in dfBurnedTokenData.index:
    dfTokenData.loc[13,'Burned']=dfBurnedTokenData.loc['USDC','amount']

# coins on collateral addresses
#BTC
link='https://blockchain.info/q/addressbalance/38pZuWUti3vSQuvuFYs8Lwbyje8cmaGhrT'
siteContent = requests.get(link)
BTCamount = float(siteContent.text)*1e-8

#ETH
link='https://api.etherscan.io/api?module=account&action=balance&address=0x94fa70d079d76279e1815ce403e9b985bccc82ac&tag=latest&apikey=WZ8T48S9KDR1YWI8RJKT9PBRGB8GCU96AE'
siteContent = requests.get(link)
apiContentAsDict=ast.literal_eval(siteContent.text)
ETHamount = float(apiContentAsDict['result'])*1e-18

#USDT
link='https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xdac17f958d2ee523a2206206994597c13d831ec7&address=0x94fa70d079d76279e1815ce403e9b985bccc82ac&tag=latest&apikey=WZ8T48S9KDR1YWI8RJKT9PBRGB8GCU96AE'
siteContent = requests.get(link)
apiContentAsDict=ast.literal_eval(siteContent.text)
USDTamount = float(apiContentAsDict['result'])*1e-6

#DOGE
link='https://sochain.com/api/v2/get_address_balance/DOGE/D7jrXDgPYck8jL9eYvRrc7Ze8n2e2Loyba'
siteContent = requests.get(link)
tempData = json.loads(siteContent.text)
DOGEamount = tempData['data']['confirmed_balance']

#LTC
link='https://sochain.com/api/v2/get_address_balance/LTC/MLYQxJfnUfVqRwfYXjDJfmLbyA77hqzSXE'
siteContent = requests.get(link)
tempData = json.loads(siteContent.text)
LTCamount = tempData['data']['confirmed_balance']

#BCH
link='https://rest.bitcoin.com/v2/address/details/bitcoincash:pp8h5g6dfqcknsfvah6gycutem32mcsqjc9u5syw86'
siteContent = requests.get(link)
tempData = json.loads(siteContent.text)
BCHamount = tempData['balance']

#USDC
link='https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&address=0x94fa70d079d76279e1815ce403e9b985bccc82ac&tag=latest&apikey=WZ8T48S9KDR1YWI8RJKT9PBRGB8GCU96AE'
siteContent = requests.get(link)
apiContentAsDict=ast.literal_eval(siteContent.text)
USDCamount = float(apiContentAsDict['result'])*1e-6


dfTokenData['Collateral'] =[ETHamount,BTCamount, USDTamount,DOGEamount,LTCamount,BCHamount,USDCamount]
    
dfOldTokenData = pd.read_csv(filepath,index_col=0)
dfTokenData = dfOldTokenData.append(dfTokenData, sort=False)
dfTokenData.reset_index(inplace=True, drop=True)
    
dfTokenData.to_csv(filepath)
