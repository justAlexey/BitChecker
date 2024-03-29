import binascii
import hashlib

import base58
import ecdsa
import random


temp = random.randint(2**32, 2**256)


def _get_random(x):
    global temp
    temp += 1
    return temp.to_bytes(32)


class Wallet:
    def __init__(self):
        self.private_key = self._generate_private_key()
        self.public_key = self._generate_public_key()
        self.address = self._generate_address()

    def _generate_private_key(self):
        self._private_key_binary = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, entropy=_get_random)
        return binascii.b2a_hex(self._private_key_binary.to_string()).decode()

    def _generate_public_key(self):
        self._public_key_binary = b'\04' + self._private_key_binary.get_verifying_key().to_string()
        return binascii.b2a_hex(self._public_key_binary).decode()

    def _generate_address(self):
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(self._public_key_binary).digest())
        r = b'\0' + ripemd160.digest()
        checksum = hashlib.sha256(hashlib.sha256(r).digest()).digest()[0:4]
        self._address_binary = base58.b58encode(r + checksum)
        return self._address_binary.decode()

    def get_wallet(self):
        return {self.address: {"private_key": self.private_key, "balance": 0}}


if __name__ == "__main__":
    wallet = Wallet()
    print(
        f"Generated wallet\nAddress: {wallet.address}\nPublic key: {wallet.public_key}\nPrivate key: {wallet.private_key}\n")
