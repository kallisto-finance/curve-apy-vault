#!/usr/bin/python3

import pytest, brownie

from conftest import *

def test_transfer(Vault, UniswapV3Router, WETH, USDC, USDT):
    UniswapV3Router.exactOutputSingle([WETH, USDC, 3000, accounts[0], 2**256 - 1, 1000 * 10**6, 10**18, 0], {"from": accounts[0], "value": 10**18})
    USDC.approve(Vault, 1000 * 10**6, {"from": accounts[0]})
    min_amount = 1
    Vault.deposit(USDC, 1000 * 10**6, 2, [], min_amount, {"from": accounts[0]})
    bal = Vault.balanceOf(accounts[0])
    Vault.transfer(accounts[1], bal, {"from": accounts[0]})
    assert bal == Vault.balanceOf(accounts[1])
    Vault.withdraw(USDT, bal, 3, [], min_amount, {"from": accounts[1]})
    assert Vault.balanceOf(accounts[1]) == 0
    assert Vault.balanceOf(accounts[0]) == 0

def test_approve(Vault, UniswapV3Router, WETH, USDC, USDT):
    UniswapV3Router.exactOutputSingle([WETH, USDC, 3000, accounts[0], 2**256 - 1, 1000 * 10**6, 10**18, 0], {"from": accounts[0], "value": 10**18})
    USDC.approve(Vault, 1000 * 10**6, {"from": accounts[0]})
    min_amount = 1
    Vault.deposit(USDC, 1000 * 10**6, 2, [], min_amount, {"from": accounts[0]})
    bal = Vault.balanceOf(accounts[0])
    with brownie.reverts():
        Vault.transferFrom(accounts[0], accounts[1], bal, {"from": accounts[1]})
    Vault.approve(accounts[1], bal, {"from": accounts[0]})
    Vault.transferFrom(accounts[0], accounts[1], bal, {"from": accounts[1]})
    assert bal == Vault.balanceOf(accounts[1])
    Vault.withdraw(USDT, bal, 3, [], min_amount, {"from": accounts[1]})
    assert Vault.balanceOf(accounts[1]) == 0
    assert Vault.balanceOf(accounts[0]) == 0