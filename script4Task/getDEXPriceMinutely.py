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
    try:
        DFIData = cg.get_price(ids='defichain', vs_currencies=['btc','eth','usd'])
        DFIPrice_ETH = DFIData['defichain']['eth']
        DFIPrice_BTC = DFIData['defichain']['btc']
        DFIPrice_USD = DFIData['defichain']['usd']
    except:
        print('###  Error in Coingecko-API')
        link = 'https://api.coinpaprika.com/v1/tickers/dfi-defi-chain?quotes=BTC,ETH,USD'
        siteContent = requests.get(link)
        tempData = json.loads(siteContent.text)
        DFIPrice_ETH = tempData['quotes']['ETH']['price']
        DFIPrice_BTC = tempData['quotes']['BTC']['price']
        DFIPrice_USD = tempData['quotes']['USD']['price']

    try:
        DogeCoinData = cg.get_price(ids='dogecoin', vs_currencies=['usd'])
        DogePrice_USD = DogeCoinData['dogecoin']['usd']
    except:
        print('###  Error in Coingecko-API')
        link = 'https://api.coinpaprika.com/v1/tickers/doge-dogecoin?quotes=USD'
        siteContent = requests.get(link)
        tempData = json.loads(siteContent.text)
        DogePrice_USD = tempData['quotes']['USD']['price']
    dogeDFIPrice = DFIPrice_USD/DogePrice_USD

    try:
        LiteCoinData = cg.get_price(ids='litecoin', vs_currencies=['usd'])
        LTCPrice_USD = LiteCoinData['litecoin']['usd']
    except:
        print('###  Error in Coingecko-API')
        link = 'https://api.coinpaprika.com/v1/tickers/ltc-litecoin?quotes=USD'
        siteContent = requests.get(link)
        tempData = json.loads(siteContent.text)
        LTCPrice_USD = tempData['quotes']['USD']['price']
    ltcDFIPrice = DFIPrice_USD/LTCPrice_USD

    try:
        BCHCoinData = cg.get_price(ids='bitcoin-cash', vs_currencies=['usd'])
        BCHPrice_USD = BCHCoinData['bitcoin-cash']['usd']
    except:
        print('###  Error in Coingecko-API')
        link = 'https://api.coinpaprika.com/v1/tickers/bch-bitcoin-cash?quotes=USD'
        siteContent = requests.get(link)
        tempData = json.loads(siteContent.text)
        BCHPrice_USD = tempData['quotes']['USD']['price']
    bchDFIPrice = DFIPrice_USD/BCHPrice_USD

    try:
        USDCCoinData = cg.get_price(ids='usd-coin', vs_currencies=['usd'])
        USDCPrice_USD = USDCCoinData['usd-coin']['usd']
    except:
        print('###  Error in Coingecko-API')
        link = 'https://api.coinpaprika.com/v1/tickers/usdce-usd-coine?quotes=USD'
        siteContent = requests.get(link)
        tempData = json.loads(siteContent.text)
        USDCPrice_USD = tempData['quotes']['USD']['price']
    USDCDFIPrice = DFIPrice_USD / USDCPrice_USD

    dfLMPoolData['DFIPrices'] = None
    dfLMPoolData.loc[0, 'DFIPrices'] = DFIPrice_ETH
    dfLMPoolData.loc[1, 'DFIPrices'] = DFIPrice_BTC
    dfLMPoolData.loc[2, 'DFIPrices'] = DFIPrice_USD
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
    dfLMPoolData = dfLMPoolData[-6570:]
    dfLMPoolData.reset_index(inplace=True, drop=True)
        
    dfLMPoolData.to_csv(filepath)
    
    # wait time before run again
    nowTimestamp = datetime.now()
    waitTime = 60-nowTimestamp.second
    print('...finished. Timestamp: '+str(datetime.now())+'   wait-time:'+str(waitTime))
    time.sleep(waitTime)