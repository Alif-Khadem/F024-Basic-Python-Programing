import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar, Style
import random


class QuizApp:
    def __init__(self, root, questions):
        self.root = root
        self.root.title("Python Quiz")
        self.questions = questions
        random.shuffle(self.questions)  # Shuffle questions for variety
        self.current_question = 0
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_points = len(questions) * 5
        self.time_left = 30  # Timer for each question
        self.quiz_finished = False  # Flag to ensure results window is shown only once
        self.is_dark_mode = False  # Default theme is light

        # Theme Configuration
        self.style = Style()
        self.set_light_theme()

        # Widgets
        self.question_label = tk.Label(root, text="", wraplength=400, font=("Arial", 16))
        self.question_label.pack(pady=20)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.options = []
        for i in range(4):
            button = tk.Button(root, text="", font=("Arial", 14), command=lambda i=i: self.check_answer(i + 1))
            button.pack(fill="x", padx=50, pady=5)
            self.options.append(button)

        self.feedback_label = tk.Label(root, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=10)

        self.correct_answer_label = tk.Label(root, text="", font=("Arial", 12))
        self.correct_answer_label.pack(pady=10)

        self.timer_label = tk.Label(root, text="Time left: 30s", font=("Arial", 14))
        self.timer_label.pack(pady=5)

        self.progress = Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)

        # Skip and Theme Buttons
        self.skip_button = tk.Button(root, text="Skip Question", font=("Arial", 12), command=self.skip_question)
        self.skip_button.pack(pady=10)

        self.theme_toggle_button = tk.Button(root, text="Toggle Dark Mode", font=("Arial", 12), command=self.toggle_theme)
        self.theme_toggle_button.pack(pady=10)

        # Display first question
        self.display_question()
        self.start_timer()

    def display_question(self):
        """Displays the current question and options."""
        question = self.questions[self.current_question]
        self.question_label.config(text=f"Q{self.current_question + 1}. {question[0]}")

        # Load and display image if available
        img_path = f"images/question{self.current_question + 1}.png"
        try:
            img = tk.PhotoImage(file=img_path)
            self.image_label.config(image=img)
            self.image_label.image = img
        except:
            self.image_label.config(image="")

        for i in range(4):
            self.options[i].config(text=question[i + 1])

        self.feedback_label.config(text="")
        self.correct_answer_label.config(text="")
        self.update_progress()

    def check_answer(self, selected_option):
        """Checks the user's answer and updates the score."""
        if self.quiz_finished:  # Prevent further interactions after the quiz ends
            return

        correct_option = self.questions[self.current_question][-1]  # Correct option index
        correct_text = self.questions[self.current_question][correct_option]  # Correct answer text

        if selected_option == correct_option:
            # Correct answer feedback
            self.feedback_label.config(text="Correct! You've earned 5 points.", fg="green")
            self.score += 5
            self.correct_answers += 1
            self.correct_answer_label.config(text="")  # Hide the correct answer label if correct
        else:
            # Incorrect answer feedback
            self.feedback_label.config(text="Incorrect.", fg="red")
            # Show the correct answer if the user's answer is wrong
            self.correct_answer_label.config(
                text=f"The correct answer was: {correct_text}", fg="blue"
            )
            self.score -= 2
            self.incorrect_answers += 1

        self.score_label.config(text=f"Score: {self.score}")
        self.next_question()

    def start_timer(self):
        """Starts the countdown timer for each question."""
        if self.quiz_finished:  # Stop the timer if the quiz is finished
            return

        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left}s", fg="black")
            self.time_left -= 1
            self.root.after(1000, self.start_timer)
        else:
            self.timer_label.config(fg="red")
            self.check_answer(None)  # Auto-check with no selection when time ends

    def next_question(self):
        """Moves to the next question or ends the quiz."""
        if self.quiz_finished:  # Prevent multiple calls after the quiz ends
            return

        self.current_question += 1
        self.time_left = 30  # Reset timer
        self.timer_label.config(fg="green")  # Flash effect on reset

        if self.current_question < len(self.questions):
            self.display_question()
            self.start_timer()
        else:
            self.show_final_results()  # Only show results once

    def skip_question(self):
        """Skips the current question without affecting the score."""
        if self.quiz_finished:
            return
        self.feedback_label.config(text="Question skipped.", fg="orange")
        self.next_question()

    def update_progress(self):
        """Updates the progress bar."""
        progress_value = (self.current_question + 1) / len(self.questions) * 100
        self.progress["value"] = progress_value

    def show_final_results(self):
        """Displays the final score and results."""
        if self.quiz_finished:  # Prevent multiple result windows
            return

        self.quiz_finished = True  # Set the flag to True

        percentage = (self.score / self.total_points) * 100
        result_message = (
            f"Final Score: {self.score}/{self.total_points}\n"
            f"Percentage: {percentage:.2f}%\n"
            f"Correct Answers: {self.correct_answers}\n"
            f"Incorrect Answers: {self.incorrect_answers}\n"
        )

        if percentage >= 60:
            result_message += "Congratulations! You passed the quiz."
        else:
            result_message += "Sorry, you failed. Better luck next time!"

        self.display_results_window(result_message)

    def display_results_window(self, result_message):
        """Displays the results in a new window with options to restart or exit."""
        results_window = tk.Toplevel(self.root)
        results_window.title("Quiz Results")
        results_window.geometry("400x300")

        results_label = tk.Label(results_window, text=result_message, font=("Arial", 14), wraplength=380, justify="left")
        results_label.pack(pady=20)

        restart_button = tk.Button(results_window, text="Restart Quiz", font=("Arial", 12), command=self.restart_quiz)
        restart_button.pack(pady=10)

        exit_button = tk.Button(results_window, text="Exit", font=("Arial", 12), command=self.root.destroy)
        exit_button.pack(pady=10)

    def restart_quiz(self):
        """Restarts the quiz."""
        self.current_question = 0
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.time_left = 30
        self.quiz_finished = False  # Reset the finished flag
        random.shuffle(self.questions)
        self.display_question()
        self.start_timer()

    def toggle_theme(self):
        """Toggles between light and dark mode."""
        if self.is_dark_mode:
            self.set_light_theme()
        else:
            self.set_dark_theme()

    def set_light_theme(self):
        """Sets the light theme."""
        self.is_dark_mode = False
        self.root.config(bg="white")
        self.style.configure("TButton", background="white", foreground="black")

    def set_dark_theme(self):
        """Sets the dark theme."""
        self.is_dark_mode = True
        self.root.config(bg="black")


# List of questions: ["Question", "Option1", "Option2", "Option3", "Option4", CorrectOption]
questions = [
    ["Which keyword is used to define a generator in Python?", "yield", "return", "def", "async", 1],
    ["What is the purpose of the @staticmethod decorator in Python?",
     "Defines an instance method", "Defines a class method", "Defines a static method", "Defines an abstract method", 3],
    ["What is the time complexity of searching for an element in a Python dictionary?",
     "O(1)", "O(log n)", "O(n)", "O(n^2)", 1],
    ["Which module in Python is used for handling regular expressions?", "regex", "re", "regexp", "pattern", 2],
    ["What does the global keyword do in Python?",
     "Defines a global variable", "Accesses a variable outside the local scope", "Creates a thread-safe variable", "Limits variable scope to the function", 2],
    ["Which built-in function can dynamically load a module in Python?", "import()", "__import__()", "load()", "load_module()", 2],
    ["What is the difference between a shallow copy and a deep copy in Python?",
     "Shallow copy copies all nested objects, deep copy does not",
     "Shallow copy copies references, deep copy copies objects", "There is no difference", "Deep copy creates threads", 2],
    ["What does the with statement ensure in Python?",
     "Encapsulation", "Garbage collection", "Resource management", "Type checking", 3],
    ["Which method is called when an object is deleted in Python?",
     "__destroy__", "__del__", "__cleanup__", "__delete__", 2],
    ["What is the purpose of Python's GIL (Global Interpreter Lock)?",
     "Improve multi-threading performance",
     "Manage memory allocation for large objects",
     "Ensure only one thread runs Python bytecode at a time", "Protect the operating system kernel", 3],
]

# Initialize the GUI
root = tk.Tk()
app = QuizApp(root, questions)
root.mainloop()
