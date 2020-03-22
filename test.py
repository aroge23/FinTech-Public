import requests as req
import re

year = "2020"
web = "https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%20" + year
f = req.get(web)
site = f.text
site = site[569:]

yieldyear = []
yieldten = []
yieldtwo = []
for i in range(site.count("\">" + year)):
    yieldyear.append(site[site.find("\">" + year) + 2 : site.find("\">" + year) + 12])
    yieldten.append(site[site.find("BC_10YEAR") + 30 : site.find("BC_10YEAR") + 34])
    yieldtwo.append(site[site.find("BC_2YEAR") + 29 : site.find("BC_2YEAR") + 33])

    site = site[1516:]

yieldten = [float(re.search(r'\d+.\d+',number).group()) for number in yieldten]
yieldtwo = [float(re.search(r'\d+.\d+',number).group()) for number in yieldtwo]

yinv = []
for i in range(len(yieldten) - 2):
    yinv.append(yieldten[i] - yieldtwo[i])
print(yinv)
#2085