from brownie import accounts
from brownie import Contract

def main():
    acct = accounts.load("deployer_account")
    Vault = Contract.from_abi("Curve APY Chaser Vault", "0xfec3d72A822A77ECA327A9178b586fE92e2954b3", [{"name": "Transfer", "inputs": [{"name": "_from", "type": "address", "indexed": True}, {"name": "_to", "type": "address", "indexed": True}, {"name": "_value", "type": "uint256", "indexed": False}], "anonymous": False, "type": "event"}, {"name": "Approval", "inputs": [{"name": "_owner", "type": "address", "indexed": True}, {"name": "_spender", "type": "address", "indexed": True}, {"name": "_value", "type": "uint256", "indexed": False}], "anonymous": False, "type": "event"}, {"stateMutability": "nonpayable", "type": "constructor", "inputs": [{"name": "_name", "type": "string"}, {"name": "_symbol", "type": "string"}, {"name": "_main_pool", "type": "address"}, {"name": "_main_deposit", "type": "address"}, {"name": "_main_pool_coin_count", "type": "uint8"}, {"name": "_main_lp_token", "type": "address"}, {"name": "_is_crypto_pool", "type": "bool"}], "outputs": []}, {"stateMutability": "pure", "type": "function", "name": "decimals", "inputs": [], "outputs": [{"name": "", "type": "uint8"}]}, {"stateMutability": "nonpayable", "type": "function", "name": "transfer", "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "outputs": [{"name": "", "type": "bool"}]}, {"stateMutability": "nonpayable", "type": "function", "name": "transferFrom", "inputs": [{"name": "_from", "type": "address"}, {"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "outputs": [{"name": "", "type": "bool"}]}, {"stateMutability": "nonpayable", "type": "function", "name": "approve", "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}], "outputs": [{"name": "", "type": "bool"}]}, {"stateMutability": "nonpayable", "type": "function", "name": "increaseAllowance", "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}], "outputs": [{"name": "", "type": "bool"}]}, {"stateMutability": "nonpayable", "type": "function", "name": "decreaseAllowance", "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}], "outputs": [{"name": "", "type": "bool"}]}, {"stateMutability": "payable", "type": "function", "name": "deposit", "inputs": [{"name": "token_address", "type": "address"}, {"name": "amount", "type": "uint256"}, {"name": "i", "type": "int128"}, {"name": "swap_route", "type": "(address,address,int128,int128,bool,bool,uint256)[]"}], "outputs": []}, {"stateMutability": "payable", "type": "function", "name": "withdraw", "inputs": [{"name": "token_address", "type": "address"}, {"name": "amount", "type": "uint256"}, {"name": "i", "type": "int128"}, {"name": "swap_route", "type": "(address,address,int128,int128,bool,bool,uint256)[]"}], "outputs": []}, {"stateMutability": "nonpayable", "type": "function", "name": "update_pool", "inputs": [{"name": "_out_token", "type": "address"}, {"name": "old_i", "type": "int128"}, {"name": "swap_route", "type": "(address,address,int128,int128,bool,bool,uint256)[]"}, {"name": "new_pool", "type": "address"}, {"name": "new_deposit", "type": "address"}, {"name": "new_i", "type": "int128"}, {"name": "new_pool_coin_count", "type": "uint8"}, {"name": "new_lp_token", "type": "address"}, {"name": "new_is_crypto_pool", "type": "bool"}], "outputs": []}, {"stateMutability": "nonpayable", "type": "function", "name": "make_fee", "inputs": [{"name": "amount", "type": "uint256"}], "outputs": []}, {
                              "stateMutability": "nonpayable", "type": "function", "name": "transfer_admin", "inputs": [{"name": "_admin", "type": "address"}], "outputs": []}, {"stateMutability": "nonpayable", "type": "function", "name": "set_validator", "inputs": [{"name": "_validator", "type": "address"}, {"name": "_value", "type": "bool"}], "outputs": []}, {"stateMutability": "payable", "type": "fallback"}, {"stateMutability": "nonpayable", "type": "function", "name": "set_main_pool", "inputs": [{"name": "_new_pool", "type": "address"}], "outputs": []}, {"stateMutability": "nonpayable", "type": "function", "name": "set_main_deposit", "inputs": [{"name": "_new_deposit", "type": "address"}], "outputs": []}, {"stateMutability": "nonpayable", "type": "function", "name": "set_main_pool_coin_count", "inputs": [{"name": "_new_main_pool_coin_count", "type": "uint8"}], "outputs": []}, {"stateMutability": "nonpayable", "type": "function", "name": "set_is_crypto_pool", "inputs": [{"name": "_new_is_crypto_pool", "type": "bool"}], "outputs": []}, {"stateMutability": "nonpayable", "type": "function", "name": "set_main_lp_token", "inputs": [{"name": "_new_main_lp_token", "type": "address"}], "outputs": []}, {"stateMutability": "nonpayable", "type": "function", "name": "set_zap_deposit", "inputs": [{"name": "_new_zap_deposit", "type": "address"}], "outputs": []}, {"stateMutability": "nonpayable", "type": "function", "name": "pause", "inputs": [{"name": "_paused", "type": "bool"}], "outputs": []}, {"stateMutability": "view", "type": "function", "name": "name", "inputs": [], "outputs": [{"name": "", "type": "string"}]}, {"stateMutability": "view", "type": "function", "name": "symbol", "inputs": [], "outputs": [{"name": "", "type": "string"}]}, {"stateMutability": "view", "type": "function", "name": "balanceOf", "inputs": [{"name": "arg0", "type": "address"}], "outputs": [{"name": "", "type": "uint256"}]}, {"stateMutability": "view", "type": "function", "name": "allowance", "inputs": [{"name": "arg0", "type": "address"}, {"name": "arg1", "type": "address"}], "outputs": [{"name": "", "type": "uint256"}]}, {"stateMutability": "view", "type": "function", "name": "totalSupply", "inputs": [], "outputs": [{"name": "", "type": "uint256"}]}, {"stateMutability": "view", "type": "function", "name": "paused", "inputs": [], "outputs": [{"name": "", "type": "bool"}]}, {"stateMutability": "view", "type": "function", "name": "main_pool", "inputs": [], "outputs": [{"name": "", "type": "address"}]}, {"stateMutability": "view", "type": "function", "name": "main_pool_coin_count", "inputs": [], "outputs": [{"name": "", "type": "uint8"}]}, {"stateMutability": "view", "type": "function", "name": "is_crypto_pool", "inputs": [], "outputs": [{"name": "", "type": "bool"}]}, {"stateMutability": "view", "type": "function", "name": "main_deposit", "inputs": [], "outputs": [{"name": "", "type": "address"}]}, {"stateMutability": "view", "type": "function", "name": "main_lp_token", "inputs": [], "outputs": [{"name": "", "type": "address"}]}, {"stateMutability": "view", "type": "function", "name": "validators", "inputs": [{"name": "arg0", "type": "address"}], "outputs": [{"name": "", "type": "bool"}]}, {"stateMutability": "view", "type": "function", "name": "admin", "inputs": [], "outputs": [{"name": "", "type": "address"}]}, {"stateMutability": "view", "type": "function", "name": "zap_deposit", "inputs": [], "outputs": [{"name": "", "type": "address"}]}])
    withdraw_token = ""
    token_index = 0
    swap_route = []
    main_pool = ""
    main_deposit = ""
    deposit_token_index = 0
    main_coin_count = 0
    lp_token = ""
    is_crypto = False
    Vault.update_pool(withdraw_token, token_index, swap_route, main_pool, main_deposit, deposit_token_index, main_coin_count, lp_token, is_crypto, {"from": acct})