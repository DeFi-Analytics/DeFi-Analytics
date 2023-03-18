import os
import subprocess
import json
import numpy as np

import pandas as pd
import plotly.io as pio
import datetime
import keyboard

from nested_lookup import nested_lookup, get_occurrences_and_values
from nested_lookup import get_occurrence_of_value

from bitcoinrpc.authproxy import AuthServiceProxy
from script4Task.credentials import rpc_username, rpc_password, rpc_hostname, rpc_port

pio.renderers.default = 'browser'

scriptPath = os.path.abspath(os.getcwd())
if scriptPath[0] == 'H':
    scriptPath=scriptPath[:-12]
path = scriptPath + '/data/'
filepathBlocklist = path +'Blocklist4DAA.csv'
filepathDAA = path +'DAAResult.csv'
filepathCountDAA = path +'analyzedDataDAA.csv'


# # load exisiting blocklist
dfBlockList = pd.read_csv(filepathBlocklist,index_col=0)
dfBlockList.sort_values(by='height', ascending=True, inplace=True)
# dfBlockList = pd.DataFrame(columns=['addressesDone', 'hash', 'height', 'time'])

# load existing daa file
dfDAA = pd.read_csv(filepathDAA,index_col=0,low_memory=False)
# dfDAA = pd.DataFrame()

rpc_connection = AuthServiceProxy(f'http://{rpc_username}:{rpc_password}@{rpc_hostname}:{rpc_port}')
currBlockNb = rpc_connection.getblockcount()
lastBlockEvaluation = dfBlockList.height.max()+1

# lastBlockEvaluation = 0

print('Start evaluating the blocks')
try:
    while lastBlockEvaluation <= currBlockNb:
        blockHash = rpc_connection.getblockhash(int(lastBlockEvaluation))

        jsonBlock = rpc_connection.getblock(blockHash,2)
        # if (jsonBlock['height'] % 100) ==0:
        print('BlockHeight: ',jsonBlock['height'])
        blockDate = datetime.datetime.fromtimestamp(jsonBlock['time'])
        dateString = blockDate.strftime('%Y-%m-%d')

        # for loops over vin and vout
        listSenderAddresses = []
        listReceiverAddresses = []
        for txEntry in jsonBlock['tx']:
            for vinEntry in txEntry['vin']:
                if 'txid' in vinEntry:
                    tempHash = vinEntry['txid']
                    neededVout = vinEntry['vout']
                    jsonTx = rpc_connection.getrawtransaction(tempHash, True)
                    senderAddress = jsonTx['vout'][neededVout]['scriptPubKey']['addresses'][0]
                    listSenderAddresses.append(senderAddress)
            for voutEntry in txEntry['vout']:
                if 'addresses' in voutEntry['scriptPubKey']:
                    listReceiverAddresses.append(voutEntry['scriptPubKey']['addresses'][0])
        listAddresses = listReceiverAddresses + listSenderAddresses

        # merge new addresslist of block with exisiting database
        if dateString in dfDAA.columns:
            columnData = listAddresses+dfDAA[dateString].to_list()
            dfDAA.drop(columns=[dateString],inplace=True)
        else:
            columnData = listAddresses

        dfBlock = pd.DataFrame(data=columnData, columns=[dateString])
        dfBlock.drop_duplicates(inplace=True)  # remove duplicates
        dfBlock.dropna(inplace=True)  # remove nan's
        dfBlock.reset_index(inplace=True, drop=True)  # reindex the remaining column

        dfDAA = dfDAA.merge(dfBlock, how='outer', left_index=True, right_index=True)
        dfDAA.dropna(how='all', inplace=True)

        dfBlockList = dfBlockList.append({'addressesDone': True, 'hash': blockHash, 'height': lastBlockEvaluation, 'time': blockDate}, ignore_index=True)
        lastBlockEvaluation += 1

        # if keyboard.read_key() == "c":
        #     print("Cancel evaluation")
        #     break
except:
    print('#### Error in RPC Call')

print('Save csv files ...')
dfBlockList.sort_values(by='height', ascending=False, inplace=True)
dfBlockList.to_csv(filepathBlocklist)
dfDAA.to_csv(filepathDAA)

dfCountDAA = pd.DataFrame()
dfCountDAA['Date'] = dfDAA.columns
dfCountDAA['countAddresses'] = dfDAA.count().values
dfCountDAA.to_csv(filepathCountDAA)
print('... finished')

