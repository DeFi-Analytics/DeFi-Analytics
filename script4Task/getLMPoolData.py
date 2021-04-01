import os
import requests
import pandas as pd
from pycoingecko import CoinGeckoAPI


scriptPath = os.path.abspath(os.getcwd())
if scriptPath[0] == 'H':
    scriptPath=scriptPath[:-14]
path        = scriptPath + '/data/'
filepath    = path + 'LMPoolData.csv'

requests.adapters.DEFAULT_RETRIES = 5

link='https://api.defichain.io/v1/listpoolpairs?start=0&limit=500&network=mainnet&including_start=false'
siteContent = requests.get(link)
dfLMPoolData = pd.read_json(siteContent.text).transpose()
dfLMPoolData.drop(['name', 'status','tradeEnabled','ownerAddress','blockCommissionA',
                   'blockCommissionB','rewardPct','creationTx','creationHeight'], axis=1,inplace=True)

# prices from Coingecko
cg = CoinGeckoAPI()
DFIData = cg.get_price(ids='defichain', vs_currencies=['btc','eth','usd'])
    
DogeCoinData = cg.get_price(ids='dogecoin', vs_currencies=['usd'])
dogeDFIPrice = DFIData['defichain']['usd']/DogeCoinData['dogecoin']['usd']
LiteCoinData = cg.get_price(ids='litecoin', vs_currencies=['usd'])
ltcDFIPrice = DFIData['defichain']['usd']/LiteCoinData['litecoin']['usd']
BCHCoinData = cg.get_price(ids='bitcoin-cash', vs_currencies=['usd'])
bchDFIPrice = DFIData['defichain']['usd']/BCHCoinData['bitcoin-cash']['usd']    


dfLMPoolData['DFIPrices'] = None
dfLMPoolData.loc[4,'DFIPrices'] = DFIData['defichain']['eth']
dfLMPoolData.loc[5,'DFIPrices'] = DFIData['defichain']['btc']
dfLMPoolData.loc[6,'DFIPrices'] = DFIData['defichain']['usd']
dfLMPoolData.loc[8,'DFIPrices'] = dogeDFIPrice
dfLMPoolData.loc[10,'DFIPrices'] = ltcDFIPrice
dfLMPoolData.loc[12,'DFIPrices'] = bchDFIPrice
dfLMPoolData['Time'] = pd.Timestamp.now()

# prices from Bittrex
link='https://api.bittrex.com/v3/markets/tickers'
siteContent = requests.get(link)    
dfBittrexTicker = pd.read_json(siteContent.text)  
dfLMPoolData['DFIPricesBittrex'] = None
dfLMPoolData.loc[5,'DFIPricesBittrex'] = dfBittrexTicker[dfBittrexTicker['symbol']=='DFI-BTC']['lastTradeRate'].values[0]
dfLMPoolData.loc[6,'DFIPricesBittrex'] = dfBittrexTicker[dfBittrexTicker['symbol']=='DFI-USDT']['lastTradeRate'].values[0]

# Amount addresses with liquidity token
# BTC/DFI-Token on DefiChain
try:
    link = "https://api.defichain.io/v1/gettokenrichlist?id=5&network=mainnet"
    siteContent = requests.get(link)
    temp = pd.read_json(siteContent.text)
    BTCDFIaddresses = temp['balance'].count()
except:
    print('Error with API of BTC/DFI Richlist')
    
# ETH/DFI-Token on DefiChain
try:
    link = "https://api.defichain.io/v1/gettokenrichlist?id=4&network=mainnet"
    siteContent = requests.get(link)
    temp = pd.read_json(siteContent.text)
    ETHDFIaddresses = temp['balance'].count()
except:
    print('Error with API of ETH/DFI Richlist')
    
# USDT/DFI-Token on DefiChain
try:
    link = "https://api.defichain.io/v1/gettokenrichlist?id=6&network=mainnet"
    siteContent = requests.get(link)
    temp = pd.read_json(siteContent.text)
    USDTDFIaddresses = temp['balance'].count()
except:
    print('Error with API of USDT/DFI Richlist')
    
# DOGE/DFI-Token on DefiChain
try:    
    link = "https://api.defichain.io/v1/gettokenrichlist?id=8&network=mainnet"
    siteContent = requests.get(link)
    temp = pd.read_json(siteContent.text)
    DOGEDFIaddresses = temp['balance'].count()
except:
    print('Error with API of DOGE/DFI Richlist')
    
# LTC/DFI-Token on DefiChain
try:
    link = "https://api.defichain.io/v1/gettokenrichlist?id=10&network=mainnet"
    siteContent = requests.get(link)
    temp = pd.read_json(siteContent.text)
    LTCDFIaddresses = temp['balance'].count()
except:
    print('Error with API of LTC/DFI Richlist')

# BCH/DFI-Token on DefiChain
try:
    link = "https://api.defichain.io/v1/gettokenrichlist?id=12&network=mainnet"
    siteContent = requests.get(link)
    temp = pd.read_json(siteContent.text)
    BCHDFIaddresses = temp['balance'].count()
except:
    print('Error with API of BCH/DFI Richlist')
    
####### add none when wrong dimension
dfLMPoolData['numberAddresses'] = None
dfLMPoolData.loc[4,'numberAddresses'] = ETHDFIaddresses
dfLMPoolData.loc[5,'numberAddresses'] = BTCDFIaddresses
dfLMPoolData.loc[6,'numberAddresses'] = USDTDFIaddresses
dfLMPoolData.loc[8,'numberAddresses'] = DOGEDFIaddresses
dfLMPoolData.loc[10,'numberAddresses'] = LTCDFIaddresses
dfLMPoolData.loc[12,'numberAddresses'] = BCHDFIaddresses
  
    
dfOldLMPoolData = pd.read_csv(filepath,index_col=0)
dfLMPoolData = dfOldLMPoolData.append(dfLMPoolData)
dfLMPoolData.reset_index(inplace=True, drop=True)
    
dfLMPoolData.to_csv(filepath)
