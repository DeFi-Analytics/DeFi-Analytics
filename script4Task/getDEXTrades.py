import requests
import pandas as pd

# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-28] + '/data/'

filepathCoinPrices = path + 'coinPriceList.csv'
filepathTradingResults = path + 'dailyTradingResultsDEX.csv'


availablePools = {'ETH':4,'BTC':5,'USDT':6,'DOGE':8,'LTC':10,'BCH':12,'USDC':14}
dfTradeResult = pd.DataFrame()

# get all swaps over all pools
for key in availablePools: 
    print('Checking trades of pool: ' + key)
    linkTrade = 'https://api.defichain.io/v1/getswaptransaction?id='+str(availablePools.get(key))+'&network=mainnet&skip=0&limit=1000000'
    siteContent = requests.get(linkTrade)
    dfJSON = pd.read_json(siteContent.text,orient='columns')
    nbTradesDEX = dfJSON['total'].max()
    
    dfTrades = pd.DataFrame(dfJSON.data.tolist())
    dfTrades['Date'] = pd.to_datetime(dfTrades['blockTime'],utc=True).dt.strftime('%Y-%m-%d')
    
    availableBaseToken = dfTrades.baseTokenSymbol.unique()
    dfTradeResult[key+'pool_nbTrades'] = dfTrades.groupby('Date')['_id'].count()
    dfTradeResult[key+'pool_base'+availableBaseToken[0]] = dfTrades.loc[dfTrades.baseTokenSymbol==availableBaseToken[0]].groupby('Date')['baseTokenAmount'].sum()
    dfTradeResult[key+'pool_quote'+availableBaseToken[0]] = dfTrades.loc[dfTrades.quoteTokenSymbol==availableBaseToken[0]].groupby('Date')['quoteTokenAmount'].sum()
    dfTradeResult[key+'pool_base'+availableBaseToken[1]] = dfTrades.loc[dfTrades.baseTokenSymbol==availableBaseToken[1]].groupby('Date')['baseTokenAmount'].sum()
    dfTradeResult[key+'pool_quote'+availableBaseToken[1]] = dfTrades.loc[dfTrades.quoteTokenSymbol==availableBaseToken[1]].groupby('Date')['quoteTokenAmount'].sum()


# add usd price information for all coins
dfCoinPrices = pd.read_csv(filepathCoinPrices,index_col=0)
dfTradeResult = dfTradeResult.merge(dfCoinPrices[['DFIPriceUSD','BTCPriceUSD','ETHPriceUSD','USDTPriceUSD','DOGEPriceUSD','LTCPriceUSD','BCHPriceUSD','USDCPriceUSD']],
                                    how='left',left_index=True, right_index=True)

# calculate trading volume in USD for each base coin and sum of pool
print('Calculating USD trading volume')
for key in availablePools: 
    dfTradeResult[key+'pool_base'+key+'_inUSD'] = dfTradeResult[key+'pool_base'+key]*dfTradeResult[key+'PriceUSD']
    dfTradeResult[key+'pool_baseDFI_inUSD'] = dfTradeResult[key+'pool_baseDFI']*dfTradeResult['DFIPriceUSD']
    dfTradeResult[key+'pool_sum_inUSD'] = dfTradeResult[key+'pool_base'+key+'_inUSD']+dfTradeResult[key+'pool_baseDFI_inUSD']

dfTradeResult.iloc[:-1].to_csv(filepathTradingResults)