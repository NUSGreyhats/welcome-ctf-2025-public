#!/usr/bin/python3

from hashlib import sha256
import hmac
import secrets
import json
import os
import sys
import struct


class ChaCha_Hmac256(object):

    """Pure python implementation of ChaCha cipher"""

    constants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

    @staticmethod
    def rotl32(v, c):
        """Rotate left a 32 bit integer v by c bits"""
        return ((v << c) & 0xffffffff) | (v >> (32 - c))

    @staticmethod
    def quarter_round(x, a, b, c, d):
        """Perform a ChaCha quarter round"""
        xa = x[a]
        xb = x[b]
        xc = x[c]
        xd = x[d]

        xa = (xa + xb) & 0xffffffff
        xd = xd ^ xa
        xd = ((xd << 16) & 0xffffffff | (xd >> 16))

        xc = (xc + xd) & 0xffffffff
        xb = xb ^ xc
        xb = ((xb << 12) & 0xffffffff | (xb >> 20))

        xa = (xa + xb) & 0xffffffff
        xd = xd ^ xa
        xd = ((xd << 8) & 0xffffffff | (xd >> 24))

        xc = (xc + xd) & 0xffffffff
        xb = xb ^ xc
        xb = ((xb << 7) & 0xffffffff | (xb >> 25))

        x[a] = xa
        x[b] = xb
        x[c] = xc
        x[d] = xd

    _round_mixup_box = [(0, 4, 8, 12),
                        (1, 5, 9, 13),
                        (2, 6, 10, 14),
                        (3, 7, 11, 15),
                        (0, 5, 10, 15),
                        (1, 6, 11, 12),
                        (2, 7, 8, 13),
                        (3, 4, 9, 14)]

    @classmethod
    def double_round(cls, x):
        """Perform two rounds of ChaCha cipher"""
        for a, b, c, d in cls._round_mixup_box:
            xa = x[a]
            xb = x[b]
            xc = x[c]
            xd = x[d]

            xa = (xa + xb) & 0xffffffff
            xd = xd ^ xa
            xd = ((xd << 16) & 0xffffffff | (xd >> 16))

            xc = (xc + xd) & 0xffffffff
            xb = xb ^ xc
            xb = ((xb << 12) & 0xffffffff | (xb >> 20))

            xa = (xa + xb) & 0xffffffff
            xd = xd ^ xa
            xd = ((xd << 8) & 0xffffffff | (xd >> 24))

            xc = (xc + xd) & 0xffffffff
            xb = xb ^ xc
            xb = ((xb << 7) & 0xffffffff | (xb >> 25))

            x[a] = xa
            x[b] = xb
            x[c] = xc
            x[d] = xd

    @staticmethod
    def chacha_block(key, counter, nonce, rounds):
        """Generate a state of a single block"""
        state = ChaCha_Hmac256.constants + key + [counter] + nonce

        working_state = state[:]
        dbl_round = ChaCha_Hmac256.double_round
        for _ in range(0, rounds // 2):
            dbl_round(working_state)

        return [(st + wrkSt) & 0xffffffff for st, wrkSt
                in zip(state, working_state)]

    @staticmethod
    def word_to_bytearray(state):
        """Convert state to little endian bytestream"""
        return bytearray(struct.pack('<LLLLLLLLLLLLLLLL', *state))

    @staticmethod
    def _bytearray_to_words(data):
        """Convert a bytearray to array of word sized ints"""
        ret = []
        for i in range(0, len(data)//4):
            ret.extend(struct.unpack('<L',
                                     (data[i*4:(i+1)*4])))
        return ret

    def __init__(self, key, nonce, counter=0, rounds=20):
        """Set the initial state for the ChaCha cipher"""
        self.key_bytes = key
        self.nonce_bytes = nonce
        self.key = []
        self.nonce = []
        self.counter = counter
        self.rounds = rounds

        self.key = ChaCha_Hmac256._bytearray_to_words(key)
        self.nonce = ChaCha_Hmac256._bytearray_to_words(nonce)
        self.key_stream = self.generate_key_stream()

    def encrypt_and_digest(self, p):
        ct = b""
        while True:
            k = self.generate_key_stream()
            r = bytes(x^y for x,y in zip(p, k))
            ct += r
            if len(r) != len(k):
                break
        sig = hmac.new(self.key_bytes, self.nonce_bytes + ct, sha256).digest()
        return ct + sig

    def decrypt_and_verify(self, ciphertext):
        tag = ciphertext[-32:]
        ciphertext = ciphertext[:-32]
        expected_signature = hmac.new(self.key_bytes, self.nonce_bytes + ciphertext, sha256).digest()
        if not hmac.compare_digest(expected_signature, tag):
            return
        pt = b""
        ct = iter(ciphertext)
        while True:
            k = self.generate_key_stream()
            r = bytes(x^y for x,y in zip(k, ct))
            pt += r
            if len(r) != len(k):
                return pt

    def generate_key_stream(self):
        key_stream = ChaCha_Hmac256.chacha_block(self.key,
                                        self.counter,
                                        self.nonce,
                                        self.rounds)
        key_stream = ChaCha_Hmac256.word_to_bytearray(key_stream)
        self.counter += 1
        return key_stream


if __name__ == "__main__":
    key = secrets.token_bytes(32)
    print(key.hex(), file=sys.stderr)
    FLAG = os.environ.get("FLAG")
    assert FLAG, print("Please contact the admins! The flag is empty!")
    print("Welcome to the Bank Kit Systems Token Service (BTS)!")
    print()
    try:
        while True:
            print("Menu:")
            print("1. Request token")
            print("2. Fetch flag")
            print("3. Exit")
            inp = int(input("Enter your choice: "))
            match inp:
                case 1:
                    data_raw = input("Enter json input: ")
                    data = json.loads(data_raw)
                    if "name" not in data:
                        print("Invalid input. 'name' field is required.")
                        exit(1)
                    if data["name"] == "admin":
                        print("Cannot issue admin token")
                        exit(1)
                    nonce = secrets.token_bytes(12)
                    token = nonce + ChaCha_Hmac256(key, nonce).encrypt_and_digest(ord(x) for x in data_raw)
                    print("Token:", token.hex())
                case 2:
                    token = input("Enter token: ")
                    token = bytes.fromhex(token)
                    data = ChaCha_Hmac256(key, token[:12]).decrypt_and_verify(token[12:])
                    if data is None:
                        print("Token validation failed!")
                        exit(1)
                    print(data, file=sys.stderr)
                    data = json.loads(data.decode())
                    if data.get("name") == "admin":
                        print(FLAG)
                    else:
                        print(f'{data.get("name")} is not allowed to read the flag!')
                    exit(1)
                case 3:
                    print("Exiting...")
                    exit(0)
                case _:
                    print("Invalid choice. Please try again.")
    except Exception as e:
        print("There was an error:", e)