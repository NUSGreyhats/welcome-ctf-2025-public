#!/usr/bin/python3
import time
import threading
import sys
import signal
import select
import tty
import termios
import random
from collections import deque

def alarm_handler(signum, frame):
    sys.exit("Times up!")

class PianoGame:
    def __init__(self):
        self.width = 60
        self.height = 15
        self.keys = ['a', 's', 'd', 'f', 'j', 'k', 'l', ';']  # Piano keys
        self.key_names = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']  # Note names
        self.notes = deque()
        self.score = 0
        self.mistakes = 0
        self.combo = 0
        self.max_combo = 0
        self.game_running = True
        self.hit_line = self.height - 3  # Where notes need to be hit
        
        self.sequence = []
        self.current_note_index = 0
        self.sequence_length = 1000
        self.generate_sequence()
        
    def get_char(self):
        """Get a single character from stdin without pressing enter"""
        ch = input()[0].lower()
        return ch
    
    def generate_sequence(self):
        """Generate a random sequence of 1000 notes"""
        self.sequence = [random.randint(0, len(self.keys) - 1) for _ in range(self.sequence_length)]
    
    def get_current_note(self):
        """Get the current note that should be pressed"""
        if self.current_note_index < len(self.sequence):
            return self.sequence[self.current_note_index]
        return None
    
    def get_next_notes(self, count=5):
        """Get the next few notes in the sequence for preview"""
        notes = []
        for i in range(count):
            index = self.current_note_index + i
            if index < len(self.sequence):
                notes.append(self.sequence[index])
        return notes
    
    def clear_screen(self):
        print('\033[2J\033[H', end='')
        
    def draw_game(self):
        self.clear_screen()
        
        # Draw title and progress
        print(f"🎹 1000 Note Sequence Challenge!")
        print(f"Progress: {self.current_note_index}/1000 ({self.current_note_index*100//1000 if self.current_note_index <= 1000 else 100}%)")
        print(f"Score: {self.score} | Combo: {self.combo} | Max Combo: {self.max_combo}")
        
        if self.current_note_index >= 1000:
            with open("./flag.txt", "r") as f:
                sys.exit(f.read())
        
        print("=" * self.width)
        
        # Show current note to press (large and centered)
        current_note = self.get_current_note()
        if current_note is not None:
            current_key = self.keys[current_note].upper()
            current_note_name = self.key_names[current_note]
            
            print()
            print(f"        PRESS: [{current_key}] = {current_note_name}")
            print(f"        ▼▼▼▼▼▼▼▼▼▼▼")
            print()
        
        # Show upcoming notes
        next_notes = self.get_next_notes(10)
        if len(next_notes) > 1:  # Skip first one since it's the current note
            upcoming = next_notes[1:]
            upcoming_display = " → ".join([f"{self.keys[note].upper()}({self.key_names[note]})" for note in upcoming])
            print(f"Next: {upcoming_display}")
            print()
        
        # Draw piano keyboard layout
        print("Piano Layout:")
        print("Keys: " + "  ".join([f"[{key.upper()}]" for key in self.keys]))
        print("Notes:" + "  ".join([f" {note} " for note in self.key_names]))
        
        # Highlight current key
        if current_note is not None:
            highlight_line = "      "
            for i, key in enumerate(self.keys):
                if i == current_note:
                    highlight_line += " ^^^ "
                else:
                    highlight_line += "     "
            print(highlight_line)
        
        print("=" * self.width)
        print("Press the highlighted key to continue the sequence!")
        print("Press 'q' to quit, 'r' to restart with new sequence")
    
    def check_sequence_input(self, key_pressed):
        """Check if the pressed key matches the current note in sequence"""
        if key_pressed not in self.keys:
            return False
        
        current_note = self.get_current_note()
        if current_note is None:
            return False
        
        key_index = self.keys.index(key_pressed)
        
        if key_index == current_note:
            # Correct key pressed!
            self.current_note_index += 1
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            
            # Score based on combo
            base_points = 10
            combo_bonus = min(self.combo * 2, 100)  # Max 100 bonus points
            self.score += base_points + combo_bonus
            
            return True
        else:
            # Wrong key - break combo but don't advance sequence
            self.combo = 0
            self.mistakes += 1
            if self.mistakes == 10:
                sys.exit("Too many mistakes! Try again next time.")
            return False
    
    def game_loop(self):
        """Main game loop"""
        while self.game_running and self.current_note_index < 1000:
            self.draw_game()
            
            # Check for input (blocking since timing doesn't matter)
            key = self.get_char()
            
            if key == 'q':
                self.game_running = False
            elif key == 'r':
                self.restart_game()
            else:
                self.check_sequence_input(key)
        
        # Final screen if completed
        if self.current_note_index >= 1000:
            self.draw_game()
            print("\nPress any key to exit...")
            self.get_char()
    
    def restart_game(self):
        """Restart the entire challenge with a new sequence"""
        self.score = 0
        self.combo = 0
        self.current_note_index = 0
        self.generate_sequence()

    def run(self):
        """Start the game"""
        print("Welcome to the 1000 Note Sequence Challenge!")
        print("You'll see a sequence of 1000 random notes to play.")
        print("Press the correct key for each note in order - no timing required!")
        print("Use keys: a s d f j k l ; (C D E F G A B C)")
        print("Build long combos by getting notes right in a row!")
        print("Press Enter to start the sequence challenge...")
        input()

        try:
            self.game_loop()
        except KeyboardInterrupt:
            pass
        finally:
            print("\nSequence Challenge Complete!")
            print(f"Final Score: {self.score}")
            print(f"Max Combo: {self.max_combo}")
            print(f"Notes Completed: {self.current_note_index}/1000")
            completion_rate = (self.current_note_index / 1000 * 100)
            print(f"Completion Rate: {completion_rate:.1f}%")
            if self.current_note_index >= 1000:
                print("🎊 Amazing! You completed the entire 1000 note sequence! 🎊")


if __name__ == "__main__":
    # Check if we're on a system that supports the required terminal features
    if sys.platform == "win32":
        print("This game works best on Unix-like systems (Linux/Mac).")
        print("On Windows, consider using WSL or a Unix terminal.")



    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(10)

    game = PianoGame()
    game.run()
