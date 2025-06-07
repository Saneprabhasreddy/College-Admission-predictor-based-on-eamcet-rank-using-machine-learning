import mysql.connector

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Prabhas@123",
            database="users"
        )
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None  # Return None if DB fails


def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize the table when the script runs
if __name__ == "__main__":
    create_table()
    print("Database initialized successfully.")
