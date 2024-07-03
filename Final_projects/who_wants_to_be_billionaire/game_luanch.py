import tkinter as tk
from tkinter import messagebox
import random
from tkinter import simpledialog
from tkinter import *

class MillionaireGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Who Wants to Be a Billionaire")
        self.questions = self.load_questions()
        self.current_question = 0
        self.score = 0
        self.lifelines = {
            "ask_audience": True,
            "fifty_fifty": True,
            "call_friend": True,
            "clicked": False

        }
        self.player_name = ""
        self.players_board = {'player_name':self.player_name,
                              'player_score': self.score}
        self.ask_player_name()
        self.setup_ui()
    def save_data(self):
        self.player_name = self.player_name.get()  
        self.lifelines["clicked"] = True
        if self.lifelines["clicked"]:
            self.save_button.config(state=tk.DISABLED)
    def ask_player_name(self):
        label = tk.Label(self.root, text="Your Name", font=("Arial", 16))
        label.pack(pady=20, padx=50)
        
        self.player_name = tk.Entry(self.root, width=50) 
        self.player_name.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save", command=self.save_data)
        self.save_button.pack()
        
        
    def setup_ui(self):
        self.question_label = tk.Label(self.root, text="", wraplength=600, justify="center", font=("Helvetica", 16))
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self.root, text="", width=40, height=2, font=("Helvetica", 12), command=lambda idx=i: self.choose_option(idx))
            button.pack(pady=5)
            self.option_buttons.append(button)

        self.lifeline_frame = tk.Frame(self.root)
        self.lifeline_frame.pack(pady=10)

        self.ask_audience_button = tk.Button(self.lifeline_frame, text="Ask the Audience", command=self.ask_audience, state=tk.NORMAL if self.lifelines["ask_audience"] else tk.DISABLED)
        self.ask_audience_button.pack(side=tk.LEFT, padx=10)

        self.fifty_fifty_button = tk.Button(self.lifeline_frame, text="50-50", command=self.fifty_fifty, state=tk.NORMAL if self.lifelines["fifty_fifty"] else tk.DISABLED)
        self.fifty_fifty_button.pack(side=tk.LEFT, padx=10)

        self.call_friend_button = tk.Button(self.lifeline_frame, text="Call_friend", command=self.call_friend, state=tk.NORMAL if self.lifelines["call_friend"] else tk.DISABLED)
        self.call_friend_button.pack(side=tk.LEFT, padx=10)

        self.next_question()

    def load_questions(self):
        # Replace with actual question loading mechanism
        return [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Madrid"],
                "answer": 1
            },
            {
                "question": "Who wrote 'Hamlet'?",
                "options": ["Shakespeare", "Dickens", "Austen", "Hemingway"],
                "answer": 0
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Mars", "Venus", "Jupiter", "Mercury"],
                "answer": 0
            },
            {
                "question": "What is the largest mammal?",
                "options": ["Elephant", "Whale", "Giraffe", "Rhino"],
                "answer": 1
            },
            {
                "question": "Who invented the light bulb?",
                "options": ["Thomas Edison", "Nikola Tesla", "Alexander Graham Bell", "Albert Einstein"],
                "answer": 0
            }
            # Add more questions as needed
        ]

    def next_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.question_label.config(text=question["question"])

            options = question["options"]
            for i in range(4):
                self.option_buttons[i].config(text=options[i])

            self.enable_lifelines()
        else:
            self.end_game()

    def choose_option(self, idx):
        question = self.questions[self.current_question]
        if idx == question["answer"]:
            self.score += 1000
            messagebox.showinfo("Correct", "Correct answer!")
        else:
            messagebox.showinfo("Incorrect", "Incorrect answer!")

        self.current_question += 1
        self.next_question()

    def ask_audience(self):
        audience_response = {
            0: random.randint(10, 80),
            1: random.randint(5, 90),
            2: random.randint(3, 95),
            3: random.randint(2, 98)
        }
        messagebox.showinfo("Ask the Audience",
                            f"The audience response:\nOption A: {audience_response[0]}%\n"
                            f"Option B: {audience_response[1]}%\nOption C: {audience_response[2]}%\n"
                            f"Option D: {audience_response[3]}%")
        self.lifelines["ask_audience"] = False


    def fifty_fifty(self):
        question = self.questions[self.current_question]
        correct_answer = question["answer"]
        options = list(range(4))
        options.remove(correct_answer)
        incorrect_option = random.choice(options)
        remaining_options = [correct_answer, incorrect_option]
        random.shuffle(remaining_options)

        for i in range(4):
            if i not in remaining_options:
                self.option_buttons[i].config(state=tk.DISABLED)

        self.lifelines["fifty_fifty"] = False


    def call_friend(self):
        question = self.questions[self.current_question]
        answer = question["answer"]
        messagebox.showinfo("call_friend", f"You friend Says its look like a {question["options"][answer]} !")
        self.lifelines["call_friend"] = False
    def enable_lifelines(self):
        self.ask_audience_button.config(state=tk.NORMAL if self.lifelines["ask_audience"] else tk.DISABLED)
        self.fifty_fifty_button.config(state=tk.NORMAL if self.lifelines["fifty_fifty"] else tk.DISABLED)
        self.call_friend_button.config(state=tk.NORMAL if self.lifelines["call_friend"] else tk.DISABLED)
        if not self.lifelines["fifty_fifty"]:
            for i in range(4):
                self.option_buttons[i].config(state=tk.NORMAL)

    def end_game(self):
        self.players_board['player_name'] = self.player_name
        self.players_board['player_score'] = self.score
        with open("top_playersssd.txt", 'w', encoding='utf-8') as file:
                file.write(f"{self.players_board['player_name'],{self.players_board['player_score']}}\n")
                
        messagebox.showinfo("Game Over", f" {self.player_name} Your final score is: {self.score}")
        self.root.destroy()

def main():
    root = tk.Tk()
    game = MillionaireGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
