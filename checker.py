import requests
import wallet

import time


class Checker:
    def __init__(self):
        self.wallets = {}
        self.balances = {}
        self._generate_wallets()
        self._check_balances()

    def _generate_wallets(self):
        for i in range(100):
            wall = wallet.Wallet()
            self.wallets[wall.address] = wall.private_key

    def _check_balances(self):
        addresses = "|".join(self.wallets.keys())
        url = f"https://blockchain.info/balance?active={addresses}"

        response = requests.get(url, timeout=20).json()
        for address in response.keys():
            self.balances[address] = response[address]["final_balance"]

    def get_address_list(self):
        return self.wallets.keys()

    def get_total_balance(self):
        total_balance = 0
        for address in self.wallets:
            total_balance += self.balances[address]
        return total_balance

    def get_private_by_address(self, address):
        return self.wallets[address]

    def get_balance_by_address(self, address):
        return self.balances[address]


if __name__ == "__main__":
    start = time.monotonic()
    checker = Checker()
    stop = time.monotonic()
    print(f"time = {stop-start}")
    start = time.monotonic()
    checker._check_balances()
    stop = time.monotonic()
    print(f"time = {stop - start}")
