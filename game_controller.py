from db import get_db
from datetime import datetime, UTC
import sqlite3


class GameError(Exception):
    def __init__(self, message, code=400):
        super().__init__(message)
        self.code = code


def validate_game(name, price, rate):
    errors = []
    if not name or len(name.strip()) == 0:
        errors.append("Name is required")
    if price is None or price < 0:
        errors.append("Price must be a positive number")
    if rate is None or not (1 <= rate <= 5):
        errors.append("Rate must be between 1 and 5")
    return errors


def insert_game(name, price, rate):
    errors = validate_game(name, price, rate)
    if errors:
        raise GameError(", ".join(errors), 400)
    
    try:
        db = get_db()
        cursor = db.cursor()
        now = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')
        statement = """
            INSERT INTO games(name, price, rate, created_at, updated_at) 
            VALUES (?, ?, ?, datetime('now'), datetime('now'))
        """
        cursor.execute(statement, [name, price, rate])
        db.commit()
        return get_by_id(cursor.lastrowid)
    except sqlite3.Error as e:
        raise GameError(f"Database error: {str(e)}", 500)


def update_game(id, name, price, rate):
    errors = validate_game(name, price, rate)
    if errors:
        raise GameError(", ".join(errors), 400)
    
    try:
        db = get_db()
        cursor = db.cursor()
        # Check if game exists
        cursor.execute("SELECT id FROM games WHERE id = ?", [id])
        if not cursor.fetchone():
            raise GameError("Game not found", 404)
        
        statement = """
            UPDATE games 
            SET name = ?, price = ?, rate = ?, updated_at = datetime('now') 
            WHERE id = ?
        """
        cursor.execute(statement, [name, price, rate, id])
        db.commit()
        return get_by_id(id)
    except sqlite3.Error as e:
        raise GameError(f"Database error: {str(e)}", 500)


def delete_game(id):
    try:
        db = get_db()
        cursor = db.cursor()
        # Check if game exists
        cursor.execute("SELECT id FROM games WHERE id = ?", [id])
        if not cursor.fetchone():
            raise GameError("Game not found", 404)
            
        statement = "DELETE FROM games WHERE id = ?"
        cursor.execute(statement, [id])
        db.commit()
        return {"message": "Game deleted successfully"}
    except sqlite3.Error as e:
        raise GameError(f"Database error: {str(e)}", 500)


def get_by_id(id):
    try:
        db = get_db()
        cursor = db.cursor()
        statement = """
            SELECT id, name, price, rate, 
                   created_at, updated_at 
            FROM games 
            WHERE id = ?
        """
        cursor.execute(statement, [id])
        game = cursor.fetchone()
        if not game:
            raise GameError("Game not found", 404)
        return dict(game)
    except sqlite3.Error as e:
        raise GameError(f"Database error: {str(e)}", 500)


def get_games():
    try:
        db = get_db()
        cursor = db.cursor()
        query = """
            SELECT id, name, price, rate, 
                   created_at, updated_at 
            FROM games 
            ORDER BY created_at DESC
        """
        cursor.execute(query)
        return [dict(game) for game in cursor.fetchall()]
    except sqlite3.Error as e:
        raise GameError(f"Database error: {str(e)}", 500)


def search_games(term):
    try:
        db = get_db()
        cursor = db.cursor()
        statement = """
            SELECT id, name, price, rate, 
                   created_at, updated_at 
            FROM games 
            WHERE name LIKE ?
            ORDER BY created_at DESC
        """
        cursor.execute(statement, [f"%{term}%"])
        return [dict(game) for game in cursor.fetchall()]
    except sqlite3.Error as e:
        raise GameError(f"Database error: {str(e)}", 500)
