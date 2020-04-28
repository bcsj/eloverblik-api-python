import json
import matplotlib.pyplot as plt
import numpy as np
import requests

# ============== ACCESS TOKEN AND URL BASE =================

accessToken = ""  # <-- The ACCESS TOKEN goes here

urlbase = 'https://api.eloverblik.dk/CustomerApi/'

# ============== METHODS =================

# Method for getting a data token
def getDataToken(accessToken):
    headers = {'Authorization': 'Bearer ' + accessToken}
    path = '/api/Token'
    url = urlbase + path
    reg = requests.get(url, headers=headers)
    if not reg.ok:
        return False, ''
    dataToken = json.loads(reg.content)['result']
    return True, dataToken

# Method for getting the metering point id
def getMeteringPointId(dataToken):
    headers = {'Authorization': 'Bearer ' + dataToken}
    path = '/api/MeteringPoints/MeteringPoints?includeAll=true'
    url = urlbase + path
    reg = requests.get(url, headers=headers)
    if not reg.ok:
        return False, ''
    meteringPointId = json.loads(reg.content)['result'][0]['meteringPointId']
    return True, meteringPointId

# Method for making a time series request
def getTimeSeries(dataToken, meteringPointId, dateFrom, dateTo, aggregation):
    headers = {'Authorization': 'Bearer ' + dataToken}
    data = {"meteringPoints": {
        "meteringPoint": [
            meteringPointId
    ]}}
    path = '/api/MeterData/GetTimeSeries/{:s}/{:s}/{:s}'.format(dateFrom,dateTo,aggregation)
    url = urlbase + path
    reg = requests.post(url, headers=headers, json=data)
    if not reg.ok:
        return False, np.array([]), np.array([])
    T, Y = parse(reg)
    return True, T, Y

# Parser for the getTimeSeries request result
def parse(reg):
    X = json.loads(reg.content)
    X = X['result'][0]['MyEnergyData_MarketDocument']
    X = X['TimeSeries'][0]['Period']

    T = []
    Y = []
    c = 0
    for period in X:
        for point in period['Point']:
            T.append(float(point['position'])+c-1)
            Y.append(float(point['out_Quantity.quantity']))
        c += len(period['Point'])
    return np.array(T), np.array(Y)

# Checks status and prints the error message if the status is False
def checkStatus(status, err):
    if not status:
        print(err)
        import sys
        sys.exit()

# ============== SCRIPT =================

# Get a data token
status,dataToken = getDataToken(accessToken)
checkStatus(status, 'Failed to get Data Token!')

# Get metering point id
status,meteringPointId = getMeteringPointId(dataToken)
checkStatus(status, 'Failed to get Metering Point ID!')

# Get (hourly) time series data
status, T, Y = getTimeSeries(dataToken, meteringPointId, '2020-01-01', '2020-01-08', 'Hour')
checkStatus(status, 'Failed to get Time Series!')

plt.ion() # interactive plotting

# Create a plot from the data
fig = plt.figure(1)
plt.plot(T, Y)
plt.ylim(0, max(Y))
plt.xlim(T[0], T[-1])
plt.xticks([24*i for i in range(len(T)//24)],
           ['Jan {:d}'.format(i+1) for i in range(len(T)//2)])
plt.ylabel('kWh')
plt.title('Energy consumption 2020 Jan 1st -- Jan 7th')
fig.tight_layout()

# Colorizes certain time intervals of the day
for i in range(len(T)//24):
    plt.axvspan(24*i, 24*i+8, facecolor=(1, .7, .0), alpha=0.25)
for i in range(len(T)//24):
    plt.axvspan(8 + 24*i, 17 + 24*i, facecolor=(.35, 1, .35), alpha=0.25)
for i in range(len(T) // 24):
    plt.axvspan(17 + 24 * i, 24 + 24 * i, facecolor=(1, .35, .35), alpha=0.25)

# Get (daily) time series data for the first (approx.) 4 months of 2020
status, T, Y = getTimeSeries(dataToken, meteringPointId, '2020-01-01', '2020-04-28', 'Day')
checkStatus(status, 'Failed to get Time Series!')

# Crate a plot from the data
fig = plt.figure(2)
plt.plot(T, Y)
plt.ylim(0, max(Y))
plt.xlim(T[0], T[-1])
plt.xticks([0, 31, 60, 91], ['Jan', 'Feb', 'Mar', 'Apr'])
plt.ylabel('kWh')
plt.title('Energy (daily) consumption 2020 Jan--Apr (28th)')
fig.tight_layout()

# Colorize January and March ... just 'cause ... readibility(?)
plt.axvspan(0, 31, facecolor=(0, .7, 1), alpha=0.25)
plt.axvspan(60, 90, facecolor=(0, .7, 1), alpha=0.25)
