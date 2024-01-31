import glob

import numpy as np
import pandas as pd

import requests
import json


scriptPath = __file__
path = scriptPath[:-38] + '/data/'
filepath = path+'extractedDFIdata.csv'
filepathSnapshot = path + 'snapshotData.csv'


pathRichlist = scriptPath[:-38] + '/data/Richlist/'
listCSVFiles = glob.glob(pathRichlist+"*_01-*.csv")
foundRichlistFiles = [richlistDate for richlistDate in listCSVFiles]


colNames = ['date', 'nbMnId', 'nbOtherId', 'fundDFI', 'mnDFI', 'otherDFI', 'foundationDFI', 'nbMnGenesisId', 'mnGenesisDFI', 'nbMnCakeId', 'mnCakeDFI', 'erc20DFI',
            'burnedDFI', 'tokenDFI', 'nbMydefichainId', 'mnMydefichainDFI', 'nbMNlocked5', 'nbMNlocked10']

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
        nbMNlocked5 = rawRichlist[rawRichlist.timelock == '5 years'].shape[0]
        nbMNlocked10 = rawRichlist[rawRichlist.timelock == '10 years'].shape[0]

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
        # get CF DFI from on-chain governance
        linkCFinfo = 'https://api.mydefichain.com/v1/listcommunitybalances/'
        siteContent = requests.get(linkCFinfo)
        if siteContent.status_code==200:
            tempData = json.loads(siteContent.text)
            fundDFIValue = fundDFIValue + tempData['CommunityDevelopmentFunds']


        if addERC20 in rawRichlist.values:
            erc20DFIValue = rawRichlist[rawRichlist.address == addERC20].balance.values[0]
        else:
            erc20DFIValue = 0

        # get all burned DFI
        linkBurninfo = 'http://api.mydefichain.com/v1/getburninfo/'
        siteContent = requests.get(linkBurninfo)
        if siteContent.status_code==200:
            tempData = json.loads(siteContent.text)
            burnedDFICoins = tempData['amount']
            burnedDFIFees = tempData['feeburn']
            burnedDFIRewards = tempData['emissionburn']
            burnedDFIToken = tempData['tokens'][0][:-4]
            burnedDFIAuction = tempData['auctionburn']
            burnedDFILoan = tempData['paybackburn']
            burnedDFIPaybackFee = tempData['dfipaybackfee']
        else:
            burnedDFIFees = np.NaN

        burnedDFIValue = float(burnedDFICoins) + float(burnedDFIFees) + float(burnedDFIRewards) + float(burnedDFIToken) + float(burnedDFIAuction) + float(burnedDFILoan[0][:-4]) + float(burnedDFIPaybackFee)


        # if addDFIToken in rawRichlist.values:
        #     tokenDFIValue = rawRichlist[rawRichlist.address == addDFIToken].balance.values[0]
        # else:
        #     tokenDFIValue = 0
        # workaround for DFI-token: use estimation from snapshot data

        snapshotData = pd.read_csv(filepathSnapshot, index_col=0)
        tokenDFIValue = snapshotData['tokenDFI'].values[0]

        # generate Series to be add to existing dataframe
        listDFI2Add = [currDate, nbMnId, nbOtherId, fundDFIValue, mnDFI, otherDFI, foundationDFIValue, nbMnGenesisId, mnGenesisDFI, nbMnCakeId, mnCakeDFI, erc20DFIValue,
                       burnedDFIValue, tokenDFIValue, nbMnMydefichainId, mnMydefichainDFI, nbMNlocked5, nbMNlocked10]
        seriesDFI2Add = pd.Series(listDFI2Add, index=colNames)

        dfDFIData = dfDFIData.append(seriesDFI2Add, ignore_index=True, sort=False)
        print('...added to extractedDFIdata.csv')

dfDFIData = dfDFIData.sort_values(by=['date'])
dfDFIData.to_csv(filepath, index = False)