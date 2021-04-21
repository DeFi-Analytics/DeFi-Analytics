from github import Github
from datetime import datetime
from githubSettings import authGithubToken

import pandas as pd

# generate filepath relative to script location
scriptPath = __file__
path = scriptPath[:-37] + '/data/'
filepath = path + 'dataPortfolioDownloads.csv'

# get github repo access
G = Github(authGithubToken) # Put your GitHub token here
repo = G.get_repo("DeFi-PortfolioManagement/defi-portfolio")

# get all downloads
dfNewData = pd.DataFrame(columns=['DateCaptured', 'Windows', 'Mac', 'Linux'])
releases = repo.get_releases()
for release in releases:
    strRelease = release.title
    assets = release.get_assets()
    downloadsDict = {}
    for item in assets:
        if 'linux' in item.name:
            strSystem = 'Linux'
        elif 'mac' in item.name:
            strSystem = 'Mac'
        elif '.exe' in item.name:
            strSystem = 'Windows'
        else:
            strSystem = 'unknown'
        downloadsDict[strSystem]=item.download_count

    dfNewData.loc[strRelease] = downloadsDict

# add capture date information
dateTimeObj = datetime.now()
strTimestamp = dateTimeObj.strftime("%Y-%m-%d")
dfNewData.loc[:, 'DateCaptured'] = strTimestamp

# append new data to existing datbase
dfReleaseData = pd.read_csv(filepath, index_col=0)
dfReleaseData = dfReleaseData.append(dfNewData)

dfReleaseData.to_csv(filepath)