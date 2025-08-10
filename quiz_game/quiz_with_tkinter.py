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
        pass

    def load_questions(self):
        pass

    def submit_answers(self):
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
