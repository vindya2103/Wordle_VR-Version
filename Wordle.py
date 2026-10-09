
import tkinter as tk
import random

# ---------------- GAME SETTINGS ----------------

WORDS = [
    "APPLE", "BRAIN", "CHAIR", "DREAM", "EARTH",
    "FLAME", "GRAPE", "HOUSE", "JUICE", "LEMON",
    "MOUSE", "NIGHT", "PLANT", "QUICK", "SMILE",
    "TRAIN", "WATER", "TIGER", "BREAD", "CLOUD",
    "SQUAD", "CRANE", "STONE", "LIGHT", "MUSIC",
    "PRIDE", "WORLD", "HEART", "SHARE", "ROBOT"
]

GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
EMPTY = "#ffffff"
BORDER = "#d3d6da"
DARK = "#202124"

answer = random.choice(WORDS)
current_guess = ""
row_number = 0
game_over = False
keyboard_colors = {}

# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Word Guess - Python Game")
root.geometry("410x720")
root.resizable(False, False)
root.configure(bg="white")

# ---------------- HEADER ----------------

header = tk.Frame(root, bg="white")
header.pack(fill="x", padx=15, pady=(12, 8))

tk.Label(
    header,
    text="?",
    font=("Arial", 17, "bold"),
    bg="white",
    fg=DARK
).pack(side="left")

tk.Label(
    header,
    text="WORD GUESS",
    font=("Georgia", 21, "bold"),
    bg="white",
    fg=DARK
).pack(side="left", expand=True)

tk.Button(
    header,
    text="↻",
    font=("Arial", 19),
    bg="white",
    fg=DARK,
    relief="flat",
    command=lambda: new_game()
).pack(side="right")

tk.Frame(root, bg="#dddddd", height=1).pack(fill="x")

# ---------------- MESSAGE ----------------

message = tk.Label(
    root,
    text="Guess the 5-letter word!",
    font=("Arial", 11),
    bg="white",
    fg=DARK
)
message.pack(pady=10)

# ---------------- GUESS GRID ----------------

grid_frame = tk.Frame(root, bg="white")
grid_frame.pack(pady=5)

tiles = []

for r in range(6):
    tile_row = []

    for c in range(5):
        tile = tk.Label(
            grid_frame,
            text="",
            font=("Arial", 22, "bold"),
            width=2,
            height=1,
            bg="white",
            fg=DARK,
            relief="solid",
            bd=1,
            highlightbackground=BORDER
        )
        tile.grid(row=r, column=c, padx=3, pady=3, ipadx=4, ipady=4)
        tile_row.append(tile)

    tiles.append(tile_row)

# ---------------- TILE COLOURS ----------------

def evaluate_guess(guess, target):
    result = ["grey"] * 5
    remaining = list(target)

    # Correct letters in correct positions
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = "green"
            remaining[i] = None

    # Correct letters in different positions
    for i in range(5):
        if result[i] != "green" and guess[i] in remaining:
            result[i] = "yellow"
            remaining[remaining.index(guess[i])] = None

    return result


def paint_tile(row, col, letter, color=None):
    bg = {
        "green": GREEN,
        "yellow": YELLOW,
        "grey": GREY
    }.get(color, EMPTY)

    fg = "white" if color else DARK

    tiles[row][col].config(
        text=letter,
        bg=bg,
        fg=fg,
        highlightbackground=BORDER
    )


# ---------------- KEYBOARD ----------------

keyboard_frame = tk.Frame(root, bg="white")
keyboard_frame.pack(pady=18, fill="x")

keyboard_rows = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    ["ENTER"] + list("ZXCVBNM") + ["⌫"]
]

key_buttons = {}


def create_keyboard():
    for widget in keyboard_frame.winfo_children():
        widget.destroy()

    key_buttons.clear()

    for r, letters in enumerate(keyboard_rows):
        row_frame = tk.Frame(keyboard_frame, bg="white")
        row_frame.pack(pady=3)

        for letter in letters:
            is_action = letter in ("ENTER", "⌫")

            key = tk.Button(
                row_frame,
                text=letter,
                font=("Arial", 9, "bold"),
                width=5 if is_action else 2,
                height=2,
                relief="flat",
                bd=0,
                bg="#d3d6da",
                fg=DARK,
                activebackground="#b8bbc0",
                command=lambda ch=letter: press_key(ch)
            )

            key.pack(side="left", padx=2)
            key_buttons[letter] = key


def update_keyboard(letter, color):
    priority = {"grey": 1, "yellow": 2, "green": 3}

    old_color = keyboard_colors.get(letter)

    if old_color is None or priority[color] > priority[old_color]:
        keyboard_colors[letter] = color

        bg = {
            "green": GREEN,
            "yellow": YELLOW,
            "grey": GREY
        }[color]

        key_buttons[letter].config(
            bg=bg,
            fg="white"
        )


# ---------------- GAME LOGIC ----------------

def press_key(key):
    global current_guess

    if game_over:
        return

    if key == "ENTER":
        submit_guess()

    elif key == "⌫":
        current_guess = current_guess[:-1]
        update_current_row()

    elif len(key) == 1 and key.isalpha():
        if len(current_guess) < 5:
            current_guess += key.upper()
            update_current_row()


def update_current_row():
    for c in range(5):
        letter = current_guess[c] if c < len(current_guess) else ""
        paint_tile(row_number, c, letter)


def submit_guess():
    global current_guess, row_number, game_over

    if len(current_guess) != 5:
        message.config(text="Please enter 5 letters!")
        return

    guess = current_guess
    result = evaluate_guess(guess, answer)

    for i in range(5):
        paint_tile(row_number, i, guess[i], result[i])
        update_keyboard(guess[i], result[i])

    if guess == answer:
        message.config(text="Excellent! You guessed the word!")
        game_over = True
        return

    row_number += 1
    current_guess = ""

    if row_number == 6:
        message.config(text="Game over! Word: " + answer)
        game_over = True
    else:
        message.config(text="Try again! Attempts left: " +
                       str(6 - row_number))


# ---------------- NEW GAME ----------------

def new_game():
    global answer, current_guess, row_number, game_over, keyboard_colors

    answer = random.choice(WORDS)
    current_guess = ""
    row_number = 0
    game_over = False
    keyboard_colors = {}

    for r in range(6):
        for c in range(5):
            paint_tile(r, c, "")

    create_keyboard()

    message.config(text="Guess the 5-letter word!")


# ---------------- PHYSICAL KEYBOARD ----------------

def physical_key(event):
    if event.keysym == "Return":
        press_key("ENTER")
    elif event.keysym == "BackSpace":
        press_key("⌫")
    elif event.char.isalpha() and len(event.char) == 1:
        press_key(event.char.upper())


root.bind("<Key>", physical_key)

create_keyboard()

# ---------------- START GAME ----------------

root.mainloop()
