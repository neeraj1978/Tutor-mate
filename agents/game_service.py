import time
import random

class GameService:
    def __init__(self):
        self.window_duration = 120  # 2 minutes
        
        # --- Game Data Stores ---
        
        # 1. MCQ Sets (5 Sets)
        self.mcq_sets = [
            {
                "id": "mcq_science",
                "type": "MCQ_SET",
                "questions": [
                    {"q": "Which gas is most abundant in the Earth's atmosphere?", "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Argon"], "correct": "Nitrogen"},
                    {"q": "What is the chemical symbol for Gold?", "options": ["Au", "Ag", "Fe", "Pb"], "correct": "Au"},
                    {"q": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Ribosome", "Endoplasmic Reticulum"], "correct": "Mitochondria"}
                ]
            },
            {
                "id": "mcq_math",
                "type": "MCQ_SET",
                "questions": [
                    {"q": "A train running at 60km/hr crosses a pole in 9 seconds. What is the length of the train?", "options": ["120m", "150m", "180m", "324m"], "correct": "150m"},
                    {"q": "What is the square root of 144?", "options": ["10", "11", "12", "14"], "correct": "12"},
                    {"q": "If x + y = 10 and x - y = 2, what is x?", "options": ["4", "5", "6", "8"], "correct": "6"}
                ]
            },
            {
                "id": "mcq_history",
                "type": "MCQ_SET",
                "questions": [
                    {"q": "Who was the first President of the United States?", "options": ["Thomas Jefferson", "George Washington", "Abraham Lincoln", "John Adams"], "correct": "George Washington"},
                    {"q": "In which year did World War II end?", "options": ["1942", "1945", "1948", "1950"], "correct": "1945"},
                    {"q": "Who discovered America?", "options": ["Christopher Columbus", "Vasco da Gama", "Marco Polo", "James Cook"], "correct": "Christopher Columbus"}
                ]
            },
            {
                "id": "mcq_tech",
                "type": "MCQ_SET",
                "questions": [
                    {"q": "What does CPU stand for?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Process Utility", "Central Processor Unit"], "correct": "Central Processing Unit"},
                    {"q": "Which language is known as the backbone of the web?", "options": ["Python", "Java", "HTML", "C++"], "correct": "HTML"},
                    {"q": "What does 'HTTP' stand for?", "options": ["HyperText Transfer Protocol", "High Transfer Text Protocol", "HyperText Transmission Protocol", "HyperText Transfer Platform"], "correct": "HyperText Transfer Protocol"}
                ]
            },
            {
                "id": "mcq_vocab",
                "type": "MCQ_SET",
                "questions": [
                    {"q": "What is the synonym of 'Happy'?", "options": ["Sad", "Joyful", "Angry", "Bored"], "correct": "Joyful"},
                    {"q": "What is the antonym of 'Ancient'?", "options": ["Old", "Modern", "Antique", "Past"], "correct": "Modern"},
                    {"q": "Choose the correct spelling:", "options": ["Recieve", "Receive", "Riceive", "Receve"], "correct": "Receive"}
                ]
            }
        ]

        # 2. Logic Puzzles (Brain Teasers) (3 Games)
        self.logic_puzzles = [
            {
                "id": "logic_painting",
                "type": "LOGIC_PUZZLE",
                "question": "A man looks at a painting in a museum and says, 'Brothers and sisters I have none, but that man's father is my father's son.' Who is in the painting?",
                "options": ["His son", "His father", "Himself", "His nephew"],
                "correct_answer": "His son",
                "image": None
            },
            {
                "id": "logic_boat",
                "type": "LOGIC_PUZZLE",
                "question": "You see a boat filled with people, yet there isn’t a single person on board. How is that possible?",
                "options": ["It's a ghost ship", "They are all married", "It's a model boat", "They are invisible"],
                "correct_answer": "They are all married",
                "image": None
            },
            {
                "id": "logic_piano",
                "type": "LOGIC_PUZZLE",
                "question": "I have keys but no locks. I have a space but no room. You can enter, but can't go outside. What am I?",
                "options": ["A Piano", "A Keyboard", "A Map", "A Crypt"],
                "correct_answer": "A Keyboard",
                "image": None
            }
        ]

        # 3. Relation Puzzles (3 Games)
        self.relation_puzzles = [
            {
                "id": "relation_photo",
                "type": "LOGIC_PUZZLE",
                "question": "Pointing to a photograph, a lady tells Pramod, 'I am the only daughter of this lady and her son is your maternal uncle.' How is the speaker related to Pramod's father?",
                "options": ["Sister-in-law", "Wife", "Sister", "Mother"],
                "correct_answer": "Wife",
                "image": None
            },
            {
                "id": "relation_girl_boy",
                "type": "LOGIC_PUZZLE",
                "question": "A girl introduced a boy as the son of the daughter of the father of her uncle. The boy is the girl's...",
                "options": ["Brother", "Uncle", "Nephew", "Son"],
                "correct_answer": "Brother",
                "image": None
            },
            {
                "id": "relation_husband",
                "type": "LOGIC_PUZZLE",
                "question": "If P is the husband of Q and R is the mother of S and Q, what is R to P?",
                "options": ["Mother", "Sister", "Aunt", "Mother-in-law"],
                "correct_answer": "Mother-in-law",
                "image": None
            }
        ]

        # 4. Shape Count (3 Games)
        self.shape_games = [
            {
                "id": "shape_triangle",
                "type": "SHAPE_COUNT",
                "question": "How many triangles are in this image?",
                "image": "/shapes_triangle_1.png", 
                "correct_answer": "8", 
                "input_type": "number"
            },
            {
                "id": "shape_square",
                "type": "SHAPE_COUNT",
                "question": "How many squares are in this image?",
                "image": "/shapes_squares_1.png", # Placeholder: Ensure this file exists or use default
                "correct_answer": "10", 
                "input_type": "number"
            },
            {
                "id": "shape_circle",
                "type": "SHAPE_COUNT",
                "question": "How many circles are in this image?",
                "image": "/shapes_circles_1.png", # Placeholder
                "correct_answer": "7", 
                "input_type": "number"
            }
        ]

        # 5. Word Games (6 Games)
        self.word_games = [
            {
                "id": "word_scramble_1",
                "type": "WORD_SCRAMBLE",
                "question": "Unscramble this word: P H Y O S H I L O S",
                "scrambled": "PHYOSHILOS",
                "correct_answer": "PHILOSOPHY",
                "input_type": "text"
            },
            {
                "id": "word_scramble_2",
                "type": "WORD_SCRAMBLE",
                "question": "Unscramble this word: Y M O N O R T S A",
                "scrambled": "YMONORTSA",
                "correct_answer": "ASTRONOMY",
                "input_type": "text"
            },
            {
                "id": "word_scramble_3",
                "type": "WORD_SCRAMBLE",
                "question": "Unscramble this word: E R U T C E T I H C R A",
                "scrambled": "ERUTCETIHCRA",
                "correct_answer": "ARCHITECTURE",
                "input_type": "text"
            },
            {
                "id": "sentence_1",
                "type": "SENTENCE_BUILDER",
                "question": "Form a correct sentence:",
                "words": ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"],
                "correct_order": ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"], 
                "correct_answer": "The quick brown fox jumps over the lazy dog"
            },
            {
                "id": "sentence_2",
                "type": "SENTENCE_BUILDER",
                "question": "Form a correct sentence:",
                "words": ["makes", "Practice", "perfect", "man", "a"],
                "correct_order": ["Practice", "makes", "a", "man", "perfect"], 
                "correct_answer": "Practice makes a man perfect"
            },
            {
                "id": "sentence_3",
                "type": "SENTENCE_BUILDER",
                "question": "Form a correct sentence:",
                "words": ["louder", "Actions", "words", "speak", "than"],
                "correct_order": ["Actions", "speak", "louder", "than", "words"], 
                "correct_answer": "Actions speak louder than words"
            }
        ]
        
        # Combine all for rotation (Total 20 Games)
        self.all_games = (
            self.mcq_sets + 
            self.logic_puzzles + 
            self.relation_puzzles + 
            self.shape_games + 
            self.word_games
        )

    def get_current_game(self):
        current_time = int(time.time())
        window_id = current_time // self.window_duration
        time_remaining = self.window_duration - (current_time % self.window_duration)
        
        # Deterministic rotation
        game_index = window_id % len(self.all_games)
        game = self.all_games[game_index]
        
        return {
            "game": game,
            "time_remaining": time_remaining,
            "window_id": window_id
        }

    def validate_answer(self, window_id, user_answer):
        # Re-fetch game to validate (stateless validation based on window_id)
        game_index = window_id % len(self.all_games)
        game = self.all_games[game_index]
        
        is_correct = False
        score = 0
        reward = "None"
        correct_answer_display = ""

        if game["type"] == "MCQ_SET":
            # user_answer should be a dict: {"0": "6", "1": "Nitrogen", ...}
            correct_count = 0
            total_questions = len(game["questions"])
            
            if isinstance(user_answer, dict):
                for i, q in enumerate(game["questions"]):
                    if str(i) in user_answer and user_answer[str(i)] == q["correct"]:
                        correct_count += 1
            
            score = (correct_count / total_questions) * 100
            is_correct = score == 100 
            correct_answer_display = "All correct answers required."

        elif game["type"] == "LOGIC_PUZZLE":
            is_correct = user_answer == game["correct_answer"]
            score = 100 if is_correct else 0
            correct_answer_display = game["correct_answer"]

        elif game["type"] == "SHAPE_COUNT":
             is_correct = str(user_answer).strip() == str(game["correct_answer"])
             score = 100 if is_correct else 0
             correct_answer_display = game["correct_answer"]

        elif game["type"] == "WORD_SCRAMBLE":
             is_correct = str(user_answer).strip().upper() == game["correct_answer"].upper()
             score = 100 if is_correct else 0
             correct_answer_display = game["correct_answer"]

        elif game["type"] == "SENTENCE_BUILDER":
             is_correct = str(user_answer).strip() == game["correct_answer"]
             score = 100 if is_correct else 0
             correct_answer_display = game["correct_answer"]

        # Reward Logic
        if score == 100:
            reward = "Gold"
        elif score >= 66:
            reward = "Silver"
        elif score >= 33:
            reward = "Bronze"
        
        return {
            "correct": is_correct,
            "score": score,
            "reward": reward,
            "correct_answer": correct_answer_display
        }
