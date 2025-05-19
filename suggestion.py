"""
Mini Virtual Suggestion Box 

we create:
- The main menu loop with flow control
- Data structures for suggestions and categories
- The 'Submit a Suggestion' feature (basic, no translation or sentiment analysis yet)
- Functions to add suggestions and categorize them by keywords
- Comments explaining the code and functions
"""

# Data structures
suggestions = []  # List to store suggestion texts

# Dictionary to categorize suggestions; each category stores list of suggestions
categories = {
    "Facility": [],
    "Work Process": [],
    "Benefits": [],
    "Other": []
}

# Keywords to help categorize suggestions
category_keywords = {
    "Facility": ["office", "room", "desk", "chair", "light", "building"],
    "Work Process": ["workflow", "schedule", "process", "meeting", "task", "communication"],
    "Benefits": ["bonus", "leave", "health", "insurance", "raise", "salary"]
}

def categorize_suggestion(text):
    """
    Categorize a suggestion based on presence of keywords.
    Returns the category name, and appends the suggestion to that category list.
    If no keywords match, categorizes as 'Other'.
    """
    text_lower = text.lower()
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                categories[category].append(text)
                return category
    categories["Other"].append(text)
    return "Other"

def add_suggestion():
    """
    Prompts the user to enter a suggestion.
    Adds the suggestion to the general list and categorizes it.
    Displays confirmation and the category.
    """
    suggestion = input("Enter your anonymous suggestion: ")
    suggestions.append(suggestion)
    category = categorize_suggestion(suggestion)
    print(f"Thank you! Your suggestion has been categorized under: {category}")

def main():
    """
    Main program loop showing menu options.
    Allows user to submit suggestions or exit.
    """
    while True:
        print("\nMini Virtual Suggestion Box ")
        print("1. Submit a Suggestion")
        print("2. Exit")

        choice = input("Choose an option (1-2): ")
        if choice == '1':
            add_suggestion()
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
