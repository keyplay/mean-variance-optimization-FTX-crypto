# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 16:14:36 2021

@author: NTU
"""

import client
from datetime import datetime
import numpy as np
from optimization import mini_vol, portfolio_info
import matplotlib.pyplot as plt

def jsonParser(json_ele):
    return [json_ele['time'], json_ele['close']]

# --------- config setting ------------
api_key=''
api_secret=''

subaccount_name='All'
tickers = ['BTC-PERP', 'ETH-PERP', 'ADA-PERP']
resolution = 3600   # interval 1 hour
freq = 365 * 24

start_time_str = '2021-10-01T00:00:00+0000'
end_time_str = '2021-10-31T23:00:00+0000'

start_time = int(datetime.timestamp(datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S%z')))
end_time = int(datetime.timestamp(datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S%z')))

# ----------- get historical data and calculate return ------------
ret_ave = []
ret_list = []
ftx_cli = client.FtxClient(api_key=api_key, api_secret=api_secret, subaccount_name=subaccount_name)
for ticker in tickers:
    data = ftx_cli.get_historical_data(market=ticker, resolution=str(resolution), start_time=str(start_time), end_time=str(end_time))
    close_price = np.array(list(map(jsonParser, data)))
    ret = (close_price[1:, 1] - close_price[:-1, 1]) / close_price[:-1, 1]
    ret_list.append(ret)
    mean = np.mean(ret) * freq
    ret_ave.append(mean)
cov = np.matrix(np.cov(ret_list) * freq)
ret_ave = np.array(ret_ave)

# ------------ mean-variance optimization ------------
expected_ret = 0.1
weight = mini_vol(len(tickers), ret_ave.reshape((-1,1)), cov, expected_ret)
result = {}
for i in range(len(tickers)):
    result[tickers[i]] = weight[i].item()

print(result)

# -------------- ploting of mean-variance efficient frontier ------------
port_ret_list = []
port_std_list = []

for i in np.arange(0, 10, 0.01):
    weight = mini_vol(len(tickers), ret_ave.reshape((-1,1)), cov, i)
    port_ret, port_std = portfolio_info(weight, ret_ave, cov)
    port_ret_list.append(port_ret)
    port_std_list.append(port_std)

port_std_list = np.array(port_std_list)
port_ret_list = np.array(port_ret_list)
plt.figure(figsize = (16,9))
plt.scatter(port_std_list, port_ret_list, c = port_ret_list/port_std_list, marker = 'o')
plt.grid(True)
plt.xlabel('excepted volatility')
plt.ylabel('expected return')
plt.colorbar(label = 'Sharpe ratio')   