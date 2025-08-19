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
    def __init__(self, topic, difficulty):
        self.topic = topic
        self.difficulty = difficulty