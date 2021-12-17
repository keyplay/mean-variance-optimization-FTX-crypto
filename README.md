# Implementation of mean variance optimization with FTX market data connection

## Code
The code is implemented with Python3.7 to create an optimal portfolio using free historical data from the FTX Markets RESTful API.

Extra package:
- numpy
- matplotlib

## File Introduction
#### client.py
This file implements the connection protocol with FTX using RESTful API, including:
1. connection configuration
2. function get_historical_data will return historical data from market

#### optimization.py
This file implementes the mean-variance optimization, which includes:
1. function mini_vol return the weight of portfolio
2. function portfolio_info return the return and standard deviation of portfolio

#### main.py
This file is the main entry of the program. Ticker name, time interval of data, start time and end time of data should be specified.
Weights for each ticker will be printed.
The figure of mean-variance efficient frontier will be plotted.

## Running
running the program by using command:

`> python main.py`
