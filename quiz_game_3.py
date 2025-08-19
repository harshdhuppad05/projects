# ask on what topic you want 5 questions
# ask the level of difficulty in the questions three options-:easy medium difficult
# generate prompt according to it and call llm specify the format {question, options, correct}
import google.generativeai as genai
import google.generativeai as genai
import os
import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import re

genai.configure(api_key="")

class QuizGenerator:
    def __init__(self):
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def generate_questions(self, topic, difficulty, num_questions = 5):
        """Generate quiz questions using Gemini AI"""
        prompt = f"""
        Create exactly {num_questions} multiple choice quiz questions about {topic} with {difficulty} difficulty level.

        Requirements:
        - Each question should have exactly 4 options (A, B, C, D)
        - Only one correct answer per question
        - Questions should be appropriate for {difficulty} level
        - Return the response in valid JSON format only, no additional text

        Format your response as a JSON array like this:
        [
            {{
                "question": "Your question here?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": 0
            }},
            {{
                "question": "Another question?",
                "options": ["Option A", "Option B", "Option C", "Option D"], 
                "correct": 2
            }}
        ]

        Topic: {topic}
        Difficulty: {difficulty}
        Number of questions: {num_questions}
        """

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group()
            else:
                json_text = response_text

            questions = json.loads(json_text)
            
            # Validate the structure
            if not isinstance(questions, list):
                raise ValueError("Response is not a list")
                
            for q in questions:
                if not all(key in q for key in ["question", "options", "correct"]):
                    raise ValueError("Missing required keys in question")
                if len(q["options"]) != 4:
                    raise ValueError("Each question must have exactly 4 options")
                if not (0 <= q["correct"] <= 3):
                    raise ValueError("Correct answer index must be between 0-3")
            
            return questions

        except Exception as e:
            print(f"error generating questions {e}")
            return self.fall_back_questions(topic, difficulty)
    
    
    def get_fallback_questions(self, topic, difficulty):
        """Fallback questions if AI generation fails"""
        return [
            {
                "question": f"This is a sample {difficulty} question about {topic}. What is 2+2?",
                "options": ["3", "4", "5", "6"],
                "correct": 1
            },
            {
                "question": f"Another {difficulty} {topic} question. Which is larger?",
                "options": ["10", "5", "15", "8"],
                "correct": 2
            },
            {
                "question": f"Final {difficulty} question on {topic}. Best practice?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": 0
            }
        ]
    
class TopicDifficultySelector:
    def __init__(self, callback):
        self.callback = callback
        self.setup_selection_window()

    def setup_selection_window(self):
        self.root = tk.Tk()
        self.root.title("Quiz Setup")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        title_label = tk.Label(
            self.root,
            text="Quiz Generator",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=20)

        topic_label = tk.Label(
            self.root,
            text="Select Topic",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        topic_label.pack(pady=10)


        self.topic_name = tk.StringVar()
        topic_frame = tk.Frame(
            self.root,
             bg="#f0f0f0"
        )
        topic_frame.pack(pady=10)
        topics = ["Python Programming", "Mathematics", "Science", "History", "Geography", "Literature", "Custom Topic"]

        for topic in topics:
            rb = tk.Radiobutton(
                topic_frame,
                text=topic,
                variable=self.topic_var,
                value=topic,
                bg="#f0f0f0",
                fg="#333",
                font=("Arial", 10)
            )
            rb.pack(anchor="w")

        self.custom_topic_var = tk.StringVar()
        custom_label = tk.Label(
            self.root,
            text="If Custom Topic, specify below:",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666"
        )
        custom_label.pack(pady=(10, 5))

        self.custom_entry = tk.Entry(
            self.root,
            textvariable=self.custom_topic_var,
            font=("Arial", 10),
            width=30
        )

        self.custom_entry.pack(pady= 5)

        difficulty_label = tk.Label(
            self.root,
            text="Select Difficulty:",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        difficulty_label.pack(pady=(20, 10))

        self.difficulty_var = tk.StringVar()
        difficulty_frame = tk.Frame(self.root, bg="#f0f0f0")
        difficulty_frame.pack(pady=10)
        
        difficulties = ["Easy", "Medium", "Hard"]
        for difficulty in difficulties:
            rb = tk.Radiobutton(
                difficulty_frame,
                text=difficulty,
                variable=self.difficulty_var,
                value=difficulty,
                bg="#f0f0f0",
                fg="#333",
                font=("Arial", 10)
            )
            rb.pack(side="left", padx=20)

        generate_btn = tk.Button(
            self.root,
            text="Generate Quiz",
            command=self.generate_quiz,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        generate_btn.pack(pady=30)
        
        # Set defaults
        self.topic_var.set("Python Programming")
        self.difficulty_var.set("Medium")

    def run(self):
        self.root.mainloop()
