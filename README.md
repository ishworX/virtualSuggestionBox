# 📝 Mini Virtual Suggestion Box 🗳️

## 🚩 Business Problem

Many companies struggle to collect honest, anonymous employee feedback 😶‍🌫️ because employees fear judgment or repercussions.  
Language barriers 🌐 in multinational workplaces also make it hard to gather and analyze feedback effectively.

---

## 🎯 Program Purpose

This Python program lets employees submit **anonymous suggestions and questions** in *any language*.  
It automatically:
- Detects language 🌍  
- Translates input to English 📝  
- Analyzes sentiment (positive, neutral, negative) 😊😐☹️  
- Categorizes feedback into business areas like Facility, Work Process, or Benefits 📂  
- Allows anonymous questions and lets users view/add multiple answers 💬  
- Stores all data persistently in files for continuity across sessions 💾  
- Provides a password-protected admin mode for secure management 🔒

This helps management better understand employee needs and improves workplace communication!

---

## ⚙️ Key Features

- ✉️ Submit anonymous suggestions & questions  
- 🌏 Auto language detection & translation with **`langdetect`** & **`googletrans`**  
- 🧠 Sentiment analysis using **`TextBlob`**  
- 📂 Categorization using keyword matching  
- 📊 View suggestion summaries and random suggestions  
- 🔍 View questions with multiple answers; add new answers  
- 💾 Persistent storage of suggestions and questions in text files  
- 🔐 Admin mode with password protection for viewing summaries and deleting data  
- 🚨 Robust input validation and error handling for smooth user experience

---

## 🐍 Python Concepts Demonstrated

- 📋 Lists & dictionaries for data storage  
- 🔄 Flow control (loops, conditionals) for program navigation  
- 🧩 Functions for modular, reusable code  
- 🔌 API integration for translation, language detection, and sentiment analysis  
- 📂 File I/O for data persistence  
- 🚨 Error handling and user input validation

---

## 📦 APIs and Libraries Used

- [`langdetect`](https://pypi.org/project/langdetect/): Detects input language  
- [`googletrans`](https://py-googletrans.readthedocs.io/en/latest/): Translates text  
- [`TextBlob`](https://textblob.readthedocs.io/en/dev/): Performs sentiment analysis

---

## 🚀 How to Run

1. Ensure Python 3 is installed 🐍  
2. Install dependencies:

   ```bash
   pip install textblob langdetect googletrans==4.0.0rc1
   python -m textblob.download_corpora

## Run the program:
 ```python suggestion_box.py
