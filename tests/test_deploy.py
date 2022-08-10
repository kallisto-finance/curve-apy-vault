#!/usr/bin/python3

import pytest, brownie

from conftest import *

def test_deploy(Vault):
    assert Vault.main_pool() == MIM_INFO[0]
    assert Vault.main_deposit() == MIM_INFO[1]
    assert Vault.name() == "Curve APY Vault"
    assert Vault.symbol() == "CAV"
    assert Vault.main_pool() == MIM_INFO[0]
    assert Vault.main_deposit() == MIM_INFO[1]
    assert Vault.main_pool_coin_count() == 4
    assert Vault.main_lp_token() == MIM_INFO[2]
    assert Vault.main_liquidity_gauge() == MIM_INFO[3]
    assert Vault.is_crypto_pool() == False