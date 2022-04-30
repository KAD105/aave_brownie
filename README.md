What does this contract do?

1-First, Swap eth to weth => done in get_weth.py
2-Second, we have to deposit some eth (after swaping became weth) into AAVE as collateral
3-Then, we want to borrow some asset(for example Dai) with the Eth collateral
4-And at the end, we want to pay everything back

For testing:

Integration test: Kovan
Unit test: mainnet-fork
