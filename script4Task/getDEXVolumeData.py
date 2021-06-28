import requests
import pandas as pd

from pycoingecko import CoinGeckoAPI

scriptPath = __file__
path = scriptPath[:-32] + '/data/'
filepath = path + 'DEXVolumeData.csv'

# DEX 24hr trading volume
link='https://api.defichain.io/v1/listswaps?network=mainnet'
siteContent = requests.get(link)
dfDEXVolume = pd.read_json(siteContent.text).transpose()
dfDEXVolume.reset_index(inplace=True)
dfDEXVolume.rename(columns={"index":"pool"},inplace=True)
dfDEXVolume.drop(['base_symbol', 'quote_symbol','base_id','quote_id'], axis=1,inplace=True)
dfDEXVolume['Time'] = pd.Timestamp.now()

# Coingecko 24hr trading volume
try:
    cg = CoinGeckoAPI()
    DFIData = cg.get_price(ids='defichain', vs_currencies='usd', include_24hr_vol='true')
    cgDFI24hVol = DFIData['defichain']['usd_24h_vol']
except:
    cgDFI24hVol = None
    print('############# Coingecko-API not reached #############')

dfDEXVolume['coingeckoVolume'] = cgDFI24hVol
    
dfOldDEXVolume = pd.read_csv(filepath,index_col=0)
dfDEXVolume = dfOldDEXVolume.append(dfDEXVolume, sort=False)
dfDEXVolume.reset_index(inplace=True, drop=True)
    
dfDEXVolume.to_csv(filepath)
print('DEX volume data updated')
