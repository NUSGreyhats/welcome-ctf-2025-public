from pwn import *

# p = process(["python3", "chall.py"])
p = remote("localhost", 34509)

p.sendline(b'')

for i in range(1000):
    p.recvuntil(b'PRESS: [')
    p.sendline(p.recv(1))

p.interactive()
