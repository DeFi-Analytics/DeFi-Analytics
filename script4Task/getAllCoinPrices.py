from datetime import datetime
from pycoingecko import CoinGeckoAPI

import pandas as pd


today = datetime.today()
startDate = datetime.timestamp(datetime(2019, 4, 1))
endDate = datetime.timestamp(today)


cg = CoinGeckoAPI()
try:

    # Bitcoin-price
    coinInfosCG = cg.get_coin_market_chart_range_by_id(id='bitcoin',vs_currency='eur',from_timestamp=startDate,to_timestamp=endDate)
    coinInfosCGUSD = cg.get_coin_market_chart_range_by_id(id='bitcoin',vs_currency='usd',from_timestamp=startDate,to_timestamp=endDate)
    temp = pd.DataFrame(coinInfosCG['prices'])
    temp['BTCPriceUSD'] = pd.DataFrame(coinInfosCGUSD['prices'])[1]
    temp = temp.rename(columns={0:'Date',1:'BTCPriceEUR',2:'BTCPriceUSD'})
    temp['Date'] = pd.to_datetime(temp['Date'], unit='ms').dt.date
    temp.set_index('Date', inplace=True)
    coinPricesDF = temp
                
    # Ethereum-price
    coinInfosCGEUR = cg.get_coin_market_chart_range_by_id(id='ethereum',vs_currency='eur',from_timestamp=startDate,to_timestamp=endDate)
    coinInfosCGUSD = cg.get_coin_market_chart_range_by_id(id='ethereum',vs_currency='usd',from_timestamp=startDate,to_timestamp=endDate)
    temp = pd.DataFrame(coinInfosCGEUR['prices'])
    temp['ETHPriceUSD'] = pd.DataFrame(coinInfosCGUSD['prices'])[1]
    temp = temp.rename(columns={0:'Date',1:'ETHPriceEUR',2:'ETHPriceUSD'})
    temp['Date'] = pd.to_datetime(temp['Date'], unit='ms').dt.date
    temp.set_index('Date', inplace=True)
    coinPricesDF[['ETHPriceEUR','ETHPriceUSD']] = temp[['ETHPriceEUR','ETHPriceUSD']]
    
    # defichain-price
    coinInfosCG = cg.get_coin_market_chart_range_by_id(id='defichain',vs_currency='eur',from_timestamp=startDate,to_timestamp=endDate)
    coinInfosCGUSD = cg.get_coin_market_chart_range_by_id(id='defichain',vs_currency='usd',from_timestamp=startDate,to_timestamp=endDate)
    temp = pd.DataFrame(coinInfosCG['prices'])
    temp['DFIPriceUSD'] = pd.DataFrame(coinInfosCGUSD['prices'])[1]
    temp = temp.rename(columns={0:'Date',1:'DFIPriceEUR',2:'DFIPriceUSD'})
    temp['Date'] = pd.to_datetime(temp['Date'], unit='ms').dt.date
    temp.set_index('Date', inplace=True)
    coinPricesDF[['DFIPriceEUR','DFIPriceUSD']] = temp[['DFIPriceEUR','DFIPriceUSD']]
    coinPricesDF['DFIPriceEUR'].fillna(0.089,inplace=True)
    coinPricesDF['DFIPriceUSD'].fillna(0.1,inplace=True)
    
    # Dash-price
    coinInfosCG = cg.get_coin_market_chart_range_by_id(id='dash',vs_currency='eur',from_timestamp=startDate,to_timestamp=endDate)
    coinInfosCGUSD = cg.get_coin_market_chart_range_by_id(id='dash',vs_currency='usd',from_timestamp=startDate,to_timestamp=endDate)
    temp = pd.DataFrame(coinInfosCG['prices'])
    temp['DASHPriceUSD'] = pd.DataFrame(coinInfosCGUSD['prices'])[1]
    temp = temp.rename(columns={0:'Date',1:'DASHPriceEUR',2:'DASHPriceUSD'})
    temp['Date'] = pd.to_datetime(temp['Date'], unit='ms').dt.date
    temp.set_index('Date', inplace=True)
    coinPricesDF[['DASHPriceEUR','DASHPriceUSD']] = temp[['DASHPriceEUR','DASHPriceUSD']]
    
    # XZC-price
    coinInfosCG = cg.get_coin_market_chart_range_by_id(id='zcoin',vs_currency='eur',from_timestamp=startDate,to_timestamp=endDate)
    coinInfosCGUSD = cg.get_coin_market_chart_range_by_id(id='zcoin',vs_currency='usd',from_timestamp=startDate,to_timestamp=endDate)
    temp = pd.DataFrame(coinInfosCG['prices'])
    temp['XZCPriceUSD'] = pd.DataFrame(coinInfosCGUSD['prices'])[1]
    temp = temp.rename(columns={0:'Date',1:'XZCPriceEUR',2:'XZCPriceUSD'})
    temp['Date'] = pd.to_datetime(temp['Date'], unit='ms').dt.date
    temp.set_index('Date', inplace=True)
    coinPricesDF[['XZCPriceEUR','XZCPriceUSD']] = temp[['XZCPriceEUR','XZCPriceUSD']]
    
    # PIVX-price
    coinInfosCG = cg.get_coin_market_chart_range_by_id(id='pivx',vs_currency='eur',from_timestamp=startDate,to_timestamp=endDate)
    coinInfosCGUSD = cg.get_coin_market_chart_range_by_id(id='pivx',vs_currency='usd',from_timestamp=startDate,to_timestamp=endDate)
    temp = pd.DataFrame(coinInfosCG['prices'])
    temp['PIVXPriceUSD'] = pd.DataFrame(coinInfosCGUSD['prices'])[1]
    temp = temp.rename(columns={0:'Date',1:'PIVXPriceEUR',2:'PIVXPriceUSD'})
    temp['Date'] = pd.to_datetime(temp['Date'], unit='ms').dt.date
    temp.set_index('Date', inplace=True)
    coinPricesDF[['PIVXPriceEUR','PIVXPriceUSD']] = temp[['PIVXPriceEUR','PIVXPriceUSD']]
    
    # USDT-price
    coinInfosCG = cg.get_coin_market_chart_range_by_id(id='tether',vs_currency='eur',from_timestamp=startDate,to_timestamp=endDate)
    coinInfosCGUSD = cg.get_coin_market_chart_range_by_id(id='tether',vs_currency='usd',from_timestamp=startDate,to_timestamp=endDate)
    temp = pd.DataFrame(coinInfosCG['prices'])
    temp['USDTPriceUSD'] = pd.DataFrame(coinInfosCGUSD['prices'])[1]
    temp = temp.rename(columns={0:'Date',1:'USDTPriceEUR',2:'USDTPriceUSD'})
    temp['Date'] = pd.to_datetime(temp['Date'], unit='ms').dt.date
    temp.set_index('Date', inplace=True)
    coinPricesDF[['USDTPriceEUR','USDTPriceUSD']] = temp[['USDTPriceEUR','USDTPriceUSD']]

    # DOGE-price
    coinInfosCG = cg.get_coin_market_chart_range_by_id(id='dogecoin',vs_currency='eur',from_timestamp=startDate,to_timestamp=endDate)
    coinInfosCGUSD = cg.get_coin_market_chart_range_by_id(id='dogecoin',vs_currency='usd',from_timestamp=startDate,to_timestamp=endDate)
    temp = pd.DataFrame(coinInfosCG['prices'])
    temp['DOGEPriceUSD'] = pd.DataFrame(coinInfosCGUSD['prices'])[1]
    temp = temp.rename(columns={0:'Date',1:'DOGEPriceEUR',2:'DOGEPriceUSD'})
    temp['Date'] = pd.to_datetime(temp['Date'], unit='ms').dt.date
    temp.set_index('Date', inplace=True)
    coinPricesDF[['DOGEPriceEUR','DOGEPriceUSD']] = temp[['DOGEPriceEUR','DOGEPriceUSD']]

    # LTC-price
    coinInfosCG = cg.get_coin_market_chart_range_by_id(id='litecoin',vs_currency='eur',from_timestamp=startDate,to_timestamp=endDate)
    coinInfosCGUSD = cg.get_coin_market_chart_range_by_id(id='litecoin',vs_currency='usd',from_timestamp=startDate,to_timestamp=endDate)
    temp = pd.DataFrame(coinInfosCG['prices'])
    temp['LTCPriceUSD'] = pd.DataFrame(coinInfosCGUSD['prices'])[1]
    temp = temp.rename(columns={0:'Date',1:'LTCPriceEUR',2:'LTCPriceUSD'})
    temp['Date'] = pd.to_datetime(temp['Date'], unit='ms').dt.date
    temp.set_index('Date', inplace=True)
    coinPricesDF[['LTCPriceEUR','LTCPriceUSD']] = temp[['LTCPriceEUR','LTCPriceUSD']]

    # BCH-price
    coinInfosCG = cg.get_coin_market_chart_range_by_id(id='bitcoin-cash',vs_currency='eur',from_timestamp=startDate,to_timestamp=endDate)
    coinInfosCGUSD = cg.get_coin_market_chart_range_by_id(id='bitcoin-cash',vs_currency='usd',from_timestamp=startDate,to_timestamp=endDate)
    temp = pd.DataFrame(coinInfosCG['prices'])
    temp['BCHPriceUSD'] = pd.DataFrame(coinInfosCGUSD['prices'])[1]
    temp = temp.rename(columns={0:'Date',1:'BCHPriceEUR',2:'BCHPriceUSD'})
    temp['Date'] = pd.to_datetime(temp['Date'], unit='ms').dt.date
    temp.set_index('Date', inplace=True)
    coinPricesDF[['BCHPriceEUR','BCHPriceUSD']] = temp[['BCHPriceEUR','BCHPriceUSD']]

    # generate filepath relative to script location
    scriptPath = __file__
    path = scriptPath[:-32] + '/data/'
    filepath = path + 'coinPriceList.csv'
    
    coinPricesDF.to_csv(filepath, index=True)
    
except:
    print('############# Coingecko-API not reached #############')