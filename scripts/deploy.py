from brownie import accounts, Contract, curve_apy_vault

def main():
    acct = accounts.load("deployer_account")
    curve_apy_vault.deploy("Curve APY Vault", "CAV", "0xA5407eAE9Ba41422680e2e00537571bcC53efBfD", "0xFCBa3E75865d2d561BE8D220616520c171F12851", 4, "0xC25a3A3b969415c80451098fa907EC722572917F", "0xA90996896660DEcC6E997655E065b23788857849", False, {"from": acct})
