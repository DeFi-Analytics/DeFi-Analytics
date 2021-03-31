import os
import requests
import pandas as pd


scriptPath = __file__
path = scriptPath[:-32] + '/data/'
filepath = path + 'DEXVolumeData.csv'


link='https://api.defichain.io/v1/listswaps?network=mainnet'
siteContent = requests.get(link)
dfDEXVolume = pd.read_json(siteContent.text).transpose()
dfDEXVolume.reset_index(inplace=True)
dfDEXVolume.rename(columns={"index":"pool"},inplace=True)
dfDEXVolume.drop(['base_symbol', 'quote_symbol','base_id','quote_id'], axis=1,inplace=True)
dfDEXVolume['Time'] = pd.Timestamp.now()


    
dfOldDEXVolume = pd.read_csv(filepath,index_col=0)
dfDEXVolume = dfOldDEXVolume.append(dfDEXVolume)
dfDEXVolume.reset_index(inplace=True, drop=True)
    
dfDEXVolume.to_csv(filepath)
