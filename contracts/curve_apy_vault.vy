# @version 0.3.3

struct SwapRoute:
    mid_token: address
    mid_pool: address
    min_amount: uint256

event Transfer:
    _from: indexed(address)
    _to: indexed(address)
    _value: uint256

event Approval:
    _owner: indexed(address)
    _spender: indexed(address)
    _value: uint256

name: public(String[64])
symbol: public(String[32])

balanceOf: public(HashMap[address, uint256])
allowance: public(HashMap[address, HashMap[address, uint256]])
totalSupply: public(uint256)

main_pool: public(address)
main_deposit: public(address)
main_lp_token: public(address)
main_pool_coin_count: public(uint256)
validators: public(HashMap[address, bool])
admin: public(address)

crv_registry: public(address)
zap_deposit: public(address)
MAX_COINS: constant(int128) = 8
VETH: constant(address) = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
INIT_CRV_REGISTRY: constant(address) = 0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5
IS_A_POOL_IN_DEPOSIT: constant(address) = 0x0000000000000000000000000000000000000001 # use address(1) as deposit address for aave pool

interface CrvRegistry:
    def is_meta(_pool: address) -> bool: view
    def get_lp_token(_pool: address) -> address: view
    def get_n_coins(_pool: address) -> uint256[2]: view
    def get_underlying_coins(_pool: address) -> address[MAX_COINS]: view
    def get_coin_indices(_pool: address, _from: address, _to: address) -> (int128, int128, bool): view

interface CrvPool:
    def coins(i: uint256) -> address: view
    def remove_liquidity_one_coin(token_amount: uint256, i: int128, min_amount: uint256) -> uint256: nonpayable
    def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256) -> uint256: nonpayable
    def exchange_underlying(i: int128, j: int128, dx: uint256, min_dy: uint256) -> uint256: nonpayable

interface CrvAPool:
    def remove_liquidity_one_coin(token_amount: uint256, i: int128, min_amount: uint256, use_underlying: bool) -> uint256: nonpayable

interface CrvZapDeposit:
    def remove_liquidity_one_coin(_pool: address, token_amount: uint256, i: int128, min_amount: uint256) -> uint256: nonpayable

interface CrvDeposit:
    def pool() -> address: view

interface CrvEthPool:
    def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256) -> uint256: payable

interface ERC20:
    def balanceOf(_to: address) -> uint256: view

interface WrappedEth:
    def deposit(): payable
    def withdraw(amount: uint256): nonpayable

@external
def __init__(_name: String[64], _symbol: String[32], _main_pool: address, _main_deposit: address, _is_a_pool: bool):
    self.name = _name
    self.symbol = _symbol
    self.admin = msg.sender
    self.validators[msg.sender] = True
    self.main_pool = _main_pool
    if CrvRegistry(INIT_CRV_REGISTRY).is_meta(_main_pool) and _main_deposit != 0xA79828DF1850E8a3A3064576f380D90aECDD3359:
        assert CrvDeposit(_main_deposit).pool() == _main_pool, "Wrong Deposit Pool"
    else:
        assert _main_deposit == ZERO_ADDRESS or _main_deposit == IS_A_POOL_IN_DEPOSIT, "Wrong Deposit Pool"
    self.main_deposit = _main_deposit
    self.crv_registry = INIT_CRV_REGISTRY
    _main_pool_coin_count: uint256 = CrvRegistry(INIT_CRV_REGISTRY).get_n_coins(_main_pool)[1]
    assert _main_pool_coin_count >= 2 and _main_pool_coin_count <= convert(MAX_COINS, uint256), "Wrong Pool Coin Count"
    self.main_pool_coin_count = _main_pool_coin_count
    _main_lp_token: address = CrvRegistry(INIT_CRV_REGISTRY).get_lp_token(_main_pool)
    assert _main_lp_token != ZERO_ADDRESS, "Wrong Pool"
    self.main_lp_token = _main_lp_token
    self.zap_deposit = 0xA79828DF1850E8a3A3064576f380D90aECDD3359

@internal
def _mint(_to: address, _value: uint256):
    assert _to != ZERO_ADDRESS # dev: zero address
    self.totalSupply += _value
    self.balanceOf[_to] += _value
    log Transfer(ZERO_ADDRESS, _to, _value)

@internal
def _burn(_to: address, _value: uint256):
    assert _to != ZERO_ADDRESS # dev: zero address
    self.totalSupply -= _value
    self.balanceOf[_to] -= _value
    log Transfer(_to, ZERO_ADDRESS, _value)

@internal
def safe_approve(_token: address, _to: address, _value: uint256):
    _response: Bytes[32] = raw_call(
        _token,
        concat(
            method_id("approve(address,uint256)"),
            convert(_to, bytes32),
            convert(_value, bytes32)
        ),
        max_outsize=32
    )  # dev: failed approve
    if len(_response) > 0:
        assert convert(_response, bool) # dev: failed approve

@internal
def safe_transfer(_token: address, _to: address, _value: uint256):
    _response: Bytes[32] = raw_call(
        _token,
        concat(
            method_id("transfer(address,uint256)"),
            convert(_to, bytes32),
            convert(_value, bytes32)
        ),
        max_outsize=32
    )  # dev: failed transfer
    if len(_response) > 0:
        assert convert(_response, bool) # dev: failed transfer

@internal
def safe_transfer_from(_token: address, _from: address, _to: address, _value: uint256):
    _response: Bytes[32] = raw_call(
        _token,
        concat(
            method_id("transferFrom(address,address,uint256)"),
            convert(_from, bytes32),
            convert(_to, bytes32),
            convert(_value, bytes32)
        ),
        max_outsize=32
    )  # dev: failed transfer from
    if len(_response) > 0:
        assert convert(_response, bool) # dev: failed transfer from

@external
@pure
def decimals() -> uint8:
    return 18

@external
def transfer(_to : address, _value : uint256) -> bool:
    assert _to != ZERO_ADDRESS # dev: zero address
    self.balanceOf[msg.sender] -= _value
    self.balanceOf[_to] += _value
    log Transfer(msg.sender, _to, _value)
    return True

@external
def transferFrom(_from : address, _to : address, _value : uint256) -> bool:
    assert _to != ZERO_ADDRESS # dev: zero address
    self.balanceOf[_from] -= _value
    self.balanceOf[_to] += _value
    self.allowance[_from][msg.sender] -= _value
    log Transfer(_from, _to, _value)
    return True

@external
def approve(_spender : address, _value : uint256) -> bool:
    assert _value == 0 or self.allowance[msg.sender][_spender] == 0
    self.allowance[msg.sender][_spender] = _value
    log Approval(msg.sender, _spender, _value)
    return True

@external
def increaseAllowance(_spender: address, _value: uint256) -> bool:
    allowance: uint256 = self.allowance[msg.sender][_spender]
    allowance += _value
    self.allowance[msg.sender][_spender] = allowance
    log Approval(msg.sender, _spender, allowance)
    return True

@external
def decreaseAllowance(_spender: address, _value: uint256) -> bool:
    allowance: uint256 = self.allowance[msg.sender][_spender]
    allowance -= _value
    self.allowance[msg.sender][_spender] = allowance
    log Approval(msg.sender, _spender, allowance)
    return True

@internal
def _deposit(_crv_registry: address, main_pool: address, _main_deposit: address, in_token: address, in_amount: uint256):
    _main_pool: address = main_pool
    coins: address[MAX_COINS] = CrvRegistry(_crv_registry).get_underlying_coins(_main_pool)
    i: int128 = -1
    for k in range(MAX_COINS):
        if in_token == coins[k]:
            i = k
    assert i >= 0, "Wrong Token / Pool"
    _main_pool_coin_count: uint256 = self.main_pool_coin_count
    payload: Bytes[320] = empty(Bytes[320])
    length: uint256 = len(payload)
    if i == 0:
        payload = concat(convert(in_amount, bytes32), EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32)
    elif i == 1:
        payload = concat(EMPTY_BYTES32, convert(in_amount, bytes32), EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32)
    elif i == 2:
        payload = concat(EMPTY_BYTES32, EMPTY_BYTES32, convert(in_amount, bytes32), EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32)
    elif i == 3:
        payload = concat(EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, convert(in_amount, bytes32), EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32)
    elif i == 4:
        payload = concat(EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, convert(in_amount, bytes32), EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32)
    elif i == 5:
        payload = concat(EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, convert(in_amount, bytes32), EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32)
    elif i == 6:
        payload = concat(EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, convert(in_amount, bytes32), EMPTY_BYTES32, EMPTY_BYTES32)
    else:
        payload = concat(EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, EMPTY_BYTES32, convert(in_amount, bytes32), EMPTY_BYTES32)

    m_id: Bytes[4] = empty(Bytes[4])
    if _main_deposit == IS_A_POOL_IN_DEPOSIT:
        true_bytes32: bytes32 = convert(True, bytes32)
        if _main_pool_coin_count == 2:
            m_id = method_id("add_liquidity(uint256[2],uint256,bool)")
            payload = concat(slice(payload, 0, 96), true_bytes32)
        elif _main_pool_coin_count == 3:
            m_id = method_id("add_liquidity(uint256[3],uint256,bool)")
            payload = concat(slice(payload, 0, 128), true_bytes32)
        elif _main_pool_coin_count == 4:
            m_id = method_id("add_liquidity(uint256[4],uint256,bool)")
            payload = concat(slice(payload, 0, 160), true_bytes32)
        elif _main_pool_coin_count == 5:
            m_id = method_id("add_liquidity(uint256[5],uint256,bool)")
            payload = concat(slice(payload, 0, 192), true_bytes32)
        elif _main_pool_coin_count == 6:
            m_id = method_id("add_liquidity(uint256[6],uint256,bool)")
            payload = concat(slice(payload, 0, 224), true_bytes32)
        elif _main_pool_coin_count == 7:
            m_id = method_id("add_liquidity(uint256[7],uint256,bool)")
            payload = concat(slice(payload, 0, 256), true_bytes32)
        else:
            m_id = method_id("add_liquidity(uint256[8],uint256,bool)")
            payload = concat(slice(payload, 0, 288), true_bytes32)
    elif _main_deposit == self.zap_deposit:
        if _main_pool_coin_count == 2:
            m_id = method_id("add_liquidity(address,uint256[2],uint256)")
            payload = concat(convert(_main_pool, bytes32), slice(payload, 0, 96))
        elif _main_pool_coin_count == 3:
            m_id = method_id("add_liquidity(address,uint256[3],uint256)")
            payload = concat(convert(_main_pool, bytes32), slice(payload, 0, 128))
        elif _main_pool_coin_count == 4:
            m_id = method_id("add_liquidity(address,uint256[4],uint256)")
            payload = concat(convert(_main_pool, bytes32), slice(payload, 0, 160))
        elif _main_pool_coin_count == 5:
            m_id = method_id("add_liquidity(address,uint256[5],uint256)")
            payload = concat(convert(_main_pool, bytes32), slice(payload, 0, 192))
        elif _main_pool_coin_count == 6:
            m_id = method_id("add_liquidity(address,uint256[6],uint256)")
            payload = concat(convert(_main_pool, bytes32), slice(payload, 0, 224))
        elif _main_pool_coin_count == 7:
            m_id = method_id("add_liquidity(address,uint256[7],uint256)")
            payload = concat(convert(_main_pool, bytes32), slice(payload, 0, 256))
        else:
            m_id = method_id("add_liquidity(address,uint256[8],uint256)")
            payload = concat(convert(_main_pool, bytes32), slice(payload, 0, 288))
    else:
        if _main_pool_coin_count == 2:
            m_id = method_id("add_liquidity(uint256[2],uint256)")
            payload = slice(payload, 0, 96)
        elif _main_pool_coin_count == 3:
            m_id = method_id("add_liquidity(uint256[3],uint256)")
            payload = slice(payload, 0, 128)
        elif _main_pool_coin_count == 4:
            m_id = method_id("add_liquidity(uint256[4],uint256)")
            payload = slice(payload, 0, 160)
        elif _main_pool_coin_count == 5:
            m_id = method_id("add_liquidity(uint256[5],uint256)")
            payload = slice(payload, 0, 192)
        elif _main_pool_coin_count == 6:
            m_id = method_id("add_liquidity(uint256[6],uint256)")
            payload = slice(payload, 0, 224)
        elif _main_pool_coin_count == 7:
            m_id = method_id("add_liquidity(uint256[7],uint256)")
            payload = slice(payload, 0, 256)
        else:
            m_id = method_id("add_liquidity(uint256[8],uint256)")
            payload = slice(payload, 0, 288)

    if _main_deposit != ZERO_ADDRESS and _main_deposit != IS_A_POOL_IN_DEPOSIT:
        _main_pool = _main_deposit
    if in_token == VETH:
        raw_call(
            _main_pool,
            concat(
                m_id,
                payload
            ),
            value=in_amount
        )
    else:
        self.safe_approve(in_token, _main_pool, in_amount)
        raw_call(
            _main_pool,
            concat(
                m_id,
                payload
            )
        )

@external
@payable
@nonreentrant("lock")
def deposit(token_address: address, amount: uint256, swap_route: SwapRoute):
    self.safe_transfer_from(token_address, msg.sender, self, amount)
    in_token: address = token_address
    in_amount: uint256 = amount
    i: int128 = 0
    j: int128 = 0
    is_underlying: bool = False
    _crv_registry: address = self.crv_registry
    if swap_route.mid_pool != ZERO_ADDRESS:
        in_token = swap_route.mid_token
        i, j, is_underlying = CrvRegistry(_crv_registry).get_coin_indices(swap_route.mid_pool, token_address, swap_route.mid_token)
        if token_address == VETH:
            in_amount = CrvEthPool(swap_route.mid_pool).exchange(i, j, amount, swap_route.min_amount, value=amount)
        else:
            self.safe_approve(token_address, swap_route.mid_token, amount)
            if is_underlying:
                in_amount = CrvPool(swap_route.mid_pool).exchange_underlying(i, j, amount, swap_route.min_amount)
            else:
                in_amount = CrvPool(swap_route.mid_pool).exchange(i, j, amount, swap_route.min_amount)
    _main_lp_token: address = self.main_lp_token
    old_balance: uint256 = ERC20(_main_lp_token).balanceOf(self)
    self._deposit(_crv_registry, self.main_pool, self.main_deposit, in_token, in_amount)
    new_balance: uint256 = ERC20(_main_lp_token).balanceOf(self)
    assert new_balance > old_balance, "Deposit failed"
    total_supply: uint256 = self.totalSupply
    if total_supply == 0:
        self._mint(msg.sender, new_balance)
    else:
        self._mint(msg.sender, (new_balance - old_balance) * total_supply / old_balance)

@external
@payable
@nonreentrant("lock")
def withdraw(token_address: address, amount: uint256, swap_route: SwapRoute):
    self._burn(msg.sender, amount)
    out_token: address = token_address
    lp_token: address = self.main_lp_token
    out_amount: uint256 = amount * ERC20(lp_token).balanceOf(self) / self.totalSupply
    if swap_route.mid_pool != ZERO_ADDRESS:
        out_token = swap_route.mid_token
    i: int128 = -1
    _main_pool: address = self.main_pool
    coins: address[MAX_COINS] = CrvRegistry(self.crv_registry).get_underlying_coins(_main_pool)
    for k in range(MAX_COINS):
        if coins[k] == out_token:
            i = k
    assert i >= 0, "Wrong Token / Pool"
    _main_deposit: address = self.main_deposit
    if _main_deposit == IS_A_POOL_IN_DEPOSIT:
        self.safe_approve(lp_token, _main_pool, out_amount)
        out_amount = CrvAPool(_main_pool).remove_liquidity_one_coin(out_amount, i, 1, True)
    elif _main_deposit == ZERO_ADDRESS:
        self.safe_approve(lp_token, _main_pool, out_amount)
        out_amount = CrvPool(_main_pool).remove_liquidity_one_coin(out_amount, i, 1)
    elif _main_deposit == self.zap_deposit:
        self.safe_approve(lp_token, _main_deposit, out_amount)
        out_amount = CrvZapDeposit(_main_deposit).remove_liquidity_one_coin(_main_pool, out_amount, i, 1)
    else:
        self.safe_approve(lp_token, _main_deposit, out_amount)
        out_amount = CrvPool(_main_deposit).remove_liquidity_one_coin(out_amount, i, 1)
    j: int128 = 0
    is_underlying: bool = False
    _crv_registry: address = self.crv_registry
    if swap_route.mid_pool != ZERO_ADDRESS:
        i, j, is_underlying = CrvRegistry(_crv_registry).get_coin_indices(swap_route.mid_pool, out_token, token_address)
        if out_token == VETH:
            out_amount = CrvEthPool(swap_route.mid_pool).exchange(i, j, out_amount, swap_route.min_amount, value=out_amount)
        else:
            self.safe_approve(out_token, swap_route.mid_token, out_amount)
            if is_underlying:
                out_amount = CrvPool(swap_route.mid_pool).exchange_underlying(i, j, out_amount, swap_route.min_amount)
            else:
                out_amount = CrvPool(swap_route.mid_pool).exchange(i, j, out_amount, swap_route.min_amount)
    if out_token == VETH:
        send(msg.sender, out_amount)
    else:
        self.safe_transfer(out_token, msg.sender, out_amount)

@external
def update_pool(_out_token: address, swap_route: SwapRoute, new_pool: address, new_deposit: address, _is_a_pool: bool):
    assert self.validators[msg.sender], "Not Validator"
    out_token: address = _out_token
    lp_token: address = self.main_lp_token
    out_amount: uint256 = ERC20(lp_token).balanceOf(self)
    i: int128 = -1
    _main_pool: address = self.main_pool
    _crv_registry: address = self.crv_registry
    coins: address[MAX_COINS] = CrvRegistry(_crv_registry).get_underlying_coins(_main_pool)
    for k in range(MAX_COINS):
        if coins[k] == out_token:
            i = k
    assert i >= 0, "Wrong Token / Pool"
    _main_deposit: address = self.main_deposit
    _zap_deposit: address = self.zap_deposit
    if _main_deposit == IS_A_POOL_IN_DEPOSIT:
        self.safe_approve(lp_token, _main_pool, out_amount)
        out_amount = CrvAPool(_main_pool).remove_liquidity_one_coin(out_amount, i, 1, True)
    elif _main_deposit == ZERO_ADDRESS:
        self.safe_approve(lp_token, _main_pool, out_amount)
        out_amount = CrvPool(_main_pool).remove_liquidity_one_coin(out_amount, i, 1)
    elif _main_deposit == _zap_deposit:
        self.safe_approve(lp_token, _main_deposit, out_amount)
        out_amount = CrvZapDeposit(_main_deposit).remove_liquidity_one_coin(_main_pool, out_amount, i, 1)
    else:
        self.safe_approve(lp_token, _main_deposit, out_amount)
        out_amount = CrvPool(_main_deposit).remove_liquidity_one_coin(out_amount, i, 1)
    j: int128 = 0
    is_underlying: bool = False
    if swap_route.mid_pool != ZERO_ADDRESS:
        i, j, is_underlying = CrvRegistry(_crv_registry).get_coin_indices(swap_route.mid_pool, out_token, swap_route.mid_token)
        if out_token == VETH:
            out_amount = CrvEthPool(swap_route.mid_pool).exchange(i, j, out_amount, swap_route.min_amount, value=out_amount)
        else:
            self.safe_approve(out_token, swap_route.mid_token, out_amount)
            if is_underlying:
                out_amount = CrvPool(swap_route.mid_pool).exchange_underlying(i, j, out_amount, swap_route.min_amount)
            else:
                out_amount = CrvPool(swap_route.mid_pool).exchange(i, j, out_amount, swap_route.min_amount)
        out_token = swap_route.mid_token
    self._deposit(_crv_registry, new_pool, new_deposit,  out_token, out_amount)
    if CrvRegistry(_crv_registry).is_meta(new_pool) and new_deposit != _zap_deposit:
        assert CrvDeposit(new_deposit).pool() == new_pool, "Wrong Deposit Pool"
    else:
        assert new_deposit == ZERO_ADDRESS or new_deposit == IS_A_POOL_IN_DEPOSIT, "Wrong Deposit Pool"
    self.main_pool = new_pool
    self.main_deposit = new_deposit
    _main_pool_coin_count: uint256 = CrvRegistry(_crv_registry).get_n_coins(new_pool)[1]
    assert _main_pool_coin_count >= 2 and _main_pool_coin_count <= convert(MAX_COINS, uint256), "Wrong Pool Coin Count"
    self.main_pool_coin_count = _main_pool_coin_count
    _main_lp_token: address = CrvRegistry(_crv_registry).get_lp_token(_main_pool)
    assert _main_lp_token != ZERO_ADDRESS, "Wrong Pool"
    self.main_lp_token = _main_lp_token

@external
def make_fee(amount: uint256):
    assert msg.sender == self.admin
    self._mint(msg.sender, amount)

@external
def update_zap_deposit(_new_zap_deposit: address):
    assert msg.sender == self.admin
    self.zap_deposit = _new_zap_deposit

@external
def transfer_admin(_admin: address):
    assert msg.sender == self.admin and _admin != ZERO_ADDRESS
    self.admin = _admin

@external
def set_validator(_validator: address, _value: bool):
    assert msg.sender == self.admin
    self.validators[_validator] = _value

@external
@payable
def __default__():
    pass