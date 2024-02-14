import requests
import wallet
import threading
import queue
import time
import random


class Checker:
    def __init__(self):
        self.threads_generate_wallets = None
        self.threads_check_balances = None
        self.wallets = queue.Queue(maxsize=10000)
        self.results = queue.Queue()
        self.work = 1

    def generate_wallets(self):
        while self.work:
            try:
                self.wallets.put(wallet.Wallet().get_wallet(), timeout=10)
            except queue.Full as e:
                pass

    def check_balances(self):
        while self.work and not self.wallets.empty():
            try:
                wallets = {}
                for _ in range(100):
                    wall = self.wallets.get()
                    wallets[list(wall)[0]] = wall[list(wall)[0]]["private_key"]
                addresses = "|".join(list(wallets))
                url = f"https://blockchain.info/balance?active={addresses}"
                response = requests.get(url).json()
                for address in list(response):
                    result = {address: {"private_key": wallets[address], "balance": response[address]["final_balance"]}}
                    self.results.put(result)
                time.sleep(random.randint(10, 15))
            except Exception as e:
                print(f"Error worker {e}")

    def start_work(self):
        self.threads_generate_wallets = [threading.Thread(target=self.generate_wallets) for _ in range(10)]
        self.threads_check_balances = [threading.Thread(target=self.check_balances) for _ in range(1)]
        print("Start workers to generate")
        for thread in self.threads_generate_wallets:
            thread.start()
        print("Start workers to check balance")
        for thread in self.threads_check_balances:
            thread.start()

    def stop_work(self):
        self.work = 0
        print("Stop workers to generate")
        for thread in self.threads_generate_wallets:
            thread.join()
        print("Stop workers to check balance")
        for thread in self.threads_check_balances:
            thread.join()


if __name__ == "__main__":
    checker = Checker()
