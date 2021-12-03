import requests
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI
import time
from datetime import datetime
import json

scriptPath = __file__
path = scriptPath[:-35] + '/data/'
filepath = path + 'LMPoolData_ShortTerm.csv'

while True: 
    start_time = pd.Timestamp.now()
    print('Get data at '+str(start_time)+' ...')
    requests.adapters.DEFAULT_RETRIES = 5

    link = 'https://ocean.defichain.com/v0/mainnet/poolpairs?size=200'
    siteContent = requests.get(link)
    dfLMPoolDataNewAPI = json.loads(siteContent.text)

    dfLMPoolData = pd.DataFrame(data={'symbol': [item['symbol'] for item in dfLMPoolDataNewAPI['data'][:]],
                                          'idTokenA': [item['tokenA']['id'] for item in dfLMPoolDataNewAPI['data'][:]],
                                          'idTokenB': [item['tokenB']['id'] for item in dfLMPoolDataNewAPI['data'][:]],
                                          'reserveA': [item['tokenA']['reserve'] for item in dfLMPoolDataNewAPI['data'][:]],
                                          'reserveB': [item['tokenB']['reserve'] for item in dfLMPoolDataNewAPI['data'][:]],
                                          'commission': [item['commission'] for item in dfLMPoolDataNewAPI['data'][:]],
                                          'totalLiquidity': [item['totalLiquidity']['token'] for item in dfLMPoolDataNewAPI['data'][:]],
                                          'reserveA/reserveB': [item['priceRatio']['ab'] for item in dfLMPoolDataNewAPI['data'][:]],
                                          'reserveB/reserveA': [item['priceRatio']['ba'] for item in dfLMPoolDataNewAPI['data'][:]],
                                          'rewardLoanPct': [item['rewardPct'] for item in dfLMPoolDataNewAPI['data'][:]]})

    cg = CoinGeckoAPI()
    DFIData = cg.get_price(ids='defichain', vs_currencies=['btc','eth','usd'])
    
    DogeCoinData = cg.get_price(ids='dogecoin', vs_currencies=['usd'])
    dogeDFIPrice = DFIData['defichain']['usd']/DogeCoinData['dogecoin']['usd']
    LiteCoinData = cg.get_price(ids='litecoin', vs_currencies=['usd'])
    ltcDFIPrice = DFIData['defichain']['usd']/LiteCoinData['litecoin']['usd']
    BCHCoinData = cg.get_price(ids='bitcoin-cash', vs_currencies=['usd'])
    bchDFIPrice = DFIData['defichain']['usd']/BCHCoinData['bitcoin-cash']['usd']
    USDCCoinData = cg.get_price(ids='usd-coin', vs_currencies=['usd'])
    USDCDFIPrice = DFIData['defichain']['usd'] / USDCCoinData['usd-coin']['usd']

    dfLMPoolData['DFIPrices'] = None
    dfLMPoolData.loc[0, 'DFIPrices'] = DFIData['defichain']['eth']
    dfLMPoolData.loc[1, 'DFIPrices'] = DFIData['defichain']['btc']
    dfLMPoolData.loc[2, 'DFIPrices'] = DFIData['defichain']['usd']
    dfLMPoolData.loc[3, 'DFIPrices'] = dogeDFIPrice
    dfLMPoolData.loc[4, 'DFIPrices'] = ltcDFIPrice
    dfLMPoolData.loc[5, 'DFIPrices'] = bchDFIPrice
    dfLMPoolData.loc[6, 'DFIPrices'] = USDCDFIPrice
    dfLMPoolData['Time'] = pd.Timestamp.now()

    # prices from Bittrex
    link = 'https://api.bittrex.com/v3/markets/tickers'
    siteContent = requests.get(link)
    dfBittrexTicker = pd.read_json(siteContent.text)
    dfLMPoolData['DFIPricesBittrex'] = None
    dfLMPoolData.loc[1, 'DFIPricesBittrex'] = dfBittrexTicker[dfBittrexTicker['symbol'] == 'DFI-BTC']['lastTradeRate'].values[0]
    dfLMPoolData.loc[2, 'DFIPricesBittrex'] = dfBittrexTicker[dfBittrexTicker['symbol'] == 'DFI-USDT']['lastTradeRate'].values[0]

        
    dfOldLMPoolData = pd.read_csv(filepath,index_col=0)
    dfLMPoolData = dfOldLMPoolData.append(dfLMPoolData, sort=False)
    dfLMPoolData = dfLMPoolData[-540:]
    dfLMPoolData.reset_index(inplace=True, drop=True)
        
    dfLMPoolData.to_csv(filepath)
    
    # wait time before run again
    nowTimestamp = datetime.now()
    waitTime = 60-nowTimestamp.second
    print('...finished. Timestamp: '+str(datetime.now())+'   wait-time:'+str(waitTime))
    time.sleep(waitTime)