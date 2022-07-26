#!/usr/bin/python3

import pytest, brownie

from conftest import *

def test_simple_update_crypto(Vault, WETH, USDT):
    min_amount = 1
    Vault.deposit(VETH, 10**18, 2, [[WETH, WETH, 0, 1, False, False], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0], "value": 10**18})
    Vault.update_pool(USDT, 2, [], TRICRYPTO2_INFO[0], TRICRYPTO2_INFO[1], 0, 3, TRICRYPTO2_INFO[2], TRICRYPTO2_INFO[3], True, 0, 2**256 - 1, {"from": accounts[0]})
    print(Vault.balanceOf(accounts[0]))

def test_simple_update_usd_pool(Vault, WETH, USDT):
    min_amount = 1
    Vault.deposit(VETH, 10**18, 2, [[WETH, WETH, 0, 1, False, False], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0], "value": 10**18})
    Vault.update_pool(USDT, 2, [], USDP_INFO[0], USDP_INFO[1], 3, 4, USDP_INFO[2], USDP_INFO[3], False, 0, 2**256 - 1)
    print(Vault.balanceOf(accounts[0]))
    Vault.deposit(VETH, 10**18, 3, [[WETH, WETH, 0, 1, False, False], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0], "value": 10**18})
    bal = Vault.balanceOf(accounts[0])
    Vault.withdraw(USDT, bal, 3, [], min_amount, {"from": accounts[0]})
    print(USDT.balanceOf(accounts[0]))

def test_simple_update_aave(Vault, WETH, USDT):
    min_amount = 1
    Vault.deposit(VETH, 10**18, 2, [[WETH, WETH, 0, 1, False, False], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0], "value": 10**18})
    Vault.update_pool(USDT, 2, [], AAVE_INFO[0], AAVE_INFO[1], 2, 3, AAVE_INFO[2], AAVE_INFO[3], False, 0, 2**256 - 1, {"from": accounts[0]})
    print(Vault.balanceOf(accounts[0]))
    Vault.deposit(VETH, 10**18, 2, [[WETH, WETH, 0, 1, False, False], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0], "value": 10**18})
