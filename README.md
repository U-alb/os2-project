# Haunted Mansion

## Description

Haunted Mansion is an interactive text-based adventure game that uses a GUI interface built with `tkinter`. Players explore different rooms of a haunted mansion, uncovering secrets, encountering random events, and making choices that affect their fate. The game features randomized outcomes to enhance replayability and includes sound effects for an immersive experience.

## Features

- Explore various rooms: living room, kitchen, basement, attic, and garden.
- Random events that occur during exploration.
- GUI-based interface with `tkinter`.
- Player input for decisions.
- Sound effects using `pygame`.
- Customizable player name.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/haunted-mansion.git
    cd haunted-mansion
    ```

2. Install the required dependencies:
    ```sh
    pip install pygame
    ```

3. Ensure you have `tkinter` installed (it comes pre-installed with standard Python distributions).

## How to Play

1. Run the game:
    ```sh
    python main.py
    ```

2. A window will appear prompting you to enter your name.

3. Navigate through the mansion by making choices presented in dialog boxes.

4. Encounter random events and make decisions to uncover secrets and survive the haunted mansion.

5. Enjoy the immersive experience with sound effects.

## Code Structure

- `story.py`: Main game logic and GUI implementation.
- `assets/`: Directory containing sound files used in the game.

## Example Code

Here is a snippet of how the game defines the player

```python
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack = 10
        self.defense = 5

    def is_alive(self):
        return self.health > 0

    def print_status(self):
        messagebox.showinfo("Outcome",
                            "\n" + "-" * 20 + "\n" + f"{self.name}: Health = {self.health}, Attacking = {self.attack}, Defense = {self.defense}")

    def modify_attack(self, value):
        self.attack = value

    def modify_defense(self, value):
        self.defense = value