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


def print_to_file_or_command_line(address, balance, private_key):
    message = f"{address} : {balance / 1e8} BTC : {private_key}"

    if balance:
        print(f"{COLORS.GREEN}[+] " + message + f"{COLORS.RESET}", flush=True)
        with open("results/wallets.txt", "a") as f:
            f.write(f"{message}\n")
    else:
        try:
            with open("results/empty.txt", "r") as f:
                temp = int(f.readline())
        except FileNotFoundError:
            temp = 0
        except ValueError:
            temp = 0
        temp += 1
        with open("results/empty.txt", "w") as f:
            f.write(f"{temp}\n")

        print(f"{COLORS.RED} -{temp}-[-] " + message + f"{COLORS.RESET}", flush=True)


def main():
    counter = -1
    work = 1
    check = checker.Checker()
    check.start_work()
    while work:
        try:
            wall = check.results.get()
            address = list(wall)[0]
            balance = wall[address]["balance"]
            private_key = wall[address]["private_key"]
            print_to_file_or_command_line(address, balance, private_key)
            if counter == 0:
                work = 0
            else:
                if counter > 0:
                    counter -= 1
                else:
                    counter = -1
        except:
            work = 0
    check.stop_work()


if __name__ == '__main__':
    colorama.init()
    make_dir()
    print("Start to mining wallets")
    main()
