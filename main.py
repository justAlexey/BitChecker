import checker
import colorama
import os


class COLORS:
    GREEN = "\033[92m"  # GREEN
    YELLOW = "\033[93m"  # YELLOW
    RED = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR


def make_dir():
    path = "results"
    if not os.path.exists(path):
        os.makedirs(path)


def main():
    for _ in range(1):
        check = checker.Checker()
        for address in check.get_address_list():
            if check.get_balance_by_address(address):
                message = f"{COLORS.GREEN}[+] {address} : {float(check.get_balance_by_address(address)) / 1e8} BTC : {check.get_private_by_address(address)}"
                print(message, flush=True)
                with open("results/wallets.txt", "a") as f:
                    f.write(
                        f"{address} : {float(check.get_balance_by_address(address)) / 1e8} BTC : {check.get_private_by_address(address)}\n"
                    )
            else:
                message = f"{COLORS.RED}[-] {address} : {float(check.get_balance_by_address(address)) / 1e8} BTC : {check.get_private_by_address(address)}"
                print(message, flush=True)
                with open("results/empty.txt", "a") as f:
                    f.write(
                        f"{address} : {float(check.get_balance_by_address(address)) / 1e8} BTC : {check.get_private_by_address(address)}\n"
                    )


if __name__ == '__main__':
    colorama.init()
    make_dir()
    print("Start to mining wallets")
    main()
