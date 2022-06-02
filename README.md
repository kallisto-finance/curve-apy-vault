### Kallisto Curve APY Chaser Vault
This vault chases the highest APY paying pools on Curve in a cost-efficient way. The strategy actively searches for the highest APY low risk pool on Curve and the best opportunity to join the selected pool. 


### External functions
**deposit**
User deposits token into Kallisto vault.
| Key | Type | Description |
| --- | --- | --- |
| token_address | address | Address of deposited token |
| amount | uint256 | deposited amount |
| swap_route |  array | best swap route on Curve |

**withdraw**
User withdraws token from Kallisto Vault


**update_pool**
Switch Kallisto vault position from current Curve pool to new best Curve pool
| Key | Type | Description |
| --- | --- | --- |
| _out_token | address | token to withdraw from current pool|
| swap_route |  array | best swap route on Curve |
| new_pool | address | Address of new Curve pool |

**make_fee**
Apply performance fee on vault earnings
| Key | Type | Description |
| --- | --- | --- |
| amount | uint256 | Fee amount|

**transfer_admin**
Transfer Contract Admin rights
| Key | Type | Description |
| --- | --- | --- |

**Emergency Functions**

**set_main_pool**
Set the current Curve pool
| Key | Type | Description |
| --- | --- | --- |
| _new_pool | address | Address of new Curve pool |

**set_main_deposit**

| Key | Type | Description |
| --- | --- | --- |


**set_main_pool_coin_count**
Set the number of coins included in the current Curve pool
| Key | Type | Description |
| --- | --- | --- |
| _new_main_pool_coin_count | uint8 | Number of coins |


**set_main_lp_token**

| Key | Type | Description |
| --- | --- | --- |
| _new_main_lp_token | address | Token address of

**pause**
Pauses contract
| Key | Type | Description |
| --- | --- | --- |
| _paused | boolean | -


### Internal functions

**swap**
Swap tokens on Curve
| Key | Type | Description |
| --- | --- | --- |
|






Other internal functions are taken from common ERC-20 interfaces.


### Disclaimer
Kallisto does not manage any portfolios. You must make an independent judgment as to whether to add liquidity to portfolios. Users of this repo should familiarize themselves with smart contracts to further consider the risks associated with smart contracts before adding liquidity to any portfolios or deployed smart contract. These smart contracts are non-custodial and come with no warranties. Kallisto does not endorse any pools in any of the smart contracts found in this repo. Kallisto is not giving you investment advice with this software and neither firm has control of your funds. Smart contracts are currently under audit, are alpha, works in progress and are undergoing daily updates that may result in errors or other issues.