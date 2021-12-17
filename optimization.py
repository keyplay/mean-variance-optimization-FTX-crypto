import numpy as np

def mini_vol(number, ret_ave, ret_cov, target_ret):
    '''
    calculate weight with volatility minimization
    para - number: scalar, ticker number
    para - ret_ave: vector, average return of all tickers
    para - ret_cov: martix, covariance matrix of all tickers' return
    para - target_ret: scalar, target return
    return - weights: vector, weight of each ticker
    '''
    ret_cov_I = ret_cov.I

    e = np.matrix([1]*number).reshape((-1,1))

    a = float(np.dot(np.dot(ret_ave.T, ret_cov_I), ret_ave))
    b = float(np.dot(np.dot(e.T, ret_cov_I), ret_ave))
    c = float(np.dot(np.dot(e.T, ret_cov_I), e))

    coeff = np.matrix([a,b,b,c]).reshape((2,2))
    coeff_I = coeff.I

    y1 = np.matrix([target_ret, 1]).reshape((-1,1))
    lambda_result = np.dot(coeff_I, y1)
    lambda1 = float(lambda_result[0])
    lambda2 = float(lambda_result[1])

    weights = lambda1 * np.dot(ret_cov_I, ret_ave) + lambda2 * np.dot(ret_cov_I, e)
    
    return weights

def portfolio_info(weights, ret_ave, ret_cov):
    '''
    para - weights: vector, ticker number
    para - ret_ave: vector, average return of all tickers
    para - ret_cov: martix, covariance matrix of all tickers' return
    return - port_return: scalar, portfolio return
    return - port_std: scalar, portfolio standard deviation
    '''
    port_return =  np.dot(weights.T, ret_ave).item()
    port_var = np.dot(np.dot(weights.T, ret_cov), weights).item()
    port_std = np.sqrt(port_var)
    
    return port_return, port_std
