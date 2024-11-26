import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the database and create the users table if it doesn't exist
def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            age INTEGER,
            college TEXT,
            major TEXT,
            classes TEXT,
            hobbies TEXT,
            session INTEGER DEFAULT 1
        )
    ''')

    conn.commit()
    conn.close()

def delete_user_by_email(email):
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Delete the user with the matching email
    cursor.execute('DELETE FROM users WHERE email = ?', (email,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    
def add_user(name, email, password, age, college, major, classes, hobbies):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO users (name, email, password, age, college, major, classes, hobbies)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, password, age, college, major, classes, hobbies))

    conn.commit()
    conn.close()

# Verify login credentials
def verify_login(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM users WHERE email = ? AND password = ?
    ''', (email, password))
    user = cursor.fetchone()

    conn.close()
    return user is not None

# Update the session data (if necessary)
def update_session(email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users SET session = session + 1 WHERE email = ?
    ''', (email,))

    conn.commit()
    conn.close()

# Fetch user data by email (including additional fields)
def get_user_by_email(email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()

    conn.close()
    return user

def update_user_info(email, age, college, major, classes, hobbies):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users
        SET age = ?, college = ?, major = ?, classes = ?, hobbies = ?
        WHERE email = ?
    ''', (age, college, major, classes, hobbies, email))

    conn.commit()
    conn.close()
