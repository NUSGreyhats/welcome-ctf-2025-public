#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_INPUT 128

/* Encrypted flag bytes:
   encryption: enc[i] = (flag[i] ^ 0x5A) + 7
   (so to recover: flag[i] = (enc[i] - 7) ^ 0x5A)
*/
static const unsigned char enc_flag[] = {
    68, 47, 70, 42, 40, 48, 58, 62, 49, 61, 70, 12, 62, 70, 59, 54, 12, 47, 70, 51, 46
};

static const size_t enc_len = sizeof(enc_flag) / sizeof(enc_flag[0]);

void print_menu() {
    puts("\n=== Simple Reverse CTF ===");
    puts("1) Say hello");
    puts("2) Show encrypted bytes");
    puts("3) Try to enter the flag");
    puts("4) Quit");
    printf("\nchoice: ");
}

void say_hello() {
    puts("\nHello, challenger. Good luck!");
}

void show_encrypted_bytes() {
    printf("\nEncrypted bytes (in decimal): ");
    for (size_t i = 0; i < enc_len - 1; ++i) {
        printf("%d, ", enc_flag[i]);
    }
    printf("%d\n", enc_flag[enc_len - 1]);
}

int check_flag(const char *input) {
    size_t in_len = strlen(input);
    if (in_len != enc_len) return 0;

    for (size_t i = 0; i < enc_len; ++i) {
        unsigned char decrypted = (unsigned char)((enc_flag[i] - 7) ^ 0x5A);
        if ((unsigned char)input[i] != decrypted) return 0;
    }
    return 1;
}

int main() {
    char buf[MAX_INPUT];
    int choice;

    while (1) {
        print_menu();
        if (fgets(buf, sizeof(buf), stdin) == NULL) break;
        choice = atoi(buf);

        switch (choice) {
            case 1:
                say_hello();
                break;
            case 2:
                show_encrypted_bytes();
                break;
            case 3:
                printf("\nEnter flag: ");
                if (fgets(buf, sizeof(buf), stdin) == NULL) {
                    puts("Input error.");
                    break;
                }
                // strip newline
                buf[strcspn(buf, "\r\n")] = '\0';
                if (check_flag(buf)) {
                    puts("\nCorrect!");
                    return 0;
                } else {
                    puts("\nNope. Try reversing the binary.");
                }
                break;
            case 4:
                puts("\nBye!");
                return 0;
            default:
                puts("\nInvalid choice.");
        }
    }

    return 0;
}
