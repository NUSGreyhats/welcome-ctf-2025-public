import random
import hashlib
from Crypto.Util.Padding import pad

xor = lambda a,b : bytes(x^y for x,y in zip(a,b))

class Feistel:
    
    def __init__(self):
        self.state = random.randbytes(32)
    
    def round(self):
        l, r = self.state[:16], self.state[16:]
        l = hashlib.md5(l).digest()
        self.state = r + l
        return self.state

    def encrypt(self, msg):
        msg = pad(msg, 32)
        blocks = [self.round() for i in range(len(msg)//32)]
        random.shuffle(blocks)
        otp = b"".join(blocks)

        return xor(otp, msg)

with open("flag.txt", "r") as f:
    flag = f.read().encode()

cipher = Feistel()


while True:
    user_input = input("> ")
    if user_input == "FLAG":
        print(cipher.encrypt(flag).hex())
    else:
        pt = bytes.fromhex(user_input)
        if (len(pt) < 32):
            print("Message too short.")
            exit(0)
        print(cipher.encrypt(pt).hex())
    

    
