#!/usr/bin/python3

import pytest, brownie

from conftest import *

def test_simple_deposit(Vault, UniswapV3Router, WETH, USDC):
    WETH.deposit({"from": accounts[0], "value": 10 ** 18})
    WETH.approve(UniswapV3Router, 10 ** 18, {"from": accounts[0]})
    UniswapV3Router.exactOutputSingle([WETH, USDC, 3000, accounts[0], 2 ** 256 - 1, 1000 * 10 ** 6, 10 ** 18, 0], {"from": accounts[0]})
    USDC.approve(Vault, 1000 * 10 ** 6, {"from": accounts[0]})
    min_amount = 1
    Vault.deposit(USDC, 1000 * 10 ** 6, 1, [], min_amount, {"from": accounts[0]})
    assert Vault.balanceOf(accounts[0]) > 0

def test_deposit_with_single_swap(Vault, WETH, USDT):
    WETH.deposit({"from": accounts[0], "value": 10 ** 18})
    WETH.approve(Vault, 10 ** 18, {"from": accounts[0]})
    min_amount = 0
    Vault.deposit(WETH, 10 ** 18, 2, [[TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0]})
    assert Vault.balanceOf(accounts[0]) > 0

def test_deposit_with_multiple_swap_with_ETH(Vault, WETH, USDT):
    min_amount = 1
    Vault.deposit(VETH, 10 ** 18, 2, [[WETH, WETH, 0, 1, False, False], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0], "value": 10 ** 18})
    assert Vault.balanceOf(accounts[0]) > 0

def test_deposit_with_multiple_swap(Vault, UniswapV3Router, WETH, USDT, CRV):
    WETH.deposit({"from": accounts[0], "value": 2 * 10 ** 18})
    WETH.approve(UniswapV3Router, 2 * 10 ** 18, {"from": accounts[0]})
    UniswapV3Router.exactOutputSingle([WETH, CRV, 3000, accounts[0], 2 ** 256 - 1, 1000 * 10 ** 18, 2 * 10 ** 18, 0], {"from": accounts[0]})
    CRV.approve(Vault, 1000 * 10 ** 18, {"from": accounts[0]})
    min_amount = 1
    Vault.deposit(CRV, 1000 * 10 ** 18, 2, [[CRVETH_INFO[0], WETH, 1, 0, False, True], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], min_amount, {"from": accounts[0]})
    assert Vault.balanceOf(accounts[0]) > 0
