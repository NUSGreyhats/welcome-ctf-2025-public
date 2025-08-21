from Crypto.Cipher import AES
import os

with open("flag.txt", "r") as f:
    FLAG = f.read()


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def enc(pt, key, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    chunks = [pt[16*i:16*i+16] for i in range(len(pt)//16)]
    ct_chunks = []
    for i in range(len(chunks)):
        ct = cipher.encrypt(xor(iv, chunks[i]))
        ct_chunks.append(ct)
        iv = xor(chunks[i], ct)
    return b"".join(ct_chunks)

try:
    while True:
        
        pt = os.urandom(16*10)
        iv = os.urandom(16)
        key = os.urandom(16)

        secret_ct = enc(pt, key, iv)

        print(f"pt_hex = {pt.hex()}")
        print(f"iv_hex = {iv.hex()}")
        
        while True:

            print("""
=== Menu ===
1. Encrypt a pt
2. Enter ct
        """)
            
            option = int(input("Select option: "))
            if option == 1:
                new_iv = bytes.fromhex(input("New iv (hex): "))
                new_pt = bytes.fromhex(input("New pt (hex): "))
                try:
                    if new_iv != iv and new_pt != pt:
                        print(f"ct_hex = {enc(new_pt, key, new_iv).hex()}")
                    else:
                        print("I said clone bthe ciphertext, not to clone bthe pt and bthe iv")
                except:
                    print("Error")

            elif option == 2:
                guess = bytes.fromhex(input("What is the bthe ciphertext? (hex): "))
                if guess == secret_ct:
                    print(FLAG)
                    exit()
                else:
                    print("You did not clone bthe ciphertext :(")
except:
    exit()
