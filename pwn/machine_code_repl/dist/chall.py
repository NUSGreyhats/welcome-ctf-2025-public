#!/usr/bin/python3

import sys
import os
try:
    from unicorn import *
    from unicorn.x86_const import *
    from keystone import *
except ImportError as e:
    print(f"Missing required libraries: {e}")
    print("Install with: pip install unicorn keystone-engine")
    sys.exit(1)

class FileDescriptor:
    """Represents an open file descriptor"""
    def __init__(self, fd_num, filepath, flags, mode, file_obj=None):
        self.fd_num = fd_num
        self.filepath = filepath
        self.flags = flags
        self.mode = mode
        self.file_obj = file_obj  # Python file object for actual I/O
        self.position = 0  # Current position in file

class X64AssemblyREPL:
    def __init__(self):
        # Initialize Unicorn Engine for x64 emulation
        self.mu = Uc(UC_ARCH_X86, UC_MODE_64)

        # Initialize Keystone assembler for x64
        self.ks = Ks(KS_ARCH_X86, KS_MODE_64)

        # Memory layout
        self.CODE_BASE = 0x400000
        self.CODE_SIZE = 2 * 1024 * 1024  # 2MB for code
        self.STACK_BASE = 0x7fff0000
        self.STACK_SIZE = 1024 * 1024  # 1MB stack
        self.DATA_BASE = 0x600000  # Base for data segment
        self.DATA_SIZE = 1024 * 1024  # 1MB for data

        # Setup memory regions
        self.mu.mem_map(self.CODE_BASE, self.CODE_SIZE)
        self.mu.mem_map(self.STACK_BASE, self.STACK_SIZE)
        self.mu.mem_map(self.DATA_BASE, self.DATA_SIZE)

        # Initialize stack pointer
        self.mu.reg_write(UC_X86_REG_RSP, self.STACK_BASE + self.STACK_SIZE - 0x1000)

        # Current instruction pointer offset
        self.current_offset = 0

        # File descriptor system
        self.open_files = {}  # fd_num -> FileDescriptor
        self.next_fd = 3  # Start from 3 (0,1,2 are stdin,stdout,stderr)
        
        # Pre-populate standard file descriptors
        self.open_files[0] = FileDescriptor(0, "/dev/stdin", 0, 0, sys.stdin)
        self.open_files[1] = FileDescriptor(1, "/dev/stdout", 1, 0, sys.stdout)
        self.open_files[2] = FileDescriptor(2, "/dev/stderr", 1, 0, sys.stderr)

        # Register mappings for display
        self.registers = {
            'RAX': UC_X86_REG_RAX, 'RBX': UC_X86_REG_RBX, 'RCX': UC_X86_REG_RCX, 'RDX': UC_X86_REG_RDX,
            'RSI': UC_X86_REG_RSI, 'RDI': UC_X86_REG_RDI, 'RBP': UC_X86_REG_RBP, 'RSP': UC_X86_REG_RSP,
            'R8':  UC_X86_REG_R8,  'R9':  UC_X86_REG_R9,  'R10': UC_X86_REG_R10, 'R11': UC_X86_REG_R11,
            'R12': UC_X86_REG_R12, 'R13': UC_X86_REG_R13, 'R14': UC_X86_REG_R14, 'R15': UC_X86_REG_R15,
            'RIP': UC_X86_REG_RIP
        }

        # Flag register
        self.flags_reg = UC_X86_REG_EFLAGS

        # Setup syscall hook
        self.mu.hook_add(UC_HOOK_INSN, self.handle_syscall, None, 1, 0, UC_X86_INS_SYSCALL)

    def parse_open_flags(self, flags):
        """Parse open flags to determine access mode"""
        # Linux open flags
        O_RDONLY = 0
        O_WRONLY = 1
        O_RDWR = 2
        O_CREAT = 0o100
        O_EXCL = 0o200
        O_TRUNC = 0o1000
        O_APPEND = 0o2000
        
        access_mode = flags & 3
        mode_str = ""
        
        if access_mode == O_RDONLY:
            mode_str = "r"
        elif access_mode == O_WRONLY:
            if flags & O_APPEND:
                mode_str = "a"
            else:
                mode_str = "w"
        elif access_mode == O_RDWR:
            if flags & O_APPEND:
                mode_str = "a+"
            else:
                mode_str = "r+" if not (flags & O_TRUNC) else "w+"
        
        # Handle creation flag
        if flags & O_CREAT and 'r' in mode_str and '+' not in mode_str:
            mode_str = "w"
        
        return mode_str, (flags & O_CREAT) != 0, (flags & O_TRUNC) != 0

    def hexdump(self, data, base_addr=0, width=16):
        """Create a hexdump representation of binary data"""
        lines = []
        for i in range(0, len(data), width):
            chunk = data[i:i+width]
            addr = base_addr + i
            hex_str = ' '.join(f'{b:02x}' for b in chunk)
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            lines.append(f'{addr:08x}  {hex_str:<{width*3-1}} |{ascii_str}|')
        return '\n'.join(lines)

    def print_stack(self, num_bytes=0x30):
        """Print stack contents in hexdump format"""
        try:
            rsp = self.mu.reg_read(UC_X86_REG_RSP)
            stack_data = self.mu.mem_read(rsp, num_bytes)
            print(f"\nSTACK (top {num_bytes:#x} bytes from RSP={rsp:#x}):")
            print("-" * 60)
            print(self.hexdump(stack_data, rsp))
            print("-" * 60)
        except Exception as e:
            print(f"Error reading stack: {e}")

    def print_open_files(self):
        """Print currently open file descriptors"""
        print("\nOPEN FILE DESCRIPTORS:")
        print("-" * 60)
        if not self.open_files:
            print("No open files")
        else:
            for fd_num, fd_obj in self.open_files.items():
                status = "open" if fd_obj.file_obj and not fd_obj.file_obj.closed else "closed"
                print(f"FD {fd_num}: {fd_obj.filepath} (flags: {fd_obj.flags:o}, {status})")
        print("-" * 60)

    def handle_syscall(self, uc, user_data):
        """Handle syscall instructions"""
        # Get syscall number from RAX
        syscall_num = uc.reg_read(UC_X86_REG_RAX)
        
        # Common syscall arguments (Linux x64 calling convention)
        rdi = uc.reg_read(UC_X86_REG_RDI)  # arg1
        rsi = uc.reg_read(UC_X86_REG_RSI)  # arg2
        rdx = uc.reg_read(UC_X86_REG_RDX)  # arg3
        r10 = uc.reg_read(UC_X86_REG_R10)  # arg4
        r8 = uc.reg_read(UC_X86_REG_R8)    # arg5
        r9 = uc.reg_read(UC_X86_REG_R9)    # arg6

        print(f"\n[SYSCALL] Number: {syscall_num} (0x{syscall_num:x})")
        print(f"  RDI (arg1): {rdi} (0x{rdi:x})")
        print(f"  RSI (arg2): {rsi} (0x{rsi:x})")
        print(f"  RDX (arg3): {rdx} (0x{rdx:x})")

        ret_val = 0

        # Handle common syscalls
        if syscall_num == 1:  # sys_write
            fd = rdi
            try:
                if fd in self.open_files:
                    fd_obj = self.open_files[fd]
                    if rsi != 0:  # Check if address is valid
                        length = rdx
                        if length > 0:
                            data = uc.mem_read(rsi, length)
                            
                            if fd_obj.file_obj:
                                if fd == 1:  # stdout
                                    print(f"[WRITE to stdout]: ", end='')
                                    sys.stdout.write(data.decode('utf-8', errors='replace'))
                                    sys.stdout.flush()
                                elif fd == 2:  # stderr
                                    print(f"[WRITE to stderr]: ", end='', file=sys.stderr)
                                    sys.stderr.write(data.decode('utf-8', errors='replace'))
                                    sys.stderr.flush()
                                else:
                                    # Write to actual file
                                    try:
                                        fd_obj.file_obj.write(data.decode('utf-8', errors='replace'))
                                        fd_obj.file_obj.flush()
                                        print(f"[WRITE to {fd_obj.filepath}]: {len(data)} bytes")
                                    except Exception as e:
                                        print(f"[WRITE ERROR]: {e}")
                                        ret_val = -1
                                        
                                if ret_val != -1:
                                    ret_val = length
                            else:
                                ret_val = -1  # Bad file descriptor
                        else:
                            ret_val = 0
                    else:
                        ret_val = -1  # EFAULT
                else:
                    print(f"[WRITE ERROR]: Invalid file descriptor {fd}")
                    ret_val = -1  # EBADF
                    
            except Exception as e:
                print(f"[SYSCALL ERROR]: {e}")
                ret_val = -1

        elif syscall_num == 0:  # sys_read
            fd = rdi
            length = rdx
            print(f"[READ] from fd {fd}, length {length}")
            
            if fd in self.open_files:
                fd_obj = self.open_files[fd]
                try:
                    if fd == 0:  # stdin
                        data = input("[STDIN INPUT]: ").encode('utf-8')[:length]
                    else:
                        # Read from actual file
                        if fd_obj.file_obj and not fd_obj.file_obj.closed:
                            data = fd_obj.file_obj.read(length).encode('utf-8')
                            print(f"[READ from {fd_obj.filepath}]: {len(data)} bytes")
                        else:
                            ret_val = -1  # Bad file descriptor
                            data = b""
                    
                    if ret_val != -1 and rsi != 0:
                        # Write data to memory buffer
                        if len(data) < length:
                            data += b'\0'  # Null terminate if shorter
                        uc.mem_write(rsi, data[:length])
                        ret_val = len(data) if len(data) <= length else length
                        
                except Exception as e:
                    print(f"[READ ERROR]: {e}")
                    ret_val = -1
            else:
                print(f"[READ ERROR]: Invalid file descriptor {fd}")
                ret_val = -1  # EBADF

        elif syscall_num == 2:  # sys_open
            try:
                # Read filename from memory
                filename_bytes = []
                addr = rdi
                while True:
                    byte = uc.mem_read(addr, 1)[0]
                    if byte == 0:
                        break
                    filename_bytes.append(byte)
                    addr += 1
                    if len(filename_bytes) > 4096:  # Prevent infinite loop
                        break
                        
                filename = bytes(filename_bytes).decode('utf-8')
                flags = rsi
                mode = rdx
                
                print(f"[OPEN] file: '{filename}', flags: {flags:o}, mode: {mode:o}")
                
                # Parse flags to determine file mode
                file_mode, create_flag, trunc_flag = self.parse_open_flags(flags)
                
                try:
                    # Open the actual file
                    file_obj = open(filename, file_mode)
                    
                    # Create file descriptor entry
                    fd_num = self.next_fd
                    self.open_files[fd_num] = FileDescriptor(fd_num, filename, flags, mode, file_obj)
                    self.next_fd += 1
                    
                    print(f"[OPEN SUCCESS]: Assigned FD {fd_num}")
                    ret_val = fd_num
                    
                except IOError as e:
                    print(f"[OPEN ERROR]: {e}")
                    ret_val = -1  # ENOENT or other error
                    
            except Exception as e:
                print(f"[SYSCALL ERROR]: {e}")
                ret_val = -1

        elif syscall_num == 3:  # sys_close
            fd = rdi
            print(f"[CLOSE] fd: {fd}")
            
            if fd in self.open_files and fd > 2:  # Don't close stdin/stdout/stderr
                fd_obj = self.open_files[fd]
                try:
                    if fd_obj.file_obj and not fd_obj.file_obj.closed:
                        fd_obj.file_obj.close()
                    del self.open_files[fd]
                    print(f"[CLOSE SUCCESS]: Closed {fd_obj.filepath}")
                    ret_val = 0
                except Exception as e:
                    print(f"[CLOSE ERROR]: {e}")
                    ret_val = -1
            elif fd <= 2:
                print(f"[CLOSE]: Cannot close standard file descriptor {fd}")
                ret_val = 0  # Success but no-op
            else:
                print(f"[CLOSE ERROR]: Invalid file descriptor {fd}")
                ret_val = -1  # EBADF

        elif syscall_num == 60:  # sys_exit
            exit_code = rdi
            print(f"[EXIT] with code: {exit_code}")
            ret_val = 0
            # Don't actually exit, just return

        else:
            print(f"[SYSCALL] Unhandled syscall number: {syscall_num}")
            ret_val = -1  # ENOSYS

        # Set return value in RAX
        uc.reg_write(UC_X86_REG_RAX, ret_val & 0xFFFFFFFFFFFFFFFF)
        print(f"[SYSCALL] Returned: {ret_val} (0x{ret_val & 0xFFFFFFFFFFFFFFFF:x})")

    def print_registers(self):
        """Print current state of all registers"""
        print("\n" + "="*60)
        print("REGISTER STATE:")
        print("="*60)

        # Print general purpose registers in a nice format
        reg_pairs = [
            ('RAX', 'RBX'), ('RCX', 'RDX'),
            ('RSI', 'RDI'), ('RBP', 'RSP'),
            ('R8',  'R9'),  ('R10', 'R11'),
            ('R12', 'R13'), ('R14', 'R15')
        ]

        for reg1, reg2 in reg_pairs:
            val1 = self.mu.reg_read(self.registers[reg1])
            val2 = self.mu.reg_read(self.registers[reg2])
            print(f"{reg1:<3}: 0x{val1:016x} ({val1:>20})  |  {reg2:<3}: 0x{val2:016x} ({val2:>20})")

        # Print instruction pointer
        rip = self.mu.reg_read(UC_X86_REG_RIP)
        print(f"RIP: 0x{rip:016x} ({rip:>20})")

        # Print flags register
        flags = self.mu.reg_read(self.flags_reg)
        print(f"\nFLAGS: 0x{flags:08x}")
        self.print_flags(flags)
        print("="*60)

    def print_flags(self, flags):
        """Print individual CPU flags"""
        flag_bits = {
            'CF': (flags >> 0) & 1,   # Carry Flag
            'PF': (flags >> 2) & 1,   # Parity Flag
            'AF': (flags >> 4) & 1,   # Auxiliary Carry Flag
            'ZF': (flags >> 6) & 1,   # Zero Flag
            'SF': (flags >> 7) & 1,   # Sign Flag
            'TF': (flags >> 8) & 1,   # Trap Flag
            'IF': (flags >> 9) & 1,   # Interrupt Enable Flag
            'DF': (flags >> 10) & 1,  # Direction Flag
            'OF': (flags >> 11) & 1,  # Overflow Flag
        }

        flag_str = " | ".join([f"{name}={val}" for name, val in flag_bits.items()])
        print(f"Flags: {flag_str}")

    def write_string_to_memory(self, address, string):
        """Helper function to write a null-terminated string to memory"""
        data = string.encode('utf-8') + b'\0'
        self.mu.mem_write(address, data)
        return len(data)

    def assemble_instruction(self, asm_code):
        """Assemble a single instruction"""
        try:
            encoding, count = self.ks.asm(asm_code)
            if not encoding:
                raise Exception("Failed to assemble instruction")
            return bytes(encoding)
        except Exception as e:
            raise Exception(f"Assembly error: {e}")

    def execute_instruction(self, asm_code):
        """Execute a single assembly instruction"""
        try:
            # Assemble the instruction
            machine_code = self.assemble_instruction(asm_code)

            # Write machine code to memory
            code_addr = self.CODE_BASE + self.current_offset
            self.mu.mem_write(code_addr, machine_code)

            # Set instruction pointer
            self.mu.reg_write(UC_X86_REG_RIP, code_addr)

            # Execute the instruction
            self.mu.emu_start(code_addr, code_addr + len(machine_code))

            # Update offset for next instruction
            self.current_offset += len(machine_code)

            return True

        except Exception as e:
            print(f"Execution error: {e}")
            return False

    def reset(self):
        """Reset the emulator state"""
        # Close all open files except standard ones
        for fd, fd_obj in list(self.open_files.items()):
            if fd > 2 and fd_obj.file_obj and not fd_obj.file_obj.closed:
                fd_obj.file_obj.close()
        
        self.mu.close()
        self.__init__()
        print("Emulator state reset.")

    def help(self):
        """Display help information"""
        print("""
x64 Assembly REPL Commands:
---------------------------
- Enter any x64 assembly instruction (e.g., 'mov rax, 42')
- Special commands:
  :help    - Show this help
  :reset   - Reset emulator state
  :regs    - Show current register state
  :stack   - Show top 0x30 bytes of stack
  :files   - Show open file descriptors
  :quit    - Exit the REPL
  """)

    def run_repl(self):
        """Main REPL loop"""
        print("x64 Assembly REPL")
        print("Type ':help' for commands, ':quit' to exit")
        print("-" * 40)

        # Show initial register state
        self.print_registers()
        self.print_stack()
        self.print_open_files()

        while True:
            try:
                # Get user input
                line = input("\nasm> ").strip()

                # Handle empty input
                if not line:
                    continue

                # Handle special commands
                if line.startswith(':'):
                    cmd = line[1:].lower()
                    if cmd == 'quit' or cmd == 'exit':
                        break
                    elif cmd == 'help':
                        self.help()
                        continue
                    elif cmd == 'reset':
                        self.reset()
                        continue
                    elif cmd == 'regs':
                        self.print_registers()
                        continue
                    elif cmd == 'stack':
                        self.print_stack()
                        continue
                    elif cmd == 'files':
                        self.print_open_files()
                        continue
                    else:
                        print(f"Unknown command: {cmd}")
                        continue

                # Execute assembly instruction
                print(f"Executing: {line}")
                if self.execute_instruction(line):
                    self.print_registers()
                    self.print_stack()

            except KeyboardInterrupt:
                print("\nUse ':quit' to exit")
                continue
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")

        # Clean up - close all open files
        for fd, fd_obj in self.open_files.items():
            if fd > 2 and fd_obj.file_obj and not fd_obj.file_obj.closed:
                fd_obj.file_obj.close()

        print("\nGoodbye!")

def main():
    repl = X64AssemblyREPL()
    repl.run_repl()

if __name__ == "__main__":
    main()
