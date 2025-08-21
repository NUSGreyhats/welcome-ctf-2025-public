#!/usr/bin/python3

import re
import math
import random

def sanitize_input(expr):
    """Simple sanitization for math expressions"""
    # Remove whitespace
    expr = expr.strip().replace(" ", "")

    # no alphabets allowed
    disallowed = re.match(r'^[a-zA-Z]+$', expr)
    if disallowed:
        return None

    # Check for dangerous patterns
    dangerous = ['__', 'import', 'exec', 'open']
    if any(bad in expr.lower() for bad in dangerous):
        return None

    return expr

def cat_math_gun_game():
    print("🐱 CAT MATH GUN GAME 🔫")
    print("Fire math expressions at enemy cats!")
    print("Example: 5*3, 10+7, (4+2)*3")
    print("-" * 30)

    player_health = 100
    enemy_cats = ["Whiskers", "Shadow", "Mittens"]

    while player_health > 0 and enemy_cats:
        # Show current enemy
        current_enemy = enemy_cats[0]
        enemy_health = random.randint(10, 25)

        print(f"\n🐱 {current_enemy} appears! (Health: {enemy_health})")
        print(f"Your health: {player_health}")

        while enemy_health > 0:
            # Get player input
            expr = input("Fire math expression (or 'quit'): ")

            if expr.lower() == 'quit':
                return

            # Sanitize and evaluate
            clean_expr = sanitize_input(expr)
            if clean_expr is None:
                print("❌ Invalid expression! Only use numbers and +, -, *, /, ()")
                continue

            try:
                # Use eval on sanitized input
                damage = eval(clean_expr)

                if not isinstance(damage, (int, float)) or damage < 0:
                    print("❌ Result must be a positive number!")
                    continue

                damage = min(int(damage), 30)  # Cap damage at 30
                enemy_health -= damage

                print(f"💥 {expr} = {eval(clean_expr)} → {damage} damage!")

                if enemy_health > 0:
                    print(f"🐱 {current_enemy} has {max(0, enemy_health)} health left")
                else:
                    print(f"🎉 {current_enemy} defeated!")
                    enemy_cats.pop(0)
                    break

            except Exception as e:
                print(f"❌ Math error: {e}")
                continue

            # Enemy attacks back
            if enemy_health > 0:
                enemy_damage = random.randint(5, 15)
                player_health -= enemy_damage
                print(f"🐱 {current_enemy} scratches you for {enemy_damage} damage!")

    # Game over
    if player_health <= 0:
        print("\n💀 You were defeated by the cats!")
    else:
        print("\n🏆 You defeated all the cats! Victory!")

if __name__ == "__main__":
    cat_math_gun_game()
