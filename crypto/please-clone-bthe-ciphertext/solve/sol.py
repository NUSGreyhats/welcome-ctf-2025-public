from pwn import remote, process
import os, sys

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

local = False

io = remote("challs.nusgreyhats.org", 31410) if not local else process([sys.executable, "./chall_pcbc.py"])

msg = io.recvline_contains(b"hex").decode().strip().split("= ")[1]
msg = bytes.fromhex(msg)

iv = io.recvline_contains(b"hex").decode().strip().split("= ")[1]
iv = bytes.fromhex(iv)

new_iv = os.urandom(16)

msg_chunks = [msg[16*i:16*i+16] for i in range(len(msg)//16)]

diff = xor(iv, new_iv)

new_msg = b"".join(xor(i, diff) for i in msg_chunks)

io.sendlineafter(b": ", "1".encode())
io.sendlineafter(b": ", new_iv.hex())
io.sendlineafter(b": ", new_msg.hex())

ct_hex = io.recvline_contains(b"hex").decode().strip().split("= ")[1]

io.sendlineafter(b": ", "2".encode())
io.sendlineafter(b": ", ct_hex.encode())


flag = io.recvline().decode()

print(flag)