from brownie import accounts, Contract, curve_apy_vault

def main():
    acct = accounts.load("deployer_account")
    curve_apy_vault.deploy("Curve APY Vault", "CAV", "0x5a6A4D54456819380173272A5E8E9B9904BdF41B", "0xA79828DF1850E8a3A3064576f380D90aECDD3359", 4, "0x5a6A4D54456819380173272A5E8E9B9904BdF41B", False, {"from": acct})
