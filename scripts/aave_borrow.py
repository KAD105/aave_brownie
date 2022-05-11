from brownie import network, config, interface
from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account
from web3 import Web3

amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork-dev"]:
        get_weth()
    lending_pool = get_lending_pool()

    # spender(the address who use our token) here is lending_pool,
    # but we only need its address
    approve_erc20(lending_pool.address, amount, erc20_address, account)

    # deposit weth into aave, for this we use the deposit function from lendingPool  


def approve_erc20(spender, amount, erc20_address, account):
    print("Approving ERC20 token!")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("ERC20 token is approved to the spender!")
    return tx


def get_lending_pool():
    lending_address_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_address_provider"]
    )
    lending_pool_address = lending_address_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
