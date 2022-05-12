from brownie import network, config, interface
from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account
from web3 import Web3

amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork-dev"]:
        # 1- Getting weth
        get_weth()
    lending_pool = get_lending_pool()

    # 2-Approving =>
    # spender(the address who use our token) here is lending_pool,
    # but we only need its address
    approve_erc20(lending_pool.address, amount, erc20_address, account)

    # 3-Depositing =>
    # deposit weth into aave, for this we use the deposit function from lendingPool
    # deposit(address asset, uint256 amount, address onBehalfOf, uint16 referralCode)
    print("Depositing weth as collateral!")
    tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited weth as collateral!\n\n")

    # 4-Borrowing =>
    # getting the borrowing data
    print("Here's the borrowing information")
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)

    # 5-Borrowing Dai =>
    # first we need to take the dai to eth conversion rate
    print("Borrowing Dai process started!")
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed_address"]
    )


def get_asset_price(price_feed_address):
    dai_to_eth_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_to_eth_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The latest Dai price based on eth is {converted_latest_price}")
    return float(latest_price)


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        availabel_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    availabel_borrow_eth = Web3.fromWei(availabel_borrow_eth, "ether")
    # Below is the info for the things we did
    print(f"We have {total_collateral_eth} worth of eth deposited.")
    print(f"We have {total_debt_eth} worth of eth borrowed.")
    print(f"We can borrow {availabel_borrow_eth} worth of eth .")
    return (float(availabel_borrow_eth), float(total_debt_eth))


def approve_erc20(spender, amount, erc20_address, account):
    print("Approving ERC20 token!")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("ERC20 token is approved to the spender!\n\n")
    return tx


def get_lending_pool():
    lending_address_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_address_provider"]
    )
    lending_pool_address = lending_address_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
