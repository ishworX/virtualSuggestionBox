"""
Mini Virtual Suggestion Box 

Features implemented:
- Submit anonymous suggestions with language detection, translation, sentiment analysis, and categorization
- Submit anonymous questions with simple duplicate check
- Basic menu navigation with flow control

This code demonstrates key Python concepts: lists, dictionaries, functions, flow control,
and simple API usage (langdetect, googletrans, TextBlob).
"""

from langdetect import detect
from googletrans import Translator
from textblob import TextBlob

# Initialize translator object for Google Translate
translator = Translator()

# Data structures to hold suggestions and questions
suggestions = []  # List to store translated suggestions
questions = {}    # Dictionary: question (string) mapped to list of answers

# Categories for suggestions with empty lists to store categorized suggestions
categories = {
    "Facility": [],
    "Work Process": [],
    "Benefits": [],
    "Other": []
}

# Keywords to help categorize suggestions by topic
category_keywords = {
    "Facility": ["office", "room", "desk", "chair", "light", "building"],
    "Work Process": ["workflow", "schedule", "process", "meeting", "task", "communication"],
    "Benefits": ["bonus", "leave", "health", "insurance", "raise", "salary"]
}

def detect_and_translate(text):
    """
    Detects the language of the input text.
    If the text is not in English, translates it to English using Google Translate API.
    Returns the translated text or original if already in English.
    Includes error handling in case detection or translation fails.
    """
    try:
        lang = detect(text)
        if lang != 'en':
            translated = translator.translate(text, dest='en')
            return translated.text
        else:
            return text
    except Exception as e:
        print(f"[Error] Language detection or translation failed: {e}")
        return text  # Return original text on failure

def analyze_sentiment(text):
    """
    Performs sentiment analysis on the input English text using TextBlob.
    Returns a string indicating whether sentiment is 'Positive', 'Neutral', or 'Negative'
    based on polarity score.
    """
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
    """
    Categorizes a suggestion based on the presence of keywords.
    Adds the suggestion to the appropriate category list.
    Returns the name of the category assigned.
    If no keywords match, categorizes under 'Other'.
    """
    text_lower = text.lower()
    for category, keywords in category_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            categories[category].append(text)
            return category
    categories["Other"].append(text)
    return "Other"

def add_suggestion():
    """
    Prompts the user to input an anonymous suggestion.
    Processes the suggestion by translating (if needed), analyzing sentiment,
    categorizing, and storing it.
    Prints out the processed suggestion details.
    """
    original = input("Enter your anonymous suggestion: ")
    translated = detect_and_translate(original)
    sentiment = analyze_sentiment(translated)
    suggestions.append(translated)
    category = categorize_suggestion(translated)
    print(f"Suggestion (translated): {translated}")
    print(f"Sentiment: {sentiment}")
    print(f"Categorized under: {category}")

def add_question():
    """
    Prompts the user to input an anonymous question.
    Translates question to English (if needed).
    Checks for duplicates; if new, adds the question to the dictionary with an empty answers list.
    Notifies user about success or duplicate.
    """
    question = input("Enter your anonymous question: ")
    translated_q = detect_and_translate(question)

    if translated_q not in questions:
        questions[translated_q] = []
        print("Question saved successfully.")
    else:
        print("This question already exists.")

def main():
    """
    Main loop presenting a menu to the user.
    Allows submission of suggestions or questions or exiting the program.
    Handles invalid inputs gracefully.
    """
    while True:
        print("\nMini Virtual Suggestion Box")
        print("1. Submit a Suggestion")
        print("2. Submit a Question")
        print("3. Exit")

        choice = input("Choose an option (1-3): ")

        if choice == '1':
            add_suggestion()
        elif choice == '2':
            add_question()
        elif choice == '3':
            print("Thank you for using the Suggestion Box. Goodbye!")
            break
        else:
            print("Invalid input. Please enter 1, 2 or 3.")

if __name__ == "__main__":
    main()
