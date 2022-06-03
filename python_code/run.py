from apy_chaser import find_max_apy, get_candidate_pools
import requests

pools1 = requests.get('https://api.curve.fi/api/getPools/ethereum/main').json()
pools2 = requests.get('https://api.curve.fi/api/getPools/ethereum/crypto').json()
pools3 = requests.get('https://api.curve.fi/api/getPools/ethereum/factory').json()
pools4 = requests.get('https://api.curve.fi/api/getPools/ethereum/factory-crypto').json()
apys = requests.get('https://api.curve.fi/api/getApys').json()

candidate_pools = get_candidate_pools(pools1)
candidate_pools.append(get_candidate_pools(pools2))
candidate_pools.append(get_candidate_pools(pools3))
candidate_pools.append(get_candidate_pools(pools4))

#print(candidate_pools)
print(find_max_apy(candidate_pools, apys))
