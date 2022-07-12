#!/usr/bin/python3

import pytest, brownie
from brownie.network.state import Chain

from conftest import *

def test_collect_crv_reward(Vault, UniswapV3Router, WETH, USDC, USDT, CRV):
    WETH.deposit({"from": accounts[1], "value": 10**18})
    WETH.approve(UniswapV3Router, 10**18, {"from": accounts[1]})
    UniswapV3Router.exactOutputSingle([WETH, USDC, 3000, accounts[1], 2**256 - 1, 1000 * 10**6, 10**18, 0], {"from": accounts[1]})
    USDC.approve(Vault, 1000 * 10**6, {"from": accounts[1]})
    min_amount = 1
    Vault.deposit(USDC, 1000 * 10**6, 1, [], min_amount, {"from": accounts[1]})
    chain = Chain()
    chain.sleep(10)
    chain.mine()
    bal = Vault.balanceOf(accounts[0]) == 0
    Vault.collect_crv_reward([[CRVETH_INFO[0], WETH, 1, 0, False, True], [TRICRYPTO2_INFO[0], USDT, 2, 0, False, True]], 2, 0, {"from": accounts[0]})
    assert Vault.balanceOf(accounts[0]) > bal