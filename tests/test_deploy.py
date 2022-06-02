#!/usr/bin/python3

import pytest, brownie

from conftest import *

def test_deploy(Vault):
    assert Vault.main_pool() == TRIPOOL_INFO[0]
    assert Vault.main_deposit() == TRIPOOL_INFO[1]
