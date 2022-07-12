#!/usr/bin/python3

import pytest, brownie

from conftest import *

def test_deploy(Vault):
    assert Vault.main_pool() == TRIPOOL_INFO[0]
    assert Vault.main_deposit() == TRIPOOL_INFO[1]
    assert Vault.name() == "Curve APY Vault"
    assert Vault.symbol() == "CAV"
    assert Vault.main_pool() == TRIPOOL_INFO[0]
    assert Vault.main_deposit() == TRIPOOL_INFO[1]
    assert Vault.main_pool_coin_count() == 3
    assert Vault.main_lp_token() == TRIPOOL_INFO[2]
    assert Vault.main_liquidity_gauge() == TRIPOOL_INFO[3]
    assert Vault.is_crypto_pool() == False