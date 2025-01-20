import sqlite3

def reset_responses(database_path):
    """
    Reset answer, time, and confidence columns to NULL for all rows in the questions table.

    Parameters:
        database_path (str): Path to the SQLite database file.
    """
    try:
        # Connect to the database
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # Update the questions table
        cursor.execute("""
            UPDATE questions
            SET answer = NULL, time = NULL, confidence = NULL;
        """)
        connection.commit()

        print("All responses have been reset.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the connection is closed
        connection.close()

# Example usage
if __name__ == "__main__":
    reset_responses('questions.db')
