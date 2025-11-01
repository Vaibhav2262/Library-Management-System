# Library-Management-System

📚 Library Management System (Python)

🚀 Project Overview
This is a console-based Library Management System built using Python.
It allows Owners and Students to manage books, issue & return records, and late fee calculation — all stored using simple text files.

🎯 Objectives

Manage books: add, delete, update, view

Maintain issued book records with issue & return dates

Auto-calculate late fees based on return delay

Allow students to issue & return books easily

Provide owner with full control over library database

📈 Key Features

✅ Add, delete & update books
✅ Separate menus for Owner & Student
✅ Auto-generated text files for data storage (books.txt, issued.txt)
✅ 7-day return policy with ₹100/day fine
✅ Preloaded default 5 books on first run
✅ Error handling for invalid inputs

🛠️ Tech Stack
Component	Used
Language	Python
Storage	Text Files (.txt files)
Modules	datetime, timedelta
Interface	Console (CLI)

🔍 Use Cases
📌 Small library or book rental shop system
📌 Learning basic CRUD operations in Python

📂 Project Structure
Library-Management-System/
│
├── library.py        # Main application file
├── books.txt         # Auto-generated book database
├── issued.txt        # Auto-generated issued record database
└── README.md         # Documentation

🔮 Future Scope
🔹 Replace text files with database (MySQL / SQLite)
🔹 Add user login system (admin + student)
🔹 Add book search & filtering options
