import tkinter as tk
from tkinter import messagebox
import random
import os

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "tie"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        return "user"
    else:
        return "computer"

def play(choice):
    global user_score, computer_score, draws, win_streak

    computer_choice = random.choice(choices)
    result = determine_winner(choice, computer_choice)

    if result == "tie":
        draws += 1
        win_streak = 0
        result_text.set(f"It's a tie! Computer also chose {computer_choice}.")
    elif result == "user":
        user_score += 1
        win_streak += 1
        result_text.set(f"You win! Computer chose {computer_choice}.")
    else:
        computer_score += 1
        win_streak = 0
        result_text.set(f"Computer wins! Computer chose {computer_choice}.")

    update_scores()

def update_scores():
    score_text.set(f"Your Score: {user_score} | Computer's Score: {computer_score} | Draws: {draws} | Win Streak: {win_streak}")

def exit_game():
    total_games = user_score + computer_score + draws
    summary = (
        f"Game Summary:\n"
        f"Total games played: {total_games}\n"
        f"Your score: {user_score}\n"
        f"Computer's score: {computer_score}\n"
        f"Total draws: {draws}\n"
    )

    if user_score > computer_score:
        summary += "Congratulations! You are the overall winner!"
    elif user_score < computer_score:
        summary += "The computer is the overall winner!"
    else:
        summary += "It's a tie overall!"

    messagebox.showinfo("Game Summary", summary)
    root.destroy()

def reset_game():
    global user_score, computer_score, draws, win_streak
    user_score = 0
    computer_score = 0
    draws = 0
    win_streak = 0
    result_text.set("Let's play Rock, Paper, Scissors!")
    update_scores()

# Initialize variables
choices = ["rock", "paper", "scissors"]
user_score = 0
computer_score = 0
draws = 0
win_streak = 0

# Ask for player name
player_name = input("Enter your name: ").strip()
if not player_name:
    player_name = "Player"

# Create the main window
root = tk.Tk()
root.title("Rock, Paper, Scissors")
root.geometry("500x500")
root.resizable(False, False)
root.configure(bg="#222831")

# Display title
title_label = tk.Label(root, text="Rock, Paper, Scissors", font=("Arial", 24, "bold"), bg="#222831", fg="#ffffff")
title_label.pack(pady=20)

# Display result
result_text = tk.StringVar()
result_text.set("Let's play Rock, Paper, Scissors!")
result_label = tk.Label(root, textvariable=result_text, font=("Arial", 16), bg="#393e46", fg="#eeeeee", relief="solid", padx=10, pady=10)
result_label.pack(pady=10)

# Display scores
score_text = tk.StringVar()
score_label = tk.Label(root, textvariable=score_text, font=("Arial", 14), bg="#222831", fg="#00adb5")
score_label.pack(pady=10)
update_scores()

# Create buttons for user choices
button_frame = tk.Frame(root, bg="#222831")
button_frame.pack(pady=20)

rock_button = tk.Button(button_frame, text="Rock", font=("Arial", 16), bg="#00adb5", fg="#ffffff", activebackground="#eeeeee", activeforeground="#000000", command=lambda: play("rock"))
rock_button.grid(row=0, column=0, padx=15, pady=10)

paper_button = tk.Button(button_frame, text="Paper", font=("Arial", 16), bg="#00adb5", fg="#ffffff", activebackground="#eeeeee", activeforeground="#000000", command=lambda: play("paper"))
paper_button.grid(row=0, column=1, padx=15, pady=10)

scissors_button = tk.Button(button_frame, text="Scissors", font=("Arial", 16), bg="#00adb5", fg="#ffffff", activebackground="#eeeeee", activeforeground="#000000", command=lambda: play("scissors"))
scissors_button.grid(row=0, column=2, padx=15, pady=10)

# Reset button
reset_button = tk.Button(root, text="Reset Game", font=("Arial", 16), bg="#00adb5", fg="#ffffff", activebackground="#eeeeee", activeforeground="#000000", command=reset_game)
reset_button.pack(pady=10)

# Exit button
exit_button = tk.Button(root, text="Exit Game", font=("Arial", 16), bg="#ff4444", fg="#ffffff", activebackground="#eeeeee", activeforeground="#000000", command=exit_game)
exit_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
