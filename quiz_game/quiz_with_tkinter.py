import tkinter as tk
from tkinter import messagebox
import random


class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("quiz app")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct": 2
            },
            {
                "question": "Which programming language is known for its simplicity?",
                "options": ["C++", "Python", "Assembly", "Java"],
                "correct": 1
            },
            {
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "correct": 1
            },
            {
                "question": "Which planet is closest to the Sun?",
                "options": ["Venus", "Mercury", "Earth", "Mars"],
                "correct": 1
            },
            {
                "question": "What does HTML stand for?",
                "options": ["Hyper Text Markup Language", "Home Tool Markup Language", 
                          "Hyperlinks and Text Markup Language", "Hyperlinking Text Marking Language"],
                "correct": 0
            }
        ]

        random.shuffle(self.questions)

        self.current_question = 0
        self.score = 0
        self.selected_option = tk.IntVar()

        self.create_widgets()
        self.load_questions()

    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Quiz Game", 
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=20)
        
        # Progress
        self.progress_label = tk.Label(
            self.root,
            text="",
            font=("Arial, 12"),
            bg="#f0f0f0",
            fg="#666"
        )
        self.progress_label.pack(pady=5)

        # Question frame

        question_frame = tk.Frame(self.root, bg="#f0f0f0")
        question_frame.pack(pady=20, padx=40, fill="x")

        self.questions_label = tk.Label(
            question_frame,
            text = "",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#333",
            wraplength=500,
            justify="left"
        )

        self.questions_label.pack(anchor="w")

        # Options frame
        
        self.option_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.option_frame.pack(pady= 20, padx=40, fill='x')

        # Radio buttons for options (will be created dynamically)
        self.option_buttons = []

        # Buttons frame
        button_frame = tk.Frame(
            self.root,
            bg = "#f0f0f0"
        )

        button_frame.pack(pady= 30)

        # Submit button
        self.submit_btn = tk.Button(
            button_frame,
            text="Submit Answer",
            command=self.submit_answer,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2"
        )
        self.submit_btn.pack(side="left", padx=10)

        # Next button (initially hidden)
        self.next_btn = tk.Button(
            button_frame,
            text="Next Question",
            command=self.next_question,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2"
        )
        
        # Score label
        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.score}/{len(self.questions)}",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        self.score_label.pack(side="bottom", pady=10)


    def load_questions(self):
        pass

    def submit_answer(self):
        pass

    def show_final_result(self):
        pass

    def next_question(self):
        self.current_question+=1
        self.lod_questions()



def main():
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
