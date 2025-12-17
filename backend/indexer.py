# backend/indexer.py
from pathlib import Path
from backend.config import MAIL_ROOT
from backend.database import connect, init_db
from backend.parser import parse_eml
from tqdm import tqdm
import sqlite3

from backend.update import update_lock
from backend.update import update_state

def rebuild_index():
    init_db()
    conn = None

    try:
        # Clear old index
        conn = connect()
        conn.execute("DELETE FROM emails;")
        conn.execute("DELETE FROM emails_fts;")
        conn.commit()
        
        with update_lock:
            update_state["status"] = "running"
            update_state["current"] = 0
            update_state["cancel_requested"] = False
            update_state["error"] = None

        count = 0
        
        eml_files = list(MAIL_ROOT.rglob("*.eml"))
        total = len(eml_files)
        print(f"Found {total} EML files. Start indexing...")

        

        with update_lock:
            update_state["total"] = len(eml_files)
            update_state["message"] = "Indexing emails"

        for eml in tqdm(eml_files, desc="Indexing emails"):

            with update_lock:
                if update_state["cancel_requested"]:
                    update_state["status"] = "cancelled"
                    break

            data = parse_eml(eml)
            conn.execute(
                """
                INSERT INTO emails (
                    path,
                    subject,
                    sender,
                    recipients,
                    body
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    data["path"],
                    data["subject"],
                    data["sender"],
                    data["recipients"],
                    data["body"],
                ),
            )

            count += 1

            with update_lock:
                update_state["current"] += 1


        with update_lock:
            update_state["status"] = "finished"
            if update_state["status"] == "cancelled":
                update_state["cancel_requested"] = False

        conn.execute(
            "INSERT INTO emails_fts(emails_fts) VALUES('rebuild');"
        )
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise

    finally:
        if conn:
            conn.close()

    return count