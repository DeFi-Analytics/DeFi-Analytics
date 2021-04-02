import requests
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI
import time

scriptPath = __file__
path = scriptPath[:-35] + '/data/'
filepath = path + 'LMPoolData_ShortTerm.csv'

while True: 
    print(pd.Timestamp.now())     
    start_time = time.time()
    requests.adapters.DEFAULT_RETRIES = 5
    link='https://api.defichain.io/v1/listpoolpairs?start=0&limit=500&network=mainnet&including_start=false'
    siteContent = requests.get(link)
    
#    s = requests.Session()
#    s.mount(link, HTTPAdapter(max_retries=5))


    dfLMPoolData = pd.read_json(siteContent.text).transpose()
    dfLMPoolData.drop(['name', 'status','tradeEnabled','ownerAddress','blockCommissionA',
                       'blockCommissionB','rewardPct','creationTx','creationHeight'], axis=1,inplace=True)
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
        
    dfOldLMPoolData = pd.read_csv(filepath,index_col=0)
    dfLMPoolData = dfOldLMPoolData.append(dfLMPoolData, sort=False)
    dfLMPoolData = dfLMPoolData[-540:]
    dfLMPoolData.reset_index(inplace=True, drop=True)
        
    dfLMPoolData.to_csv(filepath)
    
    # wait time before run again
    waitTime = 60-(time.time() - start_time)       
    waitTime = np.maximum(waitTime, 0)
    time.sleep(waitTime)