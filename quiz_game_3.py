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
                variable=self.topic_name,
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
        self.topic_name.set("Python Programming")
        self.difficulty_var.set("Medium")

    def generate_quiz(self):
        topic = self.topic_name.get()
        if topic == "custom topic":
            topic = self.custom_topic_var.get().strip()
        else :
            if not topic:
                messagebox.showerror("Error", "Please specify a custom topic!")
                return
        
        difficulty = self.difficulty_var.get()
        if not topic or not difficulty:
            messagebox.showerror("Error", "Please select both topic and difficulty!")
            return
        
        self.root.destroy()

        self.callback(topic, difficulty)

    def run(self):
        self.root.mainloop()

class QuizGame:
    def __init__(self, root, questions, topic, difficulty):
        self.root = root
        self.root.title(f"Quiz: {topic} ({difficulty})")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")
        
        self.questions = questions
        self.topic = topic
        self.difficulty = difficulty
        
        # Shuffle questions
        random.shuffle(self.questions)
        
        # Game state
        self.current_question = 0
        self.score = 0
        self.selected_option = tk.IntVar()
        
        # Create UI
        self.create_widgets()
        self.load_question()
    
    def create_widgets(self):
        # Title with topic and difficulty
        title_text = f"Quiz: {self.topic} ({self.difficulty})"
        title_label = tk.Label(
            self.root, 
            text=title_text, 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#333",
            wraplength=650
        )
        title_label.pack(pady=15)
        
        # Progress
        self.progress_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#666"
        )
        self.progress_label.pack(pady=5)
        
        # Question frame
        question_frame = tk.Frame(self.root, bg="#f0f0f0")
        question_frame.pack(pady=20, padx=40, fill="x")
        
        self.question_label = tk.Label(
            question_frame,
            text="",
            font=("Arial", 13, "bold"),
            bg="#f0f0f0",
            fg="#333",
            wraplength=600,
            justify="left"
        )
        self.question_label.pack(anchor="w")
        
        # Options frame
        self.options_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.options_frame.pack(pady=20, padx=60, fill="x")
        
        # Radio buttons (created dynamically)
        self.option_buttons = []
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=30)
        
        # Submit button
        self.submit_btn = tk.Button(
            buttons_frame,
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
        
        # Next button
        self.next_btn = tk.Button(
            buttons_frame,
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
    
    def load_question(self):
        # Clear previous options
        for button in self.option_buttons:
            button.destroy()
        self.option_buttons.clear()
        
        # Reset selection
        self.selected_option.set(-1)
        
        # Update progress
        self.progress_label.config(
            text=f"Question {self.current_question + 1} of {len(self.questions)}"
        )
        
        # Load current question
        question_data = self.questions[self.current_question]
        self.question_label.config(text=question_data["question"])
        
        # Create option buttons
        for i, option in enumerate(question_data["options"]):
            rb = tk.Radiobutton(
                self.options_frame,
                text=option,
                variable=self.selected_option,
                value=i,
                font=("Arial", 11),
                bg="#f0f0f0",
                fg="#333",
                selectcolor="#e8e8e8",
                anchor="w",
                wraplength=500,
                justify="left"
            )
            rb.pack(anchor="w", pady=5, fill="x")
            self.option_buttons.append(rb)
        
        # Show submit button, hide next button
        self.submit_btn.pack(side="left", padx=10)
        self.next_btn.pack_forget()
    
    def submit_answer(self):
        if self.selected_option.get() == -1:
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        
        question_data = self.questions[self.current_question]
        correct_answer = question_data["correct"]
        selected_answer = self.selected_option.get()
        
        # Check if answer is correct
        if selected_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Result", "Correct! ✓")
        else:
            correct_text = question_data["options"][correct_answer]
            messagebox.showinfo("Result", f"Wrong! ✗\nCorrect answer: {correct_text}")
        
        # Update score display
        self.score_label.config(text=f"Score: {self.score}/{len(self.questions)}")
        
        # Hide submit button, show next button
        self.submit_btn.pack_forget()
        if self.current_question < len(self.questions) - 1:
            self.next_btn.pack(side="left", padx=10)
        else:
            self.show_final_results()
    
    def next_question(self):
        self.current_question += 1
        self.load_question()
    
    def show_final_results(self):
        percentage = (self.score / len(self.questions)) * 100
        
        if percentage >= 80:
            grade = "Excellent! 🌟"
        elif percentage >= 60:
            grade = "Good! 👍"
        elif percentage >= 40:
            grade = "Fair 📚"
        else:
            grade = "Keep practicing! 💪"
        
        result_message = f"""
Quiz Complete!

Topic: {self.topic}
Difficulty: {self.difficulty}
Final Score: {self.score}/{len(self.questions)}
Percentage: {percentage:.1f}%
Grade: {grade}

Would you like to take another quiz?
        """
        
        play_again = messagebox.askyesno("Quiz Complete", result_message)
        
        if play_again:
            self.root.destroy()
            main()  # Start over with topic/difficulty selection
        else:
            self.root.quit()

def start_quiz(topic, difficulty):
    """Generate questions and start the quiz"""
    
    # Show loading message
    loading_root = tk.Tk()
    loading_root.title("Generating Quiz...")
    loading_root.geometry("300x150")
    loading_root.configure(bg="#f0f0f0")
    
    loading_label = tk.Label(
        loading_root,
        text=f"Generating {difficulty.lower()} questions\nabout {topic}...\n\nPlease wait...",
        font=("Arial", 12),
        bg="#f0f0f0",
        fg="#333",
        justify="center"
    )
    loading_label.pack(expand=True)
    
    # Center the loading window
    loading_root.update_idletasks()
    width = loading_root.winfo_width()
    height = loading_root.winfo_height()
    x = (loading_root.winfo_screenwidth() // 2) - (width // 2)
    y = (loading_root.winfo_screenheight() // 2) - (height // 2)
    loading_root.geometry(f"{width}x{height}+{x}+{y}")
    
    loading_root.update()
    
    try:
        # Generate questions using AI
        generator = QuizGenerator()
        questions = generator.generate_questions(topic, difficulty)
        
        if not questions:
            raise Exception("No questions generated")
        
        loading_root.destroy()
        
        # Start the quiz game
        root = tk.Tk()
        game = QuizGame(root, questions, topic, difficulty)
        root.mainloop()
        
    except Exception as e:
        loading_root.destroy()
        messagebox.showerror("Error", f"Failed to generate quiz questions: {str(e)}\n\nPlease check your internet connection and API key.")

def main():
    """Main function to start the application"""
    # Create topic and difficulty selector
    selector = TopicDifficultySelector(start_quiz)
    selector.run()

if __name__ == "__main__":
    main()