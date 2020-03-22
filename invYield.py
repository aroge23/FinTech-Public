import requests as req
import re

def yieldInv(sYear):
    year = sYear
    web = "https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%20" + year
    f = req.get(web)
    site = f.text
    site = site[569:]

    yieldten = []
    yieldtwo = []
    numList = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    for i in range(site.count("\">" + year)):
        if site[site.find("BC_10YEAR") + 33] != "<":
            if site[site.find("BC_10YEAR") + 32] in numList:
                yieldten.append(site[site.find("BC_10YEAR") + 30: site.find("BC_10YEAR") + 34])
            else:
                yieldten.append(yieldten[i-1])
        else:
            yieldten.append(site[site.find("BC_10YEAR") + 30: site.find("BC_10YEAR") + 33])
        if site[site.find("BC_2YEAR") + 32] != "<":
            if site[site.find("BC_2YEAR") + 31] in numList:
                yieldtwo.append(site[site.find("BC_2YEAR") + 29: site.find("BC_2YEAR") + 33])
            else:
                if i == 0:
                    yieldtwo.append(site[site.find("BC_2YEAR") + 29] + ".0")
                else:
                    yieldtwo.append(yieldtwo[i - 1])
        else:
            yieldtwo.append(site[site.find("BC_2YEAR") + 29: site.find("BC_2YEAR") + 32])

        site = site[1516:]

    yieldten = [float(re.search(r'\d+.\d+',number).group()) for number in yieldten]
    yieldtwo = [float(re.search(r'\d+.\d+',number).group()) for number in yieldtwo]

    yinv = []
    for i in range(len(yieldten)):
        yinv.append(yieldten[i] - yieldtwo[i])

    return yinv

def yieldYear(sYear):
    year = str(sYear)
    web = "https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%20" + year
    f = req.get(web)
    site = f.text
    site = site[569:]

    yieldyear = []
    for i in range(site.count("\">" + year)):
        yieldyear.append(site[site.find("\">" + year) + 2 : site.find("\">" + year) + 12])
        site = site[1516:]

    return yieldyear
#2085