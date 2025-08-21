#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

// RC4 implementation
void askodamdsa(unsigned char *s, unsigned char *key, int key_len) {
    int i, j = 0;
    unsigned char temp;
    
    // Initialize S-box
    for (i = 0; i < 256; i++) {
        s[i] = i;
    }
    
    // Key scheduling
    for (i = 0; i < 256; i++) {
        j = (j + s[i] + key[i % key_len]) % 256;
        temp = s[i];
        s[i] = s[j];
        s[j] = temp;
    }
}

void djfoisjfmvcx(unsigned char *s, unsigned char *data, int data_len) {
    int i = 0, j = 0, k;
    unsigned char temp;
    
    for (k = 0; k < data_len; k++) {
        i = (i + 1) % 256;
        j = (j + s[i]) % 256;
        
        temp = s[i];
        s[i] = s[j];
        s[j] = temp;
        
        data[k] ^= s[(s[i] + s[j]) % 256];
    }
}

__declspec(dllexport) int generate_ejrwwdfs(char *output_key) {
    const char *base_key = "grey_hats_is_cool";
    
    strcpy(output_key, base_key);
    
    return strlen(output_key);
}

__declspec(dllexport) void fjdsmfposmvcs(char *input_data, int data_len, char *output_data) {
    char key[256];
    unsigned char s[256];
    
    // Generate the key
    int key_len = generate_ejrwwdfs(key);
    
    // Copy input to output for in-place encryption
    memcpy(output_data, input_data, data_len);
    
    // Initialize RC4
    askodamdsa(s, (unsigned char*)key, key_len);
    
    // Encrypt the text file
    djfoisjfmvcx(s, (unsigned char*)output_data, data_len);
}

// Some dummy functions to make it look less suspicious
__declspec(dllexport) void innocent_function1() {
    // Does nothing, just here to confuse
    printf("This is totally innocent code!\n");
}

__declspec(dllexport) void innocent_function2() {
    // Another dummy function
    int x = 42;
    x *= 2;
    // Result is never used
}

// DLL entry point
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    switch (fdwReason) {
        case DLL_PROCESS_ATTACH:
            break;
        case DLL_THREAD_ATTACH:
            break;
        case DLL_THREAD_DETACH:
            break;
        case DLL_PROCESS_DETACH:
            break;
    }
    return TRUE;
}
