import tkinter as tk
import random
import os

# ========== Core Logic ==========
def shuffle_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    return ''.join(word_list)

def load_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            data = file.read().split(',')
            if len(data) == 2:
                return data[0], int(data[1])
    return "No one", 0

def save_highscore(name, score):
    with open("highscore.txt", "w") as file:
        file.write(f"{name},{score}")

def save_score_record(name, score, duration):
    with open("scores.txt", "a") as file:
        file.write(f"{name},{score},{duration}\n")

# ========== Game Logic ==========
def start_difficulty_selection():
    name = username_entry.get().strip()
    if not name:
        name_warning_label.config(text="Please enter your name!")
        return
    player_label.config(text=f"Player: {name}")
    name_frame.pack_forget()
    difficulty_frame.pack()

def start_game():
    global original_word, time_left, score, remaining_words, timer_running
    selected_level = difficulty.get()
    

    if selected_level == "Medium":
        with open("medium_words.txt", "r") as file:
            words = file.read().splitlines()
    else:
        with open("hard_words.txt", "r") as file:
            words = file.read().splitlines()

    remaining_words.clear()
    remaining_words.extend([w.upper() for w in words])
    random.shuffle(remaining_words)
    
    time_left = 120
    score = 0
    score_label.config(text=f"Score: {score}")
    result_label.config(text="")
    entry.config(state="normal")
    entry.delete(0, tk.END)
    hint_label.config(text="")

    difficulty_frame.pack_forget()
    
    update_timer()
    timer_running = True
    next_word()
    countdown()
    load_score_chart()
    game_frame.pack(fill="both", expand=True)  


def next_word():
    global original_word
    if remaining_words:
        original_word = remaining_words.pop()
        jumbled_label.config(text=f"Jumbled Word: {shuffle_word(original_word)}")
        entry.delete(0, tk.END)
        hint_label.config(text="")
    else:
        jumbled_label.config(text="No more words!")
        entry.config(state="disabled")
        check_and_update_highscore()

def check_guess():
    global score
    guess = entry.get().strip().upper()
    if guess == original_word:
        score += 10
        score_label.config(text=f"Score: {score}")
        result_label.config(text="Correct! 🎉", fg="green")
        if timer_running:
            next_word()
    else:
        result_label.config(text="Try Again! ❌", fg="red")

def check_and_update_highscore():
    global highscore, highscore_name, time_left
    duration = 120 - time_left
    player = username_entry.get().strip()

    save_score_record(player, score, duration)
    load_score_chart()

    if score > highscore:
        highscore = score
        highscore_name = player
        save_highscore(highscore_name, highscore)
        highscore_label.config(text=f"High Score: {highscore} by {highscore_name}")

def show_hint():
    global original_word
    if original_word:
        hint_label.config(text=f"First Letter: {original_word[0]}")
    else:
        hint_label.config(text="No word to hint yet.")

def countdown():
    global time_left, timer_running 
    if not timer_running:
        return  # Stop running if user restarted

    if time_left > 0:
        time_left -= 1
        update_timer()
        root.after(1000, countdown)
    else:
        timer_running = False
        entry.config(state="disabled")
        result_label.config(text=f"⏰ Time's up! The word was: {original_word}", fg="orange")
        check_and_update_highscore()


def update_timer():
    minutes = time_left // 60
    seconds = time_left % 60
    timer_label.config(text=f"Time Left: {minutes}:{seconds:02d}")


def load_score_chart():
    score_listbox.delete(0, tk.END)
    if os.path.exists("scores.txt"):
        with open("scores.txt", "r") as file:
            lines = file.readlines()
            for line in reversed(lines[-10:]):
                try:
                    name, score_val, duration = line.strip().split(',')
                    score_listbox.insert(tk.END, f"{name} | {score_val} | {duration}s")
                except ValueError:
                    continue

def restart_game():
    global timer_running, time_left, score, original_word, remaining_words

    # Stop the timer
    timer_running = False
    

    # Reset core variables
    time_left = 120
    score = 0
    original_word = ""
    remaining_words = []
    
    
    # Hide all frames
    game_frame.pack_forget()
    difficulty_frame.pack_forget()

    # Reset all game UI fields
    entry.delete(0, tk.END)
    entry.config(state="normal")
    result_label.config(text="")
    hint_label.config(text="")
    jumbled_label.config(text="Jumbled Word:")
    timer_label.config(text="Time Left: 2:00")
    score_label.config(text="Score: 0")
    player_label.config(text="Player: ")
    highscore_label.config(text=f"High Score: {highscore} by {highscore_name}")

    # Reset name entry
    username_entry.delete(0, tk.END)
    name_warning_label.config(text="")

    # Show the first screen
    name_frame.pack(fill="both", expand=True)



# ========== GUI Setup ==========
root = tk.Tk()
root.geometry("450x6500")
root.title("Twist n' Spell")
root.configure(bg="#0D3108")

# Game variables
original_word = ""
remaining_words = []
time_left = 120
score = 0
timer_running = False
highscore_name, highscore = load_highscore()

# ========== Frame 1: Name Entry ==========
name_frame = tk.Frame(root, bg="#0D3108")
name_frame.pack(expand=True, fill='both')  # Fill the window

center_frame = tk.Frame(name_frame, bg="#0D3108")
center_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center content

tk.Label(center_frame, text="🧩 Welcome To The Twisted World! 🧩",
         font=("Comic Sans MS", 18, "bold"), bg="#0D3108", fg="white").pack(pady=15)

tk.Label(center_frame, text="Enter Your Name:",
         font=("Arial", 14), bg="#0D3108", fg="white").pack(pady=(10, 5))

username_entry = tk.Entry(center_frame, font=("Arial", 14), width=22)
username_entry.pack(pady=5)

name_warning_label = tk.Label(center_frame, text="",
                              font=("Arial", 12), fg="yellow", bg="#0D3108")
name_warning_label.pack(pady=5)

tk.Button(center_frame, text="Next",
          command=start_difficulty_selection,
          font=("Arial", 14, "bold"), bg="#13540A", fg="white", width=12).pack(pady=10)


# ========== Frame 2: Difficulty Selection ==========
difficulty_frame = tk.Frame(root, bg="#0D3108", width=400, height=600)

center_difficulty_frame = tk.Frame(difficulty_frame, bg="#0D3108")
center_difficulty_frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(center_difficulty_frame, text="Select Difficulty:",
         font=("Arial", 18, "bold"), bg="#0D3108", fg="white").pack(pady=15)

difficulty = tk.StringVar(value="difficult")

tk.Radiobutton(center_difficulty_frame, text="Medium", variable=difficulty, value="Medium",
               font=("Arial", 14), bg="#0D3108", fg="white", selectcolor="#13540A").pack(pady=5)

tk.Radiobutton(center_difficulty_frame, text="Hard", variable=difficulty, value="Hard",
               font=("Arial", 14), bg="#0D3108", fg="white", selectcolor="#13540A").pack(pady=5)

tk.Button(center_difficulty_frame, text="Start Game", command=start_game,
          font=("Arial", 14, "bold"), bg="#13540A", fg="white", width=14).pack(pady=20)

# ========== Frame 3: Game Interface ==========
game_frame = tk.Frame(root, bg="#0D3108", width=4500, height=6500)

content_layout = tk.Frame(game_frame, bg="#0D3108")
content_layout.pack(expand=True, fill="both", padx=20, pady=20)

# LEFT: Main game UI (expand to fill)
left_frame = tk.Frame(content_layout, bg="#0D3108")
left_frame.pack(side="left", expand=True, fill="both")

center_game_frame = tk.Frame(left_frame, bg="#0D3108")
center_game_frame.place(relx=0.5, rely=0.5, anchor="center")

# Game content with normal font sizes
jumbled_label = tk.Label(center_game_frame, text="Jumbled Word:", font=("Arial", 20, "bold"),
                         bg="#0D3108", fg="white")
jumbled_label.pack(pady=15)

entry = tk.Entry(center_game_frame, font=("Arial", 16), width=30)
entry.pack(pady=10)

tk.Button(center_game_frame, text="Check Guess", command=check_guess,
          font=("Arial", 14), bg="#0D3108", fg="white").pack(pady=8)

tk.Button(center_game_frame, text="Hint", command=show_hint,
          font=("Arial", 14), bg="#0D3108", fg="white").pack()

result_label = tk.Label(center_game_frame, text="", font=("Arial", 14),
                        bg="#0D3108", fg="white")
result_label.pack(pady=6)

hint_label = tk.Label(center_game_frame, text="", font=("Arial", 14),
                      bg="#0D3108", fg="yellow")
hint_label.pack()

score_label = tk.Label(center_game_frame, text="Score: 0", font=("Arial", 14),
                       bg="#0D3108", fg="white")
score_label.pack()

player_label = tk.Label(center_game_frame, text="Player: ", font=("Arial", 14),
                        bg="#0D3108", fg="white")
player_label.pack()

highscore_label = tk.Label(center_game_frame, text=f"High Score: {highscore} by {highscore_name}",
                           font=("Arial", 14), bg="#0D3108", fg="white")
highscore_label.pack(pady=10)

tk.Button(center_game_frame, text="🔁 Restart", command=restart_game,
          font=("Arial", 14), bg="#A12B2B", fg="white").pack(pady=15)

# RIGHT: Timer and Score Chart panel (moderate width)
right_frame = tk.Frame(content_layout, bg="#0D3108", width=300)
right_frame.pack(side="right", fill="y", padx=(20, 0), anchor="n")

# Timer label at top-right, normal font
timer_label = tk.Label(right_frame, text="Time Left: 2:00", font=("Arial", 16, "bold"),
                       bg="#0D3108", fg="white", anchor="e", justify="right")
timer_label.pack(pady=(20, 15), fill="x")

# Score Chart box frame with border and background
score_box = tk.Frame(right_frame, bg="#123411", bd=3, relief="solid")
score_box.pack(fill="both", expand=True, padx=10, pady=10)

tk.Label(score_box, text="🏆 Score Board", font=("Arial", 16, "bold"),
         bg="#123411", fg="white").pack(pady=10)

score_listbox = tk.Listbox(score_box, width=25, height=20, font=("Arial", 12))
score_listbox.pack(padx=10, pady=10, fill="both", expand=True)


# ========== Mainloop ==========
name_frame.pack()
root.mainloop()


