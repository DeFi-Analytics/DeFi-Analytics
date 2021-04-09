import glob

import numpy as np
import pandas as pd

from datetime import datetime


scriptPath = __file__
path = scriptPath[:-38] + '/data/'
filepath = path+'extractedDFIdata.csv'

pathRichlist = scriptPath[:-38] + '/data/Richlist/'
listCSVFiles = glob.glob(pathRichlist+"*_01-*.csv")
foundRichlistFiles = [richlistDate for richlistDate in listCSVFiles]


colNames = ['date', 'nbMnId', 'nbOtherId', 'fundDFI', 'mnDFI', 'otherDFI', 'foundationDFI', 'nbMnGenesisId', 'mnGenesisDFI','nbMnCakeId' ,'mnCakeDFI']

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
        addUnknown = 'dESMvgak9hSnyjdax5TABavnCyhn2nQ1iE'
        mnGenesis1 = '8KRsoeCRKHUFFmAGGJbRBAgraXiUPUVuXn'
        mnGenesis2 = '8RPZm7SVUNhGN1RgGY3R92rvRkZBwETrCX'
        mnGenesis3 = '8PuErAcazqccCVzRcc8vJ3wFaZGm4vFbLe'

        condMNGenesis = (rawRichlist.address == mnGenesis1) | (rawRichlist.address == mnGenesis2) | (rawRichlist.address == mnGenesis3)
        condMN = rawRichlist.mnAddressAPI
        condMNCake = rawRichlist.mnAddressCakeAPI
        condPrivateAddress = (~condMN) & (rawRichlist.address != addFund) & (rawRichlist.address != addFoundation) & (rawRichlist.address != addFoundationAirdrop)

        # get balances of mn and private wallets
        balanceMN = rawRichlist[condMN].balance
        balanceMNCake = rawRichlist[condMNCake].balance
        balanceMNGenesis = rawRichlist[condMNGenesis].balance
        balancePrivat = rawRichlist[condPrivateAddress].balance

        #calc data for Dashboard
        nbMnId = balanceMN.size
        nbMnCakeId = balanceMNCake.size
        nbMnGenesisId = balanceMNGenesis.size
        nbOtherId = balancePrivat.size
        if addFund in rawRichlist.values:
            fundDFIValue = rawRichlist[rawRichlist.address == addFund].balance.values[0]
        else:
            fundDFIValue = np.NaN

        mnDFI = balanceMN.sum()
        mnCakeDFI = balanceMNCake.sum()
        mnGenesisDFI = balanceMNGenesis.sum()
        otherDFI = balancePrivat.sum()

        if addFoundation in rawRichlist.values:
            foundationDFIValue = rawRichlist[rawRichlist.address == addFoundation].balance.values[0]
        else:
            foundationDFIValue = np.NaN

        if addFoundationAirdrop in rawRichlist.values: # add amount of DFI airdrop
            foundationDFIValue = foundationDFIValue+rawRichlist[rawRichlist.address == addFoundationAirdrop].balance.values[0]


        listDFI2Add = [currDate, nbMnId, nbOtherId, fundDFIValue, mnDFI, otherDFI, foundationDFIValue, nbMnGenesisId, mnGenesisDFI, nbMnCakeId, mnCakeDFI]
        seriesDFI2Add = pd.Series(listDFI2Add, index=dfDFIData.columns)

        dfDFIData = dfDFIData.append(seriesDFI2Add, ignore_index=True, sort=False)
        print('...added to extractedDFIdata.csv')

dfDFIData = dfDFIData.sort_values(by=['date'])
dfDFIData.to_csv(filepath, index = False)