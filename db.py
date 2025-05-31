import sqlite3
from datetime import datetime
from flask import current_app, g

def get_db():
    db_name = getattr(current_app.config, 'DATABASE_NAME', 'games.db')
    conn = sqlite3.connect(db_name)
    
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    conn.row_factory = dict_factory
    return conn

def create_tables():
    # Drop existing tables first to ensure clean state
    tables = [
        """DROP TABLE IF EXISTS games""",
        """CREATE TABLE games(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            rate INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )"""
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
    db.commit()
