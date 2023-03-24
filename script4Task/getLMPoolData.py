import requests
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI
import json
import time

scriptPath = __file__
path = scriptPath[:-28] + '/data/'
filepath = path + 'LMPoolData.csv'

requests.adapters.DEFAULT_RETRIES = 5

link='https://ocean.defichain.com/v0/mainnet/poolpairs?size=200'
siteContent = requests.get(link)
dfLMPoolDataNewAPI = json.loads(siteContent.text)

dfLMPoolData = pd.DataFrame(data = {'symbol': [item['symbol'] for item in dfLMPoolDataNewAPI['data'][:]],
                                        'idTokenA': [item['tokenA']['id'] for item in dfLMPoolDataNewAPI['data'][:]],
                                        'idTokenB': [item['tokenB']['id'] for item in dfLMPoolDataNewAPI['data'][:]],
                                        'reserveA': [item['tokenA']['reserve'] for item in dfLMPoolDataNewAPI['data'][:]],
                                        'reserveB': [item['tokenB']['reserve'] for item in dfLMPoolDataNewAPI['data'][:]],
                                        'commission': [item['commission'] for item in dfLMPoolDataNewAPI['data'][:]],
                                        'totalLiquidity': [item['totalLiquidity']['token'] for item in dfLMPoolDataNewAPI['data'][:]],
                                        'reserveA/reserveB': [item['priceRatio']['ab'] for item in dfLMPoolDataNewAPI['data'][:]],
                                        'reserveB/reserveA': [item['priceRatio']['ba'] for item in dfLMPoolDataNewAPI['data'][:]],
                                        'rewardLoanPct': [item['rewardPct'] for item in dfLMPoolDataNewAPI['data'][:]],
                                        '24hrTrading': [item['volume']['h24'] for item in dfLMPoolDataNewAPI['data'][:]],
                                        '30dTrading': [item['volume']['d30'] for item in dfLMPoolDataNewAPI['data'][:]],
                                        'APRblock': [item['apr']['reward'] if 'apr' in item.keys() else None for item in dfLMPoolDataNewAPI['data'][:] ],
                                        'APRcommission': [item['apr']['commission'] if 'apr' in item.keys() else None for item in dfLMPoolDataNewAPI['data'][:] ],
                                    })

# link='https://api.defichain.io/v1/listpoolpairs?start=0&limit=500&network=mainnet&including_start=false'
# siteContent = requests.get(link)
# dfLMPoolData = pd.read_json(siteContent.text).transpose()
# dfLMPoolData.drop(['name', 'status','tradeEnabled','ownerAddress','blockCommissionA',
#                    'blockCommissionB','rewardPct','creationTx','creationHeight'], axis=1,inplace=True)

# prices from Coingecko
dfLMPoolData['Time'] = pd.Timestamp.now()
dfLMPoolData['DFIPrices'] = None
cg = CoinGeckoAPI()

try:
    time.sleep(10)
    DFIData = cg.get_price(ids='defichain', vs_currencies=['btc','eth','usd'])

    time.sleep(10)
    DogeCoinData = cg.get_price(ids='dogecoin', vs_currencies=['usd'])
    dogeDFIPrice = DFIData['defichain']['usd']/DogeCoinData['dogecoin']['usd']

    time.sleep(10)
    LiteCoinData = cg.get_price(ids='litecoin', vs_currencies=['usd'])
    ltcDFIPrice = DFIData['defichain']['usd']/LiteCoinData['litecoin']['usd']

    time.sleep(10)
    BCHCoinData = cg.get_price(ids='bitcoin-cash', vs_currencies=['usd'])
    bchDFIPrice = DFIData['defichain']['usd']/BCHCoinData['bitcoin-cash']['usd']

    time.sleep(10)
    USDCCoinData = cg.get_price(ids='usd-coin', vs_currencies=['usd'])
    USDCDFIPrice = DFIData['defichain']['usd']/USDCCoinData['usd-coin']['usd']

    time.sleep(10)
    EUROCCoinData = cg.get_price(ids='euro-coin', vs_currencies=['usd'])
    EUROCDFIPrice = DFIData['defichain']['usd']/EUROCCoinData['euro-coin']['usd']

    dfLMPoolData.loc[0,'DFIPrices'] = DFIData['defichain']['eth']
    dfLMPoolData.loc[1,'DFIPrices'] = DFIData['defichain']['btc']
    dfLMPoolData.loc[2,'DFIPrices'] = DFIData['defichain']['usd']
    dfLMPoolData.loc[3,'DFIPrices'] = dogeDFIPrice
    dfLMPoolData.loc[4,'DFIPrices'] = ltcDFIPrice
    dfLMPoolData.loc[5,'DFIPrices'] = bchDFIPrice
    dfLMPoolData.loc[6,'DFIPrices'] = USDCDFIPrice
    dfLMPoolData.loc[70,'DFIPrices'] = EUROCDFIPrice

except:
    print('### Error Coingecko API')



# prices from Bittrex
try:
    link='https://api.bittrex.com/v3/markets/tickers'
    siteContent = requests.get(link)
    dfBittrexTicker = pd.read_json(siteContent.text)
    dfLMPoolData['DFIPricesBittrex'] = None
    dfLMPoolData.loc[1,'DFIPricesBittrex'] = dfBittrexTicker[dfBittrexTicker['symbol']=='DFI-BTC']['lastTradeRate'].values[0]
    dfLMPoolData.loc[2,'DFIPricesBittrex'] = dfBittrexTicker[dfBittrexTicker['symbol']=='DFI-USDT']['lastTradeRate'].values[0]
except:
    print('### Error Bittrex API')
    dfLMPoolData.loc[1, 'DFIPricesBittrex'] = np.nan
    dfLMPoolData.loc[2, 'DFIPricesBittrex'] = np.nan



####### add none when wrong dimension
dfLMPoolData['numberAddresses'] = None
# dfLMPoolData.loc[4, 'numberAddresses'] = ETHDFIaddresses
# dfLMPoolData.loc[5, 'numberAddresses'] = BTCDFIaddresses
# dfLMPoolData.loc[6, 'numberAddresses'] = USDTDFIaddresses
# dfLMPoolData.loc[8, 'numberAddresses'] = DOGEDFIaddresses
# dfLMPoolData.loc[10, 'numberAddresses'] = LTCDFIaddresses
# dfLMPoolData.loc[12, 'numberAddresses'] = BCHDFIaddresses
# dfLMPoolData.loc[14, 'numberAddresses'] = USDCDFIaddresses
# pd.read_csv(filePath, header=0,
#                                         usecols=["DFIPrices", "DFIPricesBittrex", "Time", "idTokenA", "idTokenB", 'numberAddresses', 'reserveA', 'reserveA/reserveB',
#                                                'reserveB', 'reserveB/reserveA', 'symbol', 'totalLiquidity', '24hrTrading', '30dTrading'],
#                                         dtype={"DFIPrices": float, "DFIPricesBittrex": float, "Time": "string",
#                                                "idTokenA": int, "idTokenB": int, 'numberAddresses': float, 'reserveA': float, 'reserveA/reserveB': float,
#                                                'reserveB': float, 'reserveB/reserveA':float, 'symbol': "string", 'totalLiquidity': float, '24hrTrading': float, '30dTrading': float})
dfOldLMPoolData = pd.read_csv(filepath, index_col=0)
dfLMPoolData = dfOldLMPoolData.append(dfLMPoolData, sort=False)
dfLMPoolData.reset_index(inplace=True, drop=True)

dfLMPoolData.to_csv(filepath)
