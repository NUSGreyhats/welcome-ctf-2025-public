#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void setup() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void vulnerable_function() {
    char buffer[64];
    
    printf("Enter your input: ");
    gets(buffer);
    
    printf("You entered: %s\n", buffer);
}

void print_menu() {
    printf("\n==== Baby RetToLIBC ====\n");
    printf("1. Enter input\n");
    printf("2. Exit\n");
    printf("Choice: ");
}

void leak_address() {
    printf("Leaking puts() address: %p\n", puts);
}

int main() {
    setup();
    
    int choice;
    
    while (1) {
        print_menu();
        scanf("%d", &choice);
        getchar();
        
        switch (choice) {
            case 1:
                vulnerable_function();
                break;
            case 2:
                printf("Goodbye!\n");
                exit(0);
            case 0xdeadbeef:
                // Hidden option to leak address
                leak_address();
                break;
            default:
                printf("Invalid option!\n");
        }
    }
    
    return 0;
}
