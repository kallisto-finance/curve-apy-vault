#!/usr/bin/python3

import pytest, brownie

from conftest import *

def test_withdraw_in_ETH(Vault, WETH, USDT):
    min_amount = 1
    Vault.deposit(VETH, 10**18, 2, [[WETH, WETH, 0, 1, False, False], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0], "value": 10**18})
    bal = Vault.balanceOf(accounts[0])
    print(bal)
    Vault.withdraw(USDT, bal, 2, [], min_amount, {"from": accounts[0]})
    print(USDT.balanceOf(accounts[0]))

def test_withdraw_with_single_swap(Vault, WETH, USDT):
    min_amount = 1
    Vault.deposit(VETH, 10**18, 2, [[WETH, WETH, 0, 1, False, False], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0], "value": 10**18})
    bal = Vault.balanceOf(accounts[0])
    print(bal)
    ethbal = accounts[0].balance()
    Vault.withdraw(USDT, bal, 2, [[TRICRYPTO2_INFO[0], WETH, 0, 2, False, True], [WETH, VETH, 1, 0, False, False]], min_amount, {"from": accounts[0]})
    print(accounts[0].balance() - ethbal)
