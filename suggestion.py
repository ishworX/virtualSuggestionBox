"""
Mini Virtual Suggestion Box 

Features:
- View suggestion summary (counts by category)
- View a random suggestion
- List all questions and view/add multiple answers
- Persistent storage: load/save suggestions and questions to files
- Improved input validation and error handling

Demonstrates Python concepts: lists, dictionaries, functions, flow control, file I/O, and API usage.
"""

import random
from langdetect import detect
from googletrans import Translator
from textblob import TextBlob
import os

translator = Translator()

# Data storage structures
suggestions = []  # List of translated suggestions
questions = {}    # Dict: question (str) -> list of answers (list of str)

categories = {
    "Facility": [],
    "Work Process": [],
    "Benefits": [],
    "Other": []
}

category_keywords = {
    "Facility": ["office", "room", "desk", "chair", "light", "building"],
    "Work Process": ["workflow", "schedule", "process", "meeting", "task", "communication"],
    "Benefits": ["bonus", "leave", "health", "insurance", "raise", "salary"]
}

# File paths for persistence
SUGGESTIONS_FILE = "suggestions.txt"
QUESTIONS_FILE = "questions.txt"

def load_suggestions():
    """Load suggestions from file and categorize them."""
    if os.path.exists(SUGGESTIONS_FILE):
        with open(SUGGESTIONS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                suggestion = line.strip()
                if suggestion:
                    suggestions.append(suggestion)
                    categorize_suggestion(suggestion)

def save_suggestion(suggestion):
    """Append a new suggestion to the suggestions file."""
    with open(SUGGESTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(suggestion + "\n")

def load_questions():
    """Load questions and their answers from file."""
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            current_question = None
            for line in f:
                line = line.strip()
                if line.startswith("Q: "):
                    current_question = line[3:]
                    if current_question not in questions:
                        questions[current_question] = []
                elif line.startswith("A: ") and current_question is not None:
                    questions[current_question].append(line[3:])
                elif line == "---":
                    current_question = None

def save_question(question, answer=None):
    """Append a question and optionally an answer to the questions file."""
    with open(QUESTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(f"Q: {question}\n")
        if answer is not None:
            f.write(f"A: {answer}\n")
        f.write("---\n")

def detect_and_translate(text):
    """Detect language and translate to English if needed."""
    try:
        lang = detect(text)
        if lang != 'en':
            translated = translator.translate(text, dest='en')
            return translated.text
        else:
            return text
    except Exception as e:
        print(f"[Error] Language detection or translation failed: {e}")
        return text

def analyze_sentiment(text):
    """Analyze sentiment polarity and return category."""
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return "Positive"
        elif polarity < -0.1:
            return "Negative"
        else:
            return "Neutral"
    except Exception as e:
        print(f"[Error] Sentiment analysis failed: {e}")
        return "Neutral"

def categorize_suggestion(text):
    """Categorize suggestion and store it."""
    text_lower = text.lower()
    for category, keywords in category_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            categories[category].append(text)
            return category
    categories["Other"].append(text)
    return "Other"

def add_suggestion():
    """Prompt and process a suggestion."""
    original = input("Enter your anonymous suggestion: ")
    translated = detect_and_translate(original)
    sentiment = analyze_sentiment(translated)
    suggestions.append(translated)
    save_suggestion(translated)
    category = categorize_suggestion(translated)
    print(f"Suggestion (translated): {translated}")
    print(f"Sentiment: {sentiment}")
    print(f"Categorized under: {category}")

def view_summary():
    """Print counts of suggestions by category."""
    print("\nSuggestion Summary:")
    for category, items in categories.items():
        print(f"{category}: {len(items)}")

def random_suggestion():
    """Display a random suggestion if available."""
    if suggestions:
        print("\nRandom Suggestion:")
        print(random.choice(suggestions))
    else:
        print("\nNo suggestions available yet.")

def add_question():
    """Prompt user to submit a question if not duplicate."""
    question = input("Enter your anonymous question: ")
    translated_q = detect_and_translate(question)
    if translated_q not in questions:
        questions[translated_q] = []
        save_question(translated_q)
        print("Question saved successfully.")
    else:
        print("This question already exists.")

def list_questions():
    """List all questions, view their answers, and add new answers."""
    if not questions:
        print("\nNo questions have been submitted yet.")
        return

    while True:
        print("\nList of Questions:")
        question_list = list(questions.keys())
        for idx, q in enumerate(question_list, 1):
            print(f"{idx}. {q}")

        choice = input("Enter the number of a question to view its answers (or '0' to return): ")
        if not choice.isdigit():
            print("Please enter a valid number.")
            continue
        num = int(choice)
        if num == 0:
            break
        if 1 <= num <= len(question_list):
            q = question_list[num - 1]
            answers = questions[q]
            print(f"\nAnswers for: {q}")
            if answers:
                for i, ans in enumerate(answers, 1):
                    print(f"Answer {i}: {ans}")
            else:
                print("No answers yet.")
            while True:
                add_ans = input("Do you want to add an answer to this question? (yes/no): ").strip().lower()
                if add_ans == "yes":
                    new_answer = input("Enter your answer: ")
                    questions[q].append(new_answer)
                    save_question(q, new_answer)
                    print("Answer added.")
                    # Show updated answers after adding
                    print(f"\nUpdated answers for: {q}")
                    for i, ans in enumerate(questions[q], 1):
                        print(f"Answer {i}: {ans}")
                    break
                elif add_ans == "no":
                    break
                else:
                    print("Please type 'yes' or 'no'.")
        else:
            print("Invalid number. Try again.")

def main():
    """Main program loop with menu and input validation."""
    # Load data from files on startup
    load_suggestions()
    load_questions()

    while True:
        print("\nMini Virtual Suggestion Box Menu")
        print("1. Submit a Suggestion")
        print("2. View Suggestion Summary")
        print("3. View a Random Suggestion")
        print("4. Submit a Question")
        print("5. List Questions and View/Add Answers")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()
        if choice == '1':
            add_suggestion()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            random_suggestion()
        elif choice == '4':
            add_question()
        elif choice == '5':
            list_questions()
        elif choice == '6':
            print("Thank you for using the Suggestion Box. Goodbye!")
            break
        else:
            print("Invalid input. Please enter a number from 1 to 6.")

        # Ask if user wants to return to menu or exit
        while True:
            cont = input("\nWould you like to return to the Main Menu? (yes/no): ").strip().lower()
            if cont == 'yes':
                break
            elif cont == 'no':
                print("Thank you for using the Suggestion Box. Goodbye!")
                return
            else:
                print("Please type 'yes' or 'no'.")

if __name__ == "__main__":
    main()
