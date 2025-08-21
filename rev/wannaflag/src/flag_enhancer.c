#include <windows.h>
#include <stdio.h>
#include <string.h>

// Function prototypes for DLL imports
typedef void (*EncryptDataFunc)(char*, int, char*);
typedef int (*GenerateKeyFunc)(char*);

int main() {
    printf("HAHAH EXECUTING MY BLACKHATS PAYLOAD BRRRRRRRRRRRRRRRRR:\n");
    
    // Load the DLL
    HINSTANCE hDll = LoadLibrary("not_sus.dll");
    if (!hDll) {
        printf("Error: Could not load encryption module!\n");
        return 1;
    }
    
    // Get function addresses
    EncryptDataFunc fjdsmfposmvcs = (EncryptDataFunc)GetProcAddress(hDll, "fjdsmfposmvcs");
    if (!fjdsmfposmvcs) {
        printf("Error: Could not find encryption function!\n");
        FreeLibrary(hDll);
        return 1;
    }
    
    Sleep(500);
    
    // Check if flag.txt exists in parent directory
    FILE *flag_file = fopen("./flag.txt", "r");
    char flag[256];
    char encrypted_flag[256];
    int flag_len;
    int is_real_flag = 1;
    
    if (!flag_file) {
        // Create fake flag if flag.txt doesn't exist
        strcpy(flag, "grey{fake_flag}");
        is_real_flag = 0;
        
        // Create the fake flag.txt file in parent directory
        flag_file = fopen("./flag.txt", "w");
        if (flag_file) {
            fprintf(flag_file, "%s", flag);
            fclose(flag_file);
        }
    } else {
        // Read the real flag from ../flag.txt
        fgets(flag, sizeof(flag), flag_file);
        fclose(flag_file);
        
        // Remove newline if present
        flag[strcspn(flag, "\n")] = 0;
    }
    
    flag_len = strlen(flag);
    
    // Encrypt the flag
    fjdsmfposmvcs(flag, flag_len, encrypted_flag);
    
    printf("Hehe, I bet you'll never find out what the flag is!\n");

    // Write the "ransom note"
    FILE *ransom_file = fopen("./flag.blackhat", "w");
    if (!ransom_file) {
        printf("Error: Could not create output file!\n");
        FreeLibrary(hDll);
        return 1;
    }
    
    // Add protection message if using fake flag
    fprintf(ransom_file, "THIS FLAG ISNT THE REAL ENCRYPTED VALUE\n\n");    
    fprintf(ransom_file, "=== THIS IS A SUPER IMPORTANT MESSAGE BY ORDER OF THE NUS BLACKHATS ===\n\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣠⣤⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠘⣿⣿⣿⣿⠟⠁⠀⠀⠀⠹⣿⣿⣿⣿⣿⠟⠁⠀⠀⠹⣿⣿⡿⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⠀⢼⣿⠀⢿⣿⣿⣿⣿⠀⣾⣷⠀⠀⢿⣿⣷⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⢠⣿⣿⣿⣷⡀⠀⠀⠈⠋⢀⣿⣿⣿⣿⣿⡀⠙⠋⠀⢀⣾⣿⣿⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⢀⣀⣀⣀⣿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⣿⣾⣿⣷⣦⣤⣴⣿⣿⣿⣿⣤⠤⢤⣤⡄\n");
    fprintf(ransom_file, "⠈⠉⠉⢉⣙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣀⣀⣀⡀⠀\n");
    fprintf(ransom_file, "⠐⠚⠋⠉⢀⣬⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣥⣀⡀⠈⠀⠈⠛\n");
    fprintf(ransom_file, "⠀⠀⠴⠚⠉⠀⠀⠀⠉⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠋⠁⠀⠀⠀⠉⠛⠢⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀\n");
    fprintf(ransom_file, "⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀\n\n");
    fprintf(ransom_file, "Your flag has been encrypted!\n\n");
    fprintf(ransom_file, "To recover it, you must watch this video 1000 times on repeat:\n");
    fprintf(ransom_file, "https://www.youtube.com/watch?v=IFlDpUeMsKM\n\n");
    fprintf(ransom_file, "Or you can try decrypting it yourself LOL\n");
    fprintf(ransom_file, "Your encrypted flag is:\n");
    
    // Write encrypted flag as hex
    for (int i = 0; i < flag_len; i++) {
        fprintf(ransom_file, "%02x", (unsigned char)encrypted_flag[i]);
    }
    fprintf(ransom_file, "\n\n");
    
    fprintf(ransom_file, "- Hexerberg, Supreme Leader of NUS Blackhats\n");
    
    fclose(ransom_file);
    
    
    // Clean up
    FreeLibrary(hDll);
    
    // DeleteFile("not_sus.dll");
    return 0;
}
