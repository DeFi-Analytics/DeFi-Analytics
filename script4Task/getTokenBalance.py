import requests
import pandas as pd
import numpy as np
import ast
import json


# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-30] + '/data/'
filepath = path + 'TokenData.csv'


# minted token on defichain
print('Get tokens on defichain ...')


link='https://ocean.defichain.com/v0/mainnet/tokens'
siteContent = requests.get(link)
tempData = json.loads(siteContent.text)

dfTokenData = pd.DataFrame(columns=['symbol','minted','creationTx','creationHeight','collateralAddress'])
idTokens = {1, 2, 3, 7, 9, 11, 13}
for id in idTokens:
    dfTokenData.loc[id, 'symbol'] = tempData['data'][id]['symbol']
    dfTokenData.loc[id, 'minted'] = tempData['data'][id]['minted']
    dfTokenData.loc[id, 'creationTx'] = tempData['data'][id]['creation']['tx']
    dfTokenData.loc[id, 'creationHeight'] = tempData['data'][id]['creation']['height']
    dfTokenData.loc[id, 'collateralAddress'] = tempData['data'][id]['collateralAddress']

#EUROC token is on the 2nd page
link='https://ocean.defichain.com/v0/mainnet/tokens?size=200&next=199'
siteContent = requests.get(link)
tempData = json.loads(siteContent.text)
dfTokenData.loc[216, 'symbol'] = tempData['data'][16]['symbol']
dfTokenData.loc[216, 'minted'] = tempData['data'][16]['minted']
dfTokenData.loc[216, 'creationTx'] = tempData['data'][16]['creation']['tx']
dfTokenData.loc[216, 'creationHeight'] = tempData['data'][16]['creation']['height']
dfTokenData.loc[216, 'collateralAddress'] = tempData['data'][16]['collateralAddress']

dfTokenData['Time'] = pd.Timestamp.now()

# burned token on defichain
print('Get burned tokens on defichain ...')
link='https://ocean.defichain.com/v0/mainnet/address/8defichainBurnAddressXXXXXXXdRQkSm/tokens'
siteContent = requests.get(link)
tempData = json.loads(siteContent.text)
for item in tempData['data']:
    if int(item['id']) in idTokens:
        dfTokenData.loc[int(item['id']), 'Burned'] = item['amount']




print('Check collaterals ...')
# coins on collateral addresses
#BTC
print('... BTC ...')
try:
    link='https://blockchain.info/q/addressbalance/3GcSHxkKY8ADMWRam51T1WYxYSb2vH62VL'
    siteContent = requests.get(link)
    BTCamount = float(siteContent.text)*1e-8
except:
    BTCamount = np.nan
    print('### Error in BTC API')


#ETH
print('... ETH ...')
try:
    link='https://api.etherscan.io/api?module=account&action=balance&address=0xC889Faf456439Fb932B9Ce3d4F43D8078177fD29&tag=latest&apikey=WZ8T48S9KDR1YWI8RJKT9PBRGB8GCU96AE'
    siteContent = requests.get(link)
    apiContentAsDict=ast.literal_eval(siteContent.text)
    ETHamount = float(apiContentAsDict['result'])*1e-18
except:
    ETHamount = np.nan
    print('### Error in ETH API')


#USDT
print('... USDT ...')
try:
    link='https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xdac17f958d2ee523a2206206994597c13d831ec7&address=0xC889Faf456439Fb932B9Ce3d4F43D8078177fD29&tag=latest&apikey=WZ8T48S9KDR1YWI8RJKT9PBRGB8GCU96AE'
    siteContent = requests.get(link)
    apiContentAsDict=ast.literal_eval(siteContent.text)
    USDTamount = float(apiContentAsDict['result'])*1e-6
except:
    USDTamount = np.nan
    print('### Error in USDT API')


#DOGE
print('... DOGE ...')
try:
    link='https://dogechain.info/api/v1/address/balance/9uv4fqPjSYNVNvqzbuGUMACBw67qQcLTxg'
    siteContent = requests.get(link)
    tempData = json.loads(siteContent.text)
    DOGEamount = float(tempData['balance'])
except:
    DOGEamount = np.nan
    print('### Error in DOGE API')


#LTC
print('... LTC ...')
try:
    link ='https://sochain.com/api/v2/get_address_balance/LTC/MLYQxJfnUfVqRwfYXjDJfmLbyA77hqzSXE'
    siteContent = requests.get(link)
    tempData = json.loads(siteContent.text)
    LTCamount = tempData['data']['confirmed_balance']
except:
    LTCamount = np.nan
    print('### Error in LTC API')


#BCH
print('... BCH ...')
try:
    link='https://api.fullstack.cash/v5/electrumx/balance/pp8h5g6dfqcknsfvah6gycutem32mcsqjc9u5syw86'
    siteContent = requests.get(link)
    tempData = json.loads(siteContent.text)
    BCHamount = tempData['balance']['confirmed']*1e-8
except:
    BCHamount = np.nan
    print('### Error in BCH API')


#USDC
print('... USDC ...')
try:
    link='https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&address=0xC889Faf456439Fb932B9Ce3d4F43D8078177fD29&tag=latest&apikey=WZ8T48S9KDR1YWI8RJKT9PBRGB8GCU96AE'
    siteContent = requests.get(link)
    apiContentAsDict=ast.literal_eval(siteContent.text)
    USDCamount = float(apiContentAsDict['result'])*1e-6
except:
    USDCamount = np.nan
    print('### Error in USDC API')


#EUROC
print('... EUROC ...')
try:
    link='https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x1aBaEA1f7C830bD89Acc67eC4af516284b1bC33c&address=0xC889Faf456439Fb932B9Ce3d4F43D8078177fD29&tag=latest&apikey=WZ8T48S9KDR1YWI8RJKT9PBRGB8GCU96AE'
    siteContent = requests.get(link)
    apiContentAsDict=ast.literal_eval(siteContent.text)
    EUROCamount = float(apiContentAsDict['result'])*1e-6
except:
    EUROCamount = np.nan
    print('### Error in EUROC API')

dfTokenData['Collateral'] =[ETHamount,BTCamount, USDTamount,DOGEamount,LTCamount,BCHamount,USDCamount, EUROCamount]
    
dfOldTokenData = pd.read_csv(filepath,index_col=0)
dfTokenData = dfOldTokenData.append(dfTokenData, sort=False)
dfTokenData.reset_index(inplace=True, drop=True)
    
dfTokenData.to_csv(filepath)
