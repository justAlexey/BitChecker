import base58
import ecdsa
import hashlib
import binascii
import requests


def check_balance(address):
    addresses = "|".join(address)
    response = requests.get(f"https://blockchain.info/multiaddr?active={addresses}").json()
    return response["addresses"]


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
    for i in range(10):
        wallets.append(generate_address())
        addresses.append(wallets[i]["address"])
    balances = check_balance(addresses)
    for i, address in enumerate(balances):
        balance = address['final_balance']
        print(balance)
        if balance:
            with open("addresses.txt", "a") as file:
                file.write(str(wallets[i]) + "\n")


if __name__ == '__main__':
    main()
