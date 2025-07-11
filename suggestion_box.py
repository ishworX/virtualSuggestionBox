"""
Mini Virtual Suggestion Box - Final Version 

Business Problem:
Many companies struggle to collect honest, anonymous employee feedback, especially in multinational environments where language barriers exist.  
Employees may fear judgment or repercussions, reducing valuable input that could improve workplace conditions and processes.

Features:
- Employees can submit anonymous suggestions and questions via a simple text menu.
- Suggestions can be entered in any language; the program automatically detects the 
  language and translates input to English.
- Each suggestion is analyzed for sentiment (positive, neutral, or negative), helping 
  management understand the tone behind the feedback.
- Suggestions are automatically categorized into business-relevant areas like Facility, 
  Work Process, or Benefits based on keywords, making it easier to identify patterns and prioritize action.
- Employees can also submit anonymous questions, view previously submitted questions, and 
  add multiple answers collaboratively, promoting transparency and shared knowledge.
- All suggestions and questions are saved persistently to text files (using JSON format for suggestions) 
  so the feedback remains available across program restarts, ensuring no data loss.
- An admin mode, protected by password, allows authorized personnel to view summaries, manage data, 
  and delete all stored feedback when necessary — adding a layer of security and control.
- The program includes robust input validation and error handling, ensuring smooth user experience without crashes.
- User prompts and outputs are designed to be clear and friendly, encouraging honest communication without 
  fear of judgment or exposure.

APIs Used:
- langdetect: Detects the language of input text  
- googletrans: Translates non-English input to English  
- TextBlob: Performs sentiment analysis on suggestions

How to Run:
1. Ensure Python 3 is installed.  
2. Install dependencies with:  
   pip install langdetect googletrans==4.0.0rc1 textblob  
3. Download required TextBlob corpora:  
   python -m textblob.download_corpora  
4. Run the program:  
   python suggestion_box.py  
5. Use the on-screen menu to submit/view suggestions and questions or enter admin mode.

Author: Ishwor Tandon
Date: May 21st 2025
"""

import random
import json
from langdetect import detect
from googletrans import Translator
from textblob import TextBlob
import os
import getpass

translator = Translator()

# Data storage
suggestions = []  # Each element: {'text': "...", 'sentiment': "Positive"/"Neutral"/"Negative"}
questions = {}    # dict: question -> list of answers

# Categorization
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

# Files
SUGGESTIONS_FILE = "suggestions.txt"
QUESTIONS_FILE = "questions.txt"

# Admin password (change as desired)
ADMIN_PASSWORD = "admin123"

# ------------------- File I/O -------------------

def load_suggestions():
    """Load saved suggestions from file (JSON lines) and categorize."""
    if os.path.exists(SUGGESTIONS_FILE):
        with open(SUGGESTIONS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        suggestion_entry = json.loads(line)
                        suggestions.append(suggestion_entry)
                        categorize_suggestion(suggestion_entry['text'])
                    except json.JSONDecodeError:
                        print("[Warning] Skipping invalid suggestion entry in file.")

def save_suggestion(suggestion):
    """Append a suggestion dict as a JSON string to the suggestions file."""
    with open(SUGGESTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(suggestion) + "\n")

# Load questions and answers from file into memory.
def load_questions():
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

# Append question and optional answer to file.
def save_question(question, answer=None):
    with open(QUESTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(f"Q: {question}\n")
        if answer is not None:
            f.write(f"A: {answer}\n")
        f.write("---\n")

def delete_all_data():
    """ Delete all stored suggestions and questions files and clear memory. """
    global suggestions, questions, categories
    suggestions.clear()
    questions.clear()
    for cat in categories:
        categories[cat].clear()
    if os.path.exists(SUGGESTIONS_FILE):
        os.remove(SUGGESTIONS_FILE)
    if os.path.exists(QUESTIONS_FILE):
        os.remove(QUESTIONS_FILE)
    print("All suggestions and questions deleted.")

# ------------------- Core Features -------------------

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
        print(f"[Warning] Language detection/translation failed: {e}")
        return text

def analyze_sentiment(text):
    """Return sentiment classification of text."""
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.1:
            return "Positive"
        elif polarity < -0.1:
            return "Negative"
        else:
            return "Neutral"
    except Exception as e:
        print(f"[Warning] Sentiment analysis failed: {e}")
        return "Neutral"

def categorize_suggestion(text):
    """Categorize suggestion and store it in categories dict."""
    text_lower = text.lower()
    for category, keywords in category_keywords.items():
        if any(k in text_lower for k in keywords):
            categories[category].append({'text': text})
            return category
    categories["Other"].append({'text': text})
    return "Other"

def add_suggestion():
    original = input("Enter your anonymous suggestion: ")
    translated = detect_and_translate(original)
    sentiment = analyze_sentiment(translated)
    suggestion_entry = {"text": translated, "sentiment": sentiment}
    suggestions.append(suggestion_entry)
    save_suggestion(suggestion_entry)
    category = categorize_suggestion(translated)
    print(f"\nSuggestion (translated): {translated}")
    print(f"Sentiment: {sentiment}")
    print(f"Categorized under: {category}")

def add_question():
    """Handle anonymous question input and processing."""
    question = input("Enter your anonymous question: ")
    translated_q = detect_and_translate(question)
    if translated_q not in questions:
        questions[translated_q] = []
        save_question(translated_q)
        print("Question saved successfully.")
    else:
        print("This question already exists.")

def list_questions():
    """List all questions; view and add answers."""
    if not questions:
        print("\nNo questions submitted yet.")
        return

    while True:
        print("\nList of Questions:")
        q_list = list(questions.keys())
        for idx, q in enumerate(q_list, 1):
            print(f"{idx}. {q}")

        choice = input("Enter question number to view answers or 0 to return: ").strip()
        if not choice.isdigit():
            print("Please enter a valid number.")
            continue
        num = int(choice)
        if num == 0:
            break
        if 1 <= num <= len(q_list):
            q = q_list[num - 1]
            answers = questions[q]
            print(f"\nAnswers for: {q}")
            if answers:
                for i, ans in enumerate(answers, 1):
                    print(f"Answer {i}: {ans}")
            else:
                print("No answers yet.")

            while True:
                add_ans = input("Add an answer? (yes/no): ").strip().lower()
                if add_ans == 'yes':
                    new_ans = input("Enter your answer: ")
                    questions[q].append(new_ans)
                    save_question(q, new_ans)
                    print("Answer added.")
                    break
                elif add_ans == 'no':
                    break
                else:
                    print("Please type 'yes' or 'no'.")
        else:
            print("Invalid question number.")

def view_summary():
    """Show counts of suggestions per category."""
    print("\nSuggestion Summary:")
    for category, items in categories.items():
        print(f"{category}: {len(items)}")

def view_suggestions_by_category():
    """
    Displays all suggestion categories along with how many suggestions each contains.
    Prompts the user to select a category to view its suggestions.
    For the chosen category, lists all suggestions with their associated sentiment (Positive, Neutral, Negative).
    Handles invalid inputs gracefully and allows the user to return to the previous menu.
    """
    categories_list = list(categories.keys())
    print("\nCategories and suggestion counts:")
    print("{:<5} {:<15} {}".format("No.", "Category", "Suggestion Count"))
    print("-" * 35)
    for i, cat in enumerate(categories_list, 1):
        count = len(categories[cat])
        print(f"{i:<5} {cat:<15} {count}")
    choice = input(f"\nChoose a category to view suggestions (1-{len(categories_list)}), or 0 to return: ").strip()
    if not choice.isdigit():
        print("Please enter a valid number.")
        return
    choice_num = int(choice)
    if choice_num == 0:
        return
    if 1 <= choice_num <= len(categories_list):
        selected_cat = categories_list[choice_num - 1]
        suggestions_in_cat = categories[selected_cat]
        if suggestions_in_cat:
            print(f"\nSuggestions under '{selected_cat}':")
            for i, suggestion_entry in enumerate(suggestions_in_cat, 1):
                # Find sentiment from main suggestions list by matching text
                sentiment = "Unknown"
                for sug in suggestions:
                    if sug['text'] == suggestion_entry['text']:
                        sentiment = sug.get('sentiment', 'Unknown')
                        break
                print(f"{i}. {suggestion_entry['text']} (Sentiment: {sentiment})")
        else:
            print(f"\nNo suggestions yet under '{selected_cat}'.")
    else:
        print("Invalid choice.")

# ------------------- Admin Functions -------------------

def admin_menu():
    """Admin-only menu with password protection."""
    pw = getpass.getpass("Enter admin password: ")
    if pw != ADMIN_PASSWORD:
        print("Incorrect password. Access denied.")
        return
    while True:
        print("\n--- Admin Menu ---")
        print("1. View Suggestion Summary")
        print("2. List Questions and Answers")
        print("3. Delete All Suggestions and Questions")
        print("4. Exit Admin Menu")
        choice = input("Choose an option (1-4): ").strip()
        if choice == '1':
            view_summary()
        elif choice == '2':
            list_questions()
        elif choice == '3':
            confirm = input("Are you sure? This will delete all data. (yes/no): ").strip().lower()
            if confirm == 'yes':
                delete_all_data()
            else:
                print("Deletion cancelled.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Enter 1-4.")

# ------------------- Main Loop -------------------

def main():
    # Load persisted data on program start
    load_suggestions()
    load_questions()

    while True:
        print("\nMini Virtual Suggestion Box Menu")
        print("1. Submit a Suggestion")
        print("2. View Suggestion Summary")
        print("3. View Suggestions by Category")  # updated menu text
        print("4. Submit a Question")
        print("5. List Questions and View/Add Answers")
        print("6. Exit")
        print("7. Admin Mode")

        choice = input("Choose an option (1-7): ").strip()

        if choice == '1':
            add_suggestion()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            view_suggestions_by_category()
        elif choice == '4':
            add_question()
        elif choice == '5':
            list_questions()
        elif choice == '6':
            print("Thank you for using the Suggestion Box. Goodbye!")
            break
        elif choice == '7':
            admin_menu()
        else:
            print("Invalid input. Please enter a number from 1 to 7.")

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
