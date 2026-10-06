import sqlite3
import hashlib

DATABASE_NAME = "career_ai.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            education TEXT DEFAULT '',
            skills TEXT DEFAULT '',
            interests TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessment_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill TEXT NOT NULL,
            score REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_careers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            career TEXT NOT NULL,
            match_score REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()


def register_user(name, email, password):
    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = hash_password(password)

    try:
        cursor.execute("""
            INSERT INTO users (
                name,
                email,
                password
            )
            VALUES (?, ?, ?)
        """, (
            name.strip(),
            email.strip().lower(),
            hashed_password
        ))

        connection.commit()

        return True, "Registration successful."

    except sqlite3.IntegrityError:
        return False, "This email is already registered."

    except Exception as error:
        return False, f"Registration error: {error}"

    finally:
        connection.close()


def login_user(email, password):
    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            education,
            skills,
            interests
        FROM users
        WHERE email = ?
        AND password = ?
    """, (
        email.strip().lower(),
        hashed_password
    ))

    user = cursor.fetchone()

    connection.close()

    return user


def get_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            education,
            skills,
            interests
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    connection.close()

    return user


def update_profile(
    user_id,
    education,
    skills,
    interests
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET
            education = ?,
            skills = ?,
            interests = ?
        WHERE id = ?
    """, (
        education,
        skills,
        interests,
        user_id
    ))

    connection.commit()
    connection.close()


def save_assessment_result(
    user_id,
    skill,
    score
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO assessment_results (
            user_id,
            skill,
            score
        )
        VALUES (?, ?, ?)
    """, (
        user_id,
        skill,
        score
    ))

    connection.commit()
    connection.close()


def get_assessment_results(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            skill,
            score,
            created_at
        FROM assessment_results
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))

    results = cursor.fetchall()

    connection.close()

    return results


def save_career_recommendation(
    user_id,
    career,
    match_score
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO user_careers (
            user_id,
            career,
            match_score
        )
        VALUES (?, ?, ?)
    """, (
        user_id,
        career,
        match_score
    ))

    connection.commit()
    connection.close()


def get_career_recommendations(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            career,
            match_score,
            created_at
        FROM user_careers
        WHERE user_id = ?
        ORDER BY match_score DESC
    """, (user_id,))

    careers = cursor.fetchall()

    connection.close()

    return careers