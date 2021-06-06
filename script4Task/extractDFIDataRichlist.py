import glob

import numpy as np
import pandas as pd

import requests
import json


scriptPath = __file__
path = scriptPath[:-38] + '/data/'
filepath = path+'extractedDFIdata.csv'

pathRichlist = scriptPath[:-38] + '/data/Richlist/'
listCSVFiles = glob.glob(pathRichlist+"*_01-*.csv")
foundRichlistFiles = [richlistDate for richlistDate in listCSVFiles]


colNames = ['date', 'nbMnId', 'nbOtherId', 'fundDFI', 'mnDFI', 'otherDFI', 'foundationDFI', 'nbMnGenesisId', 'mnGenesisDFI', 'nbMnCakeId', 'mnCakeDFI', 'erc20DFI',
            'burnedDFI', 'tokenDFI', 'nbMydefichainId', 'mnMydefichainDFI']

dfDFIData = pd.read_csv(filepath)

for richlistFile in foundRichlistFiles:
    if richlistFile[-32:-22] not in dfDFIData.date.values:
        rawRichlist = pd.read_csv(richlistFile)
        print('File '+richlistFile+'...')
        currDate = richlistFile[-32:-22]

        # special DFI addresses
        addFoundation = 'dJEbxbfufyPF14SC93yxiquECEfq4YSd9L'
        addFoundationAirdrop = 'dMysnhSbg8VbJJjdj273bNQi6i69z4WL6Z'
        addFund = 'dZcHjYhKtEM88TtZLjp314H2xZjkztXtRc'

        addERC20 = 'dZFYejknFdHMHNfHMNQAtwihzvq7DkzV49'
        addBurned = '8defichainBurnAddressXXXXXXXdRQkSm'

        addDFIToken = 'DFITokenOnDefiChain'     # this amount was captured via token richlist, it is not included in the DFI Richlist

        mnGenesis1 = '8KRsoeCRKHUFFmAGGJbRBAgraXiUPUVuXn'
        mnGenesis2 = '8RPZm7SVUNhGN1RgGY3R92rvRkZBwETrCX'
        mnGenesis3 = '8PuErAcazqccCVzRcc8vJ3wFaZGm4vFbLe'

        condMNGenesis = (rawRichlist.address == mnGenesis1) | (rawRichlist.address == mnGenesis2) | (rawRichlist.address == mnGenesis3)
        condMN = rawRichlist.mnAddressAPI

        if 'mnAddressCakeAPI' in rawRichlist.columns:
            condMNCake = rawRichlist.mnAddressCakeAPI & rawRichlist.mnAddressAPI
        else:
            condMNCake = rawRichlist.mnAddressAPI & False

        # get MN of mydefichain via excel sheet (will be replaced after API is available)
        filepathMydefichain = path + 'mydefichainOperatornodes.xlsx'
        dfMydefichainData = pd.read_excel(filepathMydefichain, sheet_name='listmasternodes')
        dfMydefichainData = dfMydefichainData[dfMydefichainData['Spalte1'] == 'mydefichain']
        rawRichlist['mnAddressMyDefichain'] = rawRichlist['address'].isin(dfMydefichainData['Value.ownerAuthAddress'])

        if 'mnAddressCakeAPI' in rawRichlist.columns:
            condMNMydefichain = rawRichlist.mnAddressMyDefichain & rawRichlist.mnAddressAPI
        else:
            condMNMydefichain = rawRichlist.mnAddressAPI & False

        condOtherAddress = (~condMN) & (rawRichlist.address != addFund) & (rawRichlist.address != addFoundation) & (rawRichlist.address != addFoundationAirdrop) \
                             & (rawRichlist.address != addERC20) & (rawRichlist.address != addBurned) & (rawRichlist.address != addDFIToken)

        # get balances of mn and private wallets
        balanceMN = rawRichlist[condMN].balance
        balanceMNCake = rawRichlist[condMNCake].balance
        balanceMNMydefichain = rawRichlist[condMNMydefichain].balance
        balanceMNGenesis = rawRichlist[condMNGenesis].balance
        balancePrivat = rawRichlist[condOtherAddress].balance


        # calc addcress number for Dashboard
        nbMnId = balanceMN.size
        nbMnCakeId = balanceMNCake.size
        nbMnMydefichainId = balanceMNMydefichain.size
        nbMnGenesisId = balanceMNGenesis.size
        nbOtherId = balancePrivat.size

        # calc DFI amount on address category
        mnDFI = balanceMN.sum()
        mnCakeDFI = balanceMNCake.sum()
        mnMydefichainDFI = balanceMNMydefichain.sum()
        mnGenesisDFI = balanceMNGenesis.sum()
        otherDFI = balancePrivat.sum()
        if addFoundation in rawRichlist.values:
            foundationDFIValue = rawRichlist[rawRichlist.address == addFoundation].balance.values[0]
        else:
            foundationDFIValue = 0

        if addFoundationAirdrop in rawRichlist.values: # add amount of DFI airdrop
            foundationDFIValue = foundationDFIValue+rawRichlist[rawRichlist.address == addFoundationAirdrop].balance.values[0]

        if addFund in rawRichlist.values:
            fundDFIValue = rawRichlist[rawRichlist.address == addFund].balance.values[0]
        else:
            fundDFIValue = np.NaN

        if addERC20 in rawRichlist.values:
            erc20DFIValue = rawRichlist[rawRichlist.address == addERC20].balance.values[0]
        else:
            erc20DFIValue = 0

        # get all burned DFI
        linkBurninfo = 'http://api.mydeficha.in/v1/getburninfo/'
        siteContent = requests.get(linkBurninfo)
        if siteContent.status_code==200:
            tempData = pd.read_json(siteContent.text).transpose()
            burnedDFIFees = tempData.iloc[2, 0]
        else:
            burnedDFIFees = np.NaN

        linkBurnRewards = 'https://api.defichain.io/v1/stats?network=mainnet&pretty'
        siteContent = requests.get(linkBurnRewards)
        if siteContent.status_code==200:
            tempData = json.loads(siteContent.text)
            burnedDFIRewards = tempData['listCommunities']['Burnt']
        else:
            burnedDFIRewards = np.NaN

        if addBurned in rawRichlist.values:
            burnedDFICoins = rawRichlist[rawRichlist.address == addBurned].balance.values[0]
        else:
            burnedDFICoins = 0

        burnedDFIValue = burnedDFICoins + burnedDFIFees + burnedDFIRewards


        if addDFIToken in rawRichlist.values:
            tokenDFIValue = rawRichlist[rawRichlist.address == addDFIToken].balance.values[0]
        else:
            tokenDFIValue = 0

        # generate Series to be add to existing dataframe
        listDFI2Add = [currDate, nbMnId, nbOtherId, fundDFIValue, mnDFI, otherDFI, foundationDFIValue, nbMnGenesisId, mnGenesisDFI, nbMnCakeId, mnCakeDFI, erc20DFIValue,
                       burnedDFIValue, tokenDFIValue, nbMnMydefichainId, mnMydefichainDFI]
        seriesDFI2Add = pd.Series(listDFI2Add, index=dfDFIData.columns)

        dfDFIData = dfDFIData.append(seriesDFI2Add, ignore_index=True, sort=False)
        print('...added to extractedDFIdata.csv')

dfDFIData = dfDFIData.sort_values(by=['date'])
dfDFIData.to_csv(filepath, index = False)