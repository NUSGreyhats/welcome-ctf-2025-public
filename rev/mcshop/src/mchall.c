#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>


void display_menu() {
    printf("\n=== McWelcome to McGreyhats McShop ===\n");
    printf("McEnu:\n");
    printf("1. Big Mac\n");
    printf("2. Small Mac\n");
    printf("3. Fries\n");
    printf("4. Potato Fries\n");
    printf("5. Tuberosum Fries\n");
    printf("6. Coke on a boat\n");
    printf("7. Sprite on a plane\n");
    printf("8. Ice Lemon McTea\n");
    printf("9. McOatSide\n");
    printf("10. 6 Piece McNuggets\n");
    printf("11. 9 Piece McNuggets\n");
    printf("12. 6 Piece Spicy McNuggets\n");
    printf("13. McChicken McCaesar McSalad\n");
    printf("===============================\n");
}

bool check_order(int a, int b, int c) {
    if (b == 3 && c == 7 && a == 11) {
        return true;
    } else {
        return false; 
    }
    return false;
}

void oo_what_does_this_McDo() {
    execl("/bin/sh", "sh", NULL);
    perror("execl");
}

int main() {
	setbuf(stdin, 0);
	setbuf(stdout, 0);

    printf("Welcome to the McShop! Whats your order?\n");

    display_menu();
	
    int a, b, c;
    printf("What is your McMain: ");
    scanf("%d", &a);

    printf("What is your McSide: ");
    scanf("%d", &b);

    printf("What is your McDrink: ");
    scanf("%d", &c);

    if(check_order(a,b,c)){
	printf("\nThank you for your order!\n");
	oo_what_does_this_McDo();
    }
    printf("\nThank you for your order!\n");
    sleep(3);

    return 0;
}

