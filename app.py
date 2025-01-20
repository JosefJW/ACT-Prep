import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import time
import os

# Connect to the database
connection = sqlite3.connect('questions.db')
cursor = connection.cursor()

# Function to get an unanswered question
def get_unanswered_question():
    cursor.execute("SELECT * FROM questions WHERE answer IS NULL LIMIT 1;")
    return cursor.fetchone()

# Function to get the passage content from the passages table
def get_passage(passage_id):
    cursor.execute("SELECT passage FROM passages WHERE id = ?;", (passage_id,))
    result = cursor.fetchone()
    return result[0] if result else None

# Function to update the database with the user's response
def record_response(question_id, selected_option, time_taken, confidence):
    cursor.execute(
        """
        UPDATE questions
        SET answer = ?, time = ?, confidence = ?
        WHERE id = ?;
        """,
        (selected_option, time_taken, confidence, question_id),
    )
    connection.commit()

# Function to submit the answer
def submit_answer():
    global start_time

    if selected_option.get() == 0:
        messagebox.showwarning("Warning", "Please select an option before submitting!")
        return

    end_time = time.time()
    time_taken = int(end_time - start_time)

    confidence = confidence_scale.get()

    record_response(current_question[0], selected_option.get(), time_taken, confidence)

    #messagebox.showinfo("Info", "Your response has been recorded!")
    window.destroy()
    main()

# Function to display a passage if it's an image file
def display_passage(passage):
    if passage.startswith("File "):
        filename = os.path.join("images", passage.split(" ", 1)[1])
        if os.path.exists(filename):
            image = Image.open(filename)
            image = image.resize((400, 300))#, Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image)

            img_label = tk.Label(window, image=img)
            img_label.image = img
            img_label.pack(pady=10)
        else:
            tk.Label(window, text="Image file not found.", font=("Arial", 12), fg="red").pack(pady=10)
    else:
        tk.Label(window, text=passage, wraplength=400, font=("Arial", 14)).pack(pady=10)

# Main function to display the question
def main():
    global window, selected_option, confidence_scale, start_time, current_question

    # Fetch an unanswered question
    current_question = get_unanswered_question()
    if not current_question:
        print("No unanswered questions available.")
        return

    window = tk.Tk()
    window.title("Quiz App")

    # Center the window on the screen
    window_width = 800  # Width of the window
    window_height = 800  # Height of the window
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int((screen_height / 2) - (window_height / 2))
    position_right = int((screen_width / 2) - (window_width / 2))
    window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    question_text = current_question[1]
    passage_id = current_question[9]  # Passage ID column
    choices = current_question[2:7]

    if passage_id:
        passage = get_passage(passage_id)
        if passage:
            display_passage(passage)

    tk.Label(window, text=question_text, wraplength=800, font=("Arial", 14)).pack(pady=10)

    selected_option = tk.IntVar()

    for i, choice in enumerate(choices, start=1):
        if choice:
            tk.Radiobutton(window, text=choice, variable=selected_option, value=i, font=("Arial", 12)).pack(anchor="w")

    tk.Label(window, text="Confidence (1 = Low, 5 = High):", font=("Arial", 12)).pack(pady=10)
    confidence_scale = tk.Scale(window, from_=1, to=5, orient="horizontal", font=("Arial", 10))
    confidence_scale.set(3)
    confidence_scale.pack()

    tk.Button(window, text="Submit", command=submit_answer, font=("Arial", 12)).pack(pady=20)

    start_time = time.time()
    window.mainloop()

# Run the main function
if __name__ == "__main__":
    main()

# Close the database connection when done
connection.close()
