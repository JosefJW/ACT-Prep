import tkinter as tk
import sqlite3

connection = sqlite3.connect('questions.db')
cursor = connection.cursor()

def create_tables():
    cursor.execute("""
    CREATE TABLE questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        choice1 TEXT,
        choice2 TEXT,
        choice3 TEXT,
        choice4 TEXT,
        choice5 TEXT,
        correctChoice INT,
        answer INT,
        passage INT,
        subject TEXT,
        time INT,
        confidence INT
    );""")

    connection.commit()

    cursor.execute("""
    CREATE TABLE passages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        passage TEXT
    );""")
    connection.commit()

insert_query = """
INSERT INTO questions (
    question, choice1, choice2, choice3, choice4, choice5, correctChoice, passage, subject
) VALUES (
    ?, ?, ?, ?, ?, ?, ?, ?, ?
);
"""

data = (
    "Ray PK bisects angle LPM, the measure of angle LPM is 11x deg, and the measure of angle LPK is (4x+18) deg. What is the measure of angle KPM?", # Question
    "12 deg", # Choice 1
    "28 and 2/7 deg", # Choice 2
    "42 deg", # Choice 3
    "61 and 1/5 deg", # Choice 4
    "66 deg", # Choice 5
    5, # Correct choice
    0, # Passage num
    "Math", # Subject
)

# insert_query = """
# INSERT INTO passages (
#     passage
# ) VALUES (
#      ?           
# );
# """

# data = ("File Math49.png",)

cursor.execute(insert_query, data)

connection.commit()