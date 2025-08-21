from pwn import *
import hashlib 
context.log_level = 'error'

xor = lambda a,b : bytes(x^y for x,y in zip(a,b))


class Feistel:
    
    def __init__(self, state):
        self.state = state
    
    def round(self):
        l, r = self.state[:16], self.state[16:]
        l = hashlib.md5(l).digest()
        self.state = r + l
        return self.state
    

r = remote("127.0.0.1", 32000)

r.sendlineafter(b">", b"0"*64)
res = bytes.fromhex(r.readline().decode().strip())

cipher = Feistel(res[:32])
blocks = [cipher.round() for i in range(10)]

r.sendlineafter(b">", b"FLAG")
encflag = bytes.fromhex(r.readline().decode().strip())

flag = b""
for i in range(0, len(encflag), 32):
    for b in blocks:
        test = xor(b, encflag[i:i+32])
        if all(chr(x) in string.printable for x in test):
            flag += test

r.close()
print(flag)
