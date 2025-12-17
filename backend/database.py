# backend/database.py

import os
import sqlite3
from backend.config import DB_PATH


def connect():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    print("USING DB FILE:", os.path.abspath(DB_PATH))
    return conn


def init_db():
    conn = connect()
    cur = conn.cursor()

    # 1. main table：Real email data
    cur.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            subject TEXT,
            sender TEXT,
            recipients TEXT,
            body TEXT
        );
    """)

    # 2. FTS5 surface：Full text index（external content）
    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS emails_fts
        USING fts5(
            subject,
            sender,
            recipients,
            body,
            content='emails',
            content_rowid='id',
            tokenize='unicode61'
        );
    """)

    conn.commit()
    conn.close()

    print("Database initialized (emails + emails_fts)")
