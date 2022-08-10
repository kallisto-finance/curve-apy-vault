### Kallisto Curve APY Chaser Vault

This vault chases the highest APY paying pools on Curve in a cost-efficient way. The strategy actively searches for the highest APY low risk pool on Curve and the best opportunity to join the selected pool. 


### External functions

#### deposit

User deposits token into Kallisto vault.

| Key | Type | Description |
| --- | --- | --- |
| token_address | address | Address of deposited token |
| amount | uint256 | deposited amount |
| i | int128 | deposit token index of the main pool |
| swap_route | SwapRoute[] | best swap route on Curve |
| min_amount | uint256 | minimum amount of vault balance after deposit |

#### withdraw

User withdraws token from Kallisto Vault

| Key | Type | Description |
| --- | --- | --- |
| token_address | address | withdraw token address |
| amount | uint256 | withdraw vault balance amount (not token amount) |
| i | int128 | withdraw token index of the main pool |
| swap_route | SwapRoute[] | best swap route on Curve |
| min_amount | uint256 | minimum amount of withdrawn token from withdraw |


#### update_pool

Switch Kallisto vault position from current Curve pool to new best Curve pool

| Key | Type | Description |
| --- | --- | --- |
| _out_token | address | token to withdraw from current pool |
| old_i | int128 | withdraw token index of current pool |
| swap_route | SwapRoute[] | best swap route on Curve |
| new_pool | address | Address of new Curve pool |
| new_deposit | address | Address of new Curve deposit contract |
| new_i | int128 | deposit token index of new Curve Pool |
| new_pool_coin_count | uint8 | coin count of new Curve Pool |
| new_lp_token | address | Address of new Curve LP token |
| new_liquidity_gauge | address | Address of new Liquidity Gauge for Curve LP token |
| new_is_crypto_pool | bool | True if new main pool coin index type is uint256 |
| new_lp_min_amount | uint256 | minimum amount of new curve lp token |

#### collect_crv_reward

Collect CRV reward and swap into liquidity

| Key | Type | Description |
| --- | --- | --- |
| swap_route | SwapRoute[] | best swap route on Curve |
| i | int128 | token index of the main pool |
| min_amount | uint256 | minimum amount of lp token |

#### Emergency Functions

#### set_main_pool

Set the current Curve pool

| Key | Type | Description |
| --- | --- | --- |
| _new_pool | address | Address of new Curve pool |

#### set_main_deposit

| Key | Type | Description |
| --- | --- | --- |


#### set_main_pool_coin_count

Set the number of coins included in the current Curve pool

| Key | Type | Description |
| --- | --- | --- |
| _new_main_pool_coin_count | uint8 | Number of coins |


#### set_main_lp_token

| Key | Type | Description |
| --- | --- | --- |
| _new_main_lp_token | address | Token address of

#### pause

Pauses contract

| Key | Type | Description |
| --- | --- | --- |
| _paused | boolean | -


### Struct

#### SwapRoute

| Key | Type | Description |
| --- | --- | --- |
| swap_pool | address | swap pool to use for swap |
| j_token | address | out token address from the pool |
| i | int128 | token index into the pool |
| j | address | swap pool to use for swap |
| is_underlying | bool | true if exchange underlying coins using exchange_underlying() |
| is_crypto_pool | bool | true if token index type is uint256 |


### Disclaimer: Please Read Carefuly

Kallisto does not manage any portfolios. You must make an independent judgment as to whether to add liquidity to portfolios. Users of this repo should familiarize themselves with smart contracts to further consider the risks associated with smart contracts before adding liquidity to any portfolios or deployed smart contract. These smart contracts are non-custodial and come with no warranties. Kallisto does not endorse any pools in any of the smart contracts found in this repo. Kallisto is not giving you investment advice with this software and neither firm has control of your funds. Smart contracts are currently under audit, are alpha, works in progress and are undergoing daily updates that may result in errors or other issues.
