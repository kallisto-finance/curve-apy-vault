#!/usr/bin/python3

import pytest, brownie

from conftest import *

def test_simple_update_0(Vault, WETH, USDT):
    min_amount = 1
    Vault.deposit(VETH, 10 ** 18, 2, [[WETH, WETH, 0, 1, False, False], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0], "value": 10 ** 18})
    Vault.update_pool(USDT, 2, [], TRICRYPTO2_INFO[0], TRICRYPTO2_INFO[1], 0, 3, TRICRYPTO2_INFO[2], True, 0)
    print(Vault.balanceOf(accounts[0]))

def test_simple_update_1(Vault, WETH, USDT):
    min_amount = 1
    Vault.deposit(VETH, 10 ** 18, 2, [[WETH, WETH, 0, 1, False, False], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0], "value": 10 ** 18})
    Vault.update_pool(USDT, 2, [], USDP_INFO[0], USDP_INFO[1], 3, 4, USDP_INFO[2], False, 0)
    print(Vault.balanceOf(accounts[0]))
    Vault.deposit(VETH, 10 ** 18, 3, [[WETH, WETH, 0, 1, False, False], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0], "value": 10 ** 18})
    bal = Vault.balanceOf(accounts[0])
    Vault.withdraw(USDT, bal, 3, [], min_amount, {"from": accounts[0]})
    print(USDT.balanceOf(accounts[0]))