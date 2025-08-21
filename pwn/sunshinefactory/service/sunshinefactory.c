#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

struct checking_struct {
    char canary[8];
    void (*check_fail_fn)(void);
};

struct sunshine {
    void* ptr;
    struct checking_struct* checker;
};

void check_heap_fail() {
    puts("Heap smashing detected!");
    _exit(0);
}

void win() {
    system("/bin/sh");
}

void banner() {
    puts("Choose an option:");
    puts("1. Allocate sunshine");
    puts("2. Free sunshine");
    printf("> ");
}

int main() {
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    char heap_canary[8];
    int fd = open("/dev/urandom", O_RDONLY);
    read(fd, heap_canary, 8);
    struct sunshine* main_sunshine = NULL;
    while (true) {
        banner();
        int option;
        scanf("%d", &option);
        getchar();
        if (option == 1) { 
            printf("Enter sunshine size needed: ");
            ssize_t mem_size_needed;
            scanf("%lu", &mem_size_needed);
            getchar();
            if (mem_size_needed <= 0) {
                puts("Invalid sunshine size requested!");
                continue;
            }
            void* ptr = calloc(1, mem_size_needed);
            struct checking_struct* curchecker = calloc(1, sizeof(struct checking_struct));
            memcpy(curchecker->canary, heap_canary, 8);
            curchecker->check_fail_fn = check_heap_fail;
            struct sunshine* cursunshine = calloc(1, sizeof(struct sunshine));
            cursunshine->ptr = ptr;
            cursunshine->checker = curchecker;
            printf("Enter sunshine content: ");
            read(0, ptr, 0x100);
            puts("Sunshine created!");
            main_sunshine = cursunshine;
        } else if (option == 2) {
            if (main_sunshine == NULL) {
                puts("You need to create a sunshine first!");
                continue;
            }
            if (strncmp(main_sunshine->checker->canary, heap_canary, 8) != 0) {
                main_sunshine->checker->check_fail_fn();
            } else {
                free(main_sunshine->ptr);
                free(main_sunshine->checker);
                free(main_sunshine);
                main_sunshine = NULL;
            }
        } else {
            puts("Invalid choice!");
            continue;
        }
    }
}