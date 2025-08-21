#include <unistd.h>     // For syscalls like write, read
#include <sys/syscall.h> // For SYS_write, SYS_read (Linux specific)
#include <stddef.h>     // For size_t

#define STDOUT_FILENO 1
#define STDIN_FILENO  0

long _syscall(long syscall_num, long arg1, long arg2, long arg3, long arg4, long arg5, long arg6) {
    long ret;
    asm volatile (
        "syscall"
        : "=a" (ret)                    // Output: RAX (return value) into 'ret'
        : "a" (syscall_num),            // Input: syscall_num into RAX
          "D" (arg1),                   // Input: arg1 into RDI
          "S" (arg2),                   // Input: arg2 into RSI
          "d" (arg3),                   // Input: arg3 into RDX
          "r" (arg4),                   // Input: arg4 into R10 (compiler picks register, then mapped)
          "r" (arg5),                   // Input: arg5 into R8
          "r" (arg6)                    // Input: arg6 into R9
        : "rcx", "r11", "memory"        // Clobbered registers and memory
    );
    return ret;
}

__attribute__((noinline)) size_t _strlen(const char* s) {
    size_t len = 0;
    while (s[len] != '\0') {
        len++;
    }
    return len;
}

__attribute__((noinline)) void _write_str(const char* s) {
    _syscall(SYS_write, STDOUT_FILENO, (long)s, _strlen(s), 0, 0, 0);
}

__attribute__((noinline)) size_t _read_line(char* buffer, size_t max_len) {
    size_t bytes_read = 0;
    char c;
    while (bytes_read < max_len - 1) {
        // Read one byte at a time
        long result = _syscall(SYS_read, STDIN_FILENO, (long)&c, 1, 0, 0, 0);
        if (result <= 0) { // EOF or error
            break;
        }
        if (c == '\n') { // Newline character, stop reading
            break;
        }
        buffer[bytes_read++] = c;
    }
    buffer[bytes_read] = '\0'; // Null-terminate the string
    return bytes_read;
}

volatile const char key[] = "grey{fL?c3_0|H7Ohr5f#lTwlf9T7e+} <-- Fake";

int main();
int checkflag(const char* flag) __attribute__((noinline));
int checkflag_0(const char* flag) __attribute__((noinline));
int checkflag_1(const char* flag) __attribute__((noinline));
int checkflag_2(const char* flag) __attribute__((noinline));
int checkflag_3(const char* flag) __attribute__((noinline));
int checkflag_4(const char* flag) __attribute__((noinline));
int checkflag_5(const char* flag) __attribute__((noinline));
int checkflag_6(const char* flag) __attribute__((noinline));
int checkflag_7(const char* flag) __attribute__((noinline));
int checkflag_8(const char* flag) __attribute__((noinline));
int checkflag_9(const char* flag) __attribute__((noinline));
int checkflag_10(const char* flag) __attribute__((noinline));
int checkflag_11(const char* flag) __attribute__((noinline));
int checkflag_12(const char* flag) __attribute__((noinline));
int checkflag_13(const char* flag) __attribute__((noinline));
int checkflag_14(const char* flag) __attribute__((noinline));
int checkflag_15(const char* flag) __attribute__((noinline));
int checkflag_16(const char* flag) __attribute__((noinline));
int checkflag_17(const char* flag) __attribute__((noinline));
int checkflag_18(const char* flag) __attribute__((noinline));
int checkflag_19(const char* flag) __attribute__((noinline));
int checkflag_20(const char* flag) __attribute__((noinline));
int checkflag_21(const char* flag) __attribute__((noinline));


__attribute__((noinline)) int checkflag(const char* flag) {
    if (_strlen(flag) == 36) {
        return checkflag_0(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_0(const char* flag) {
    if (flag[0] == key[0]) {
        return checkflag_1(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_1(const char* flag) {
    if (flag[1] == key[1]) {
        return checkflag_2(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_2(const char* flag) {
    if (flag[2] == key[2]) {
        return checkflag_3(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_3(const char* flag) {
    if (flag[3] == key[3]) {
        return checkflag_4(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_4(const char* flag) {
    if (flag[4] == key[4]) {
        return checkflag_5(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_5(const char* flag) {
    if (flag[18] == (-(flag[5] == key[5]) & key[6])) {
        return checkflag_6(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_6(const char* flag) {
    if (((flag[10] - 0x13) ^ 0x2b) + 0xa == key[7]) {
        return checkflag_7(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_7(const char* flag) {
    if (((flag[28] + flag[31]) == key[8]) && (flag[28] == key[9])) {
        return checkflag_8(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_8(const char* flag) {
    if (((flag[8] == flag[12]) & 
         (flag[12] == flag[16]) &
         (flag[16] == flag[22]) &
         (flag[22] == flag[25]) &
         (flag[25] == flag[29]) &
         (flag[29] == key[10])) == 1) {
        return checkflag_9(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_9(const char* flag) {
    if (flag[6] == key[11]) {
        return checkflag_10(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_10(const char* flag) {
    if (((flag[14] + flag[9]) == key[12]) && (flag[14] == key[13])) {
        return checkflag_11(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_11(const char* flag) {
    if (flag[23] == (-(flag[13] == key[14]) & key[15])) {
        return checkflag_12(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_12(const char* flag) {
    if (flag[7] == (-(flag[27] == key[16]) & key[17])) {
        return checkflag_13(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_13(const char* flag) {
    if (flag[21] == key[18] && flag[24] == key[19]) {
        return checkflag_14(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_14(const char* flag) {
    if ((flag[32] - 0x2f) == key[20]) {
        return checkflag_15(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_15(const char* flag) {
    if (flag[26] == (-(flag[11] == key[21]) & key[22])) {
        return checkflag_16(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_16(const char* flag) {
    if (flag[33] == (-(flag[30] == key[23]) & key[24])) {
        return checkflag_17(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_17(const char* flag) {
    if (flag[20] == (-(flag[17] == key[25]) & key[26])) {
        return checkflag_18(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_18(const char* flag) {
    if (((flag[34] + 0x3) ^ 0x67) == key[27]) {
        return checkflag_19(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_19(const char* flag) {
    if (flag[15] == (-(flag[13] == key[28]) & key[29])) {
        return checkflag_20(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_20(const char* flag) {
    if (((flag[19] - 0x2e) ^ 0x18) == key[30]) {
        return checkflag_21(flag);
    }
    return 0;
}

__attribute__((noinline)) int checkflag_21(const char* flag) {
    if (flag[35] == key[31]) {
        return 1;
    }
    return 0;
}

void _start() {
    // Call the main function. We don't pass argc/argv here for simplicity,
    // as our main doesn't use them.
    main();

    // Exit the program using a syscall.
    // SYS_exit is the syscall number for exit().
    // The exit code (0 for success) is passed as the first argument.
    _syscall(SYS_exit, 0, 0, 0, 0, 0, 0);
}

int main() {
    char user_flag_buffer[64];

    _write_str("Enter your flag: ");

    _read_line(user_flag_buffer, sizeof(user_flag_buffer));

    // Call the checkFlag function to validate the user's input
    if (checkflag(user_flag_buffer)) {
        _write_str("Congratulations! Flag is correct!\n");
    } else {
        _write_str("Incorrect flag. Try again!\n");
    }

    return 0;
}

// grey{f0r_41l_7He_fLa95_Of_Th3_w0Rl0}