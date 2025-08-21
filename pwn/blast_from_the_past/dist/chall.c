#include <stdio.h>
#include <string.h>

void ignore_me() {
	setbuf(stdin, 0);
	setbuf(stdout, 0);
}

void pew_pew_90s() {
    printf("🔫 *pew pew* Retro laser gun fires! But it's still just a cat toy from the 90s...\n");
}

int main() {

	ignore_me();
	
    char retro_cat[32];
	int ver = 50004;
    
    printf("🕹️  BLAST TO THE PAST - Cyber Cat Defense %d! 🐱💾\n", ver);
    printf("Enter your retro cyber-cat's name, dude: ");
    
	scanf("%320s", retro_cat);
    
    printf("Radical! %s is locked and loaded with a sweet laser gun!\n", retro_cat);
    pew_pew_90s();
    
    return 0;
}
