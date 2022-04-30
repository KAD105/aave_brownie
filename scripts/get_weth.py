from scripts.helpful_scripts import get_account
from brownie import interface, config, network


def main():
    get_weth()


def get_weth():
    account = get_account()
    # Here we don't use get_contract, because we don't deploy mock
    # so we only work with Kovan or miannet-fork
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10 ** 18})
    tx.wait(1)
    print("received 0.1 weth!")
