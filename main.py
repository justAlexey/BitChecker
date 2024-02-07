import base58
import ecdsa
import hashlib
import binascii
import requests

import proxy as proxies
import random


def check_balances(address):
    status = 0
    addresses = "|".join(address)
    response = None
    while status != 200:
        proxy = random.choice(proxies.proxy_list)
        temp = {"http": proxy}
        response = requests.get(f"https://blockchain.info/multiaddr?active={addresses}", proxies=temp)
        if response.status_code == 200:
            status = 200
    return response.json()["addresses"]


def generate_address():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = b'\04' + private_key.get_verifying_key().to_string()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(public_key).digest())
    r = b'\0' + ripemd160.digest()
    checksum = hashlib.sha256(hashlib.sha256(r).digest()).digest()[0:4]
    address = base58.b58encode(r + checksum)
    temp = dict()
    temp["private_key"] = binascii.b2a_hex(private_key.to_string()).decode()
    temp["public_key"] = binascii.b2a_hex(public_key).decode()
    temp["address"] = address.decode()
    return temp


def main():
    wallets = []
    addresses = []
    generated = 0
    while True:
        founded_with_balance = 0
        for i in range(50):
            wallets.append(generate_address())
            addresses.append(wallets[i]["address"])
        balances = check_balances(addresses)
        for i, address in enumerate(balances):
            balance = address['final_balance']
            if balance:
                print(balance)
                founded_with_balance += 1
                with open("addresses.txt", "a") as file:
                    file.write(str(wallets[i]) + "\n")
        generated += 50
        print(f"generated {generated} wallets, {founded_with_balance} with balance")


if __name__ == '__main__':
    proxies.get_proxy_list()
    print("Start to mining wallets")
    main()
