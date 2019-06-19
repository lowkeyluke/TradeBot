import csv
import json
import numpy as np
import requests
import time
import datetime

'''
Tasks (Automated):
1. obtain data
- Find all companies that fulfill the private filter
  - utilizes Web Scraping
2. prepare data
3. Run private algorithm on cooked data
- return Confirmation
4. Buy & Sell
- if confirmation > threshold: 
  - purchaseOrder() @ specified buyTime
  - if price > pThreshold: 
    - sellOrder() @ specified sellTime
    else:
      - send notification to user's phone to manually handle sell
'''

def collectCompanies(url, splitters):
    # Collect all companies where XXXXXX
    response = requests.get(url)

    webScrape = response.content.decode('utf-8')  # decode bytes
    webScrape = csv.reader(webScrape.splitlines())
    webScrape = list(webScrape)

    splitterStr, splitterStr2 = splitters

    tickers = []
    for i in range(len(webScrape)):
        if splitterStr in str(webScrape[i]) and splitterStr2 in str(webScrape[i]):
            x = str(webScrape[i])
            splitter = x.split(splitterStr)
            splitter2 = splitter[1].split(splitterStr2)
            ticker = splitter2[0].upper()
            tickers.append(ticker)
    print(tickers)
    return tickers

def convertDate(dates):
    # Convert dates from xm/dd/yyyy format to yyyy-mm-dd format
    dateCount = 0
    for date in dates:
        date = datetime.datetime.strptime(date, "%m/%d/%Y").date()
        date = date.strftime('%Y-%m-%d')
        dates[dateCount] = date
        dateCount += 1
    return dates


def computeConfirmation(tickers, url, restrict, private, privateBody, privs):
    # API restriction: ONLY X CALLS/MIN. use time library accordingly
    currentTime = time.time()
    endTime = time.time()

    confirmProbs = []
    print("Evaluating", len(tickers), "companies...")
    count = 0
    ''' FOR EACH COMPANY '''
    for ticker in tickers:
        # X calls/min (API restriction)
        if endTime - currentTime < 60 and len(confirmProbs) >= restrict and len(confirmProbs)%restrict == 0:
            wait = 60 - int(endTime - currentTime)
            remaining = len(tickers) - count
            print("sleeping for", wait,"seconds (to avoid API restriction)...")
            print("(", remaining, "companies remaining )")
            # if count > 10:
            #     return confirmProbs  # TEMPORARY: TESTING PURPOSES ONLY
            time.sleep(wait)
            currentTime = time.time()

        data2 = []
        data1 = []
        # private lines

        ''' API CALL: GET REQUEST  '''
        print(url)
        response = requests.get(url)
        apidata = response.content.decode('utf-8')  # decode bytes
        apidata = csv.reader(apidata.splitlines())
        apidata = list(apidata)
        for i in range(len(apidata)):
            if private:
                privateBody.run()
            else:
                break
        '''
        algo
            - return confirmationProbability, paired w/ ticker
        '''
        if data2:
            confirmCount = 0
            for d2, d1, priv in zip(data2, data1, privs):
                d2P = float(d2[2])
                d1P = float(d1[4])
                priv = float(priv)
                if private:
                    confirmCount += 1
            confirmProb = confirmCount / len(data2)
            confirmProbs.append((ticker, confirmProb))
        else:
            print(ticker, "DATA NOT FOUND")
        print(confirmProbs)

        count += 1
        endTime = time.time()

    return confirmProbs


def purchaseOrder(ticker, hourP, minP):
    print("purchasing", ticker, "...")

    currentTime = datetime.datetime.now()
    print("Current time:", currentTime)
    today = currentTime.date()
    purchaseTime = datetime.datetime(today.year, today.month, today.day, hourP, minP)
    wait = int(purchaseTime.timestamp() - currentTime.timestamp())
    print("Time until purchase (seconds):", wait)

    if wait > 0:
        print("Sleeping for", wait, "seconds...")
        time.sleep(wait)

    '''MAKE PURCHASE'''
    print("PRIVATE")

def sellOrder(ticker, hourP, minP):
    print("selling", ticker, "...")

    currentTime = datetime.datetime.now()
    print("Current time:", currentTime)
    today = currentTime.date()
    sellTime = datetime.datetime(today.year, today.month, today.day, hourP, minP)
    wait = int(sellTime.timestamp() - currentTime.timestamp())
    print("Time until sell:", wait)
    print("Sleeping for", wait, "seconds...")
    time.sleep(wait)

    '''MAKE SALE'''
    # fill sell order
    print("PRIVATE")


''' MAIN SCRIPT '''
threshold = .9
tickers = collectCompanies()
confirmProbs = computeConfirmation(tickers)
rem = []
for i in range(len(confirmProbs)):
    ticker, confirmProb = confirmProbs[i]
    if confirmProb > threshold:
        rem.append((ticker, confirmProb))
confirmProbs = rem
print(len(confirmProbs), "companies passed Confirmation threshold of", threshold, "!")
print(confirmProbs)

for ticker, confirmProb in confirmProbs:
    if confirmProb > threshold:
        currentTime = time.time()
        # MISSING EXCLUSIVE PRIVATE CODE
        privateHour = 0
        privateMin = 0
        purchaseOrder(ticker, privateHour, privateMin)  # time-sensitive method that will only execute @ specified time

for ticker, confirmProb in confirmProbs:
    if confirmProb > threshold:  # if ticker has been purchased:
        currentTime = time.time()
        # MISSING EXCLUSIVE PRIVATE CODE
        privateHour = 0
        privateMin = 0
        sellOrder(ticker, privateHour, privateMin)


