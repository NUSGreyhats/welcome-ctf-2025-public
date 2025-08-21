#include <stdio.h>

void wrong_item() {
    printf("error: wrong item in the bag!\n");
}

int main() {
    FILE* file = fopen("bag.txt", "r");
    if (file == NULL) {
        printf("error: you need a bag!\n");
        return 1;
    }
    
    char contents[7];
    fread(contents, sizeof(char), 7, file);
    //printf("%s", contents);
    
    if (contents[1] != 'r') {
        wrong_item();
        return 1;
    }
    
    if (contents[5] != 'a') {
        wrong_item();
        return 1;
    }
    
    if (contents[3] != 'y') {
        wrong_item();
        return 1;
    }
    
    if (contents[2] != 'e') {
        wrong_item();
        return 1;
    }
    
    if (contents[4] != 'c') {
        wrong_item();
        return 1;
    }
    
    if (contents[0] != 'g') {
        wrong_item();
        return 1;
    }
    
    if (contents[6] != 't') {
        wrong_item();
        return 1;
    }
    
    int sum = 0;
    for (int i = 0; i < 7; i++) {
        sum += contents[i];
    }
    printf("grey{th3_b4g_c0nt41ns_%d_%ss!!}\n", sum, contents);
}
