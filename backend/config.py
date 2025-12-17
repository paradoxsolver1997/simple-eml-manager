# backend/config.py
from pathlib import Path

# user Documents Table of contents（Cross-platform）
DOCUMENTS = Path.home() / "Documents"

# EML storage location（you can Documents Create a subdirectory）
MAIL_ROOT = DOCUMENTS / "Mail"

# SQLite Database path
DB_PATH = MAIL_ROOT / "eml-search.db"