#import datetime, os,time
# pandas as pd
from params import address_to_name, name_to_address, balance_threshold, balance_ratio_threshold



def read_coin_frompool(pool):
    """
    read out the name, total balance, and the balance ratio of each token in a pool
    """
    total_balance = pool['usdTotal']
    
    name_ = ''    
    coin_balances = []
    coin_ratios = []
    
    for coin in pool['coins']:
        name_ += coin['symbol'] + '-'
        try:
            coin_balance_ = coin['usdPrice']*float(coin['poolBalance'])/(10**int(coin['decimals']))
            coin_ratio_ = coin_balance_ / total_balance
            coin_balances.append(coin_balance_)
            coin_ratios.append(coin_ratio_)
            #print(coin['symbol'], coin_ratio_)
        except:
            pass
            #print('balance failed to read')
    return name_, total_balance, coin_balances, coin_ratios

def get_candidate_pools(pools, balance_threshold=balance_threshold, balance_ratio_threshold=balance_ratio_threshold):
    """
    select candidate pools based on the thresholds
    """
    candidate_pools = []

    for pool in pools['data']['poolData']:
        name_, total_balance, coin_balances, coin_ratios = read_coin_frompool(pool)

        #print(name_, total_balance)
        #print('-------------------------------------------------------------')

        if total_balance > balance_threshold and max(coin_ratios) < balance_ratio_threshold:
            candidate_pools.append(pool)
            print(name_, total_balance, pool['address'])
            print('-------------------------------------------------------------')
            
    return candidate_pools

def find_max_apy(candidate_pools, apys, address_to_name=address_to_name, crvapy=True):
    max_apy = -100
    best_pool = ''
    best_pool_address = ''

    for pool in candidate_pools:

        try:
            if type(pool) == list:
                pool = pool[0]

            address_ = pool['address']
            name_ = address_to_name[address_]
            apy_ = float(apys['data'][name_]['baseApy'])
            if crvapy:
                apy_ += float(apys['data'][name_]['crvApy'])
            print(name_, ': is done')

            if apy_ > max_apy :
                max_apy = apy_
                best_pool = name_
                best_pool_address = address_
        except Exception as e:
            print('error: ', e)
            pass
                    
    return best_pool, best_pool_address, max_apy





