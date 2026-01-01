# 📧 Easy Mail Librarian (EML)

> **Organize old emails like a library.** 

Easy Mail Librarian (EML) is a lightweight and fast **searching & viewing system** for `.eml` archives, featuring **FTS5-based full-text search**, **incremental indexing**, and **on-demand email expansion** from original files.

Refer to [docs/design.md](docs/design.md) for the design rational of this project.


## ✨ Introduction

This app is designed for users who need to manage or rediscover their archived emails:

*   📦 **Running out of IMAP storage?** — Free up space by moving old, untouched emails to local archives.
*   🚪 **Changed jobs or lost access?** — Keep a portable, searchable backup of emails from previous positions.
*   📂 **Proactive about digital hygiene?** — Create organized, local backups of your important correspondence.
*   🤔 **Unsure what to delete?** — Safely archive emails locally first, then decide what to keep without the pressure of limited server storage.
*   … and anyone who wants **instant, offline access** to their email history.

### 🚀 How It Works
1.  🗄️**Backup:** Export your emails as `.eml` files using your favorite email client (like Outlook, Thunderbird, Apple Mail, etc.) and save them to your local hard drive.
2.  🔎**Search & View:** Use this app to **instantly search** through your archive and view any email in detail—perfect for when you urgently need to find an old attachment, conversation, or piece of information.


### ✨ Features
* 🍥 **Simple functionality** simply update library and then search your cotents.
* 🔍 **Full-text search** powered by SQLite FTS5
  Search across subject, sender, recipients, and body content.

* 🧠 **Explicit indexing model**
  Clean separation between:

  * structured metadata (`emails` table)
  * search index (`emails_fts`)
  * original `.eml` files (source of truth)

* ⚡ **Fast, local, dependency-light** no internet connection needed

  * SQLite (no external DB)
  * Python backend (FastAPI)
  * Vanilla JS frontend

* 📂 **On-demand email expansion**

  * Search results are lightweight
  * Full email body is loaded only when a result is clicked

* 🧩 **Research-friendly architecture**

  * Deterministic behavior
  * Inspectable SQL
  * Reproducible indexing
  * No hidden caching layers

* 📱 **Flexible mobility** accessible by phones and tablets
---


## 🚝 Motivation

Modern information tools increasingly assume cloud connectivity, centralized services, and opaque automation.

This project started from a simple question:

> *Can a personal information system be powerful, searchable, and user-friendly—without giving up local control, transparency, or simplicity?*

Rather than building another platform, this project explores a different direction: **a small, self-contained system that does one thing well**, remains understandable, and respects the user’s autonomy. This project intentionally avoids:

* Heavy frontend frameworks
* Opaque indexing layers
* Implicit caching
* Email client abstractions

Instead, it emphasizes:

* **Traceability**
* **Determinism**
* **Minimal state**
* **Research reproducibility**

Ideal for:

* 📚 Academic email corpora
* 🔬 NLP / IR experiments
* 🛠️ Tooling for inspection and analysis
* 🧠 Systems research and prototyping


---

## ⚒️ Installation

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

(SQLite with FTS5 is required; most Python builds include it.)

---

### 2️⃣ Configure mail directory

In `backend/config.py`:

```python
# MAIL_ROOT: the path to your .eml archive. The app will recursively traverse all .eml files
MAIL_ROOT = Path("/path/to/eml/archive")

# DB_PATH: the path where you want to store the database
DB_PATH = Path("/path/to/eml/database.db")
```

---

## 🚀 Usage

### 1️⃣ Start the backend

Simply run
```powershell
# In Windows command prompt
.\scripts\run.bat
# In Linux
chmod +x ./scripts/run.sh
./scripts/run.sh
```
---

### 2️⃣ Open the frontend

Simply open `http://localhost:8000` in your browser. Click `Update Library` to initialize the database if you have not executed 3️⃣. Once done, you are ready to enjoy fast search and convenient viewing.

---

## 🔎 Search Behavior

* Choose a supported field:

  * Full text (`all`)
  * Subject
  * Sender
  * Recipients
  * Body

* Enter the keyword to search
* Click `Search` button
* Click any result to expand the full text

---

## 🖱️ Interactive Result Expansion

* Each search result is a **clickable bar**
* Clicking a result:

  * Loads the full email content from the original `.eml`
  * Expands inline
* Clicking again:

  * Folds the email body

This ensures:

* 🔒 No duplication of large email bodies
* 📈 Excellent scalability
* 🧪 Clear separation between indexing and presentation

---

## 🏗️ Architecture Overview

```text
.eml archive
   │
   ▼
[ indexer.py ]
   │  parses
   ▼
┌──────────────────┐
│ SQLite Database  │
│                  │
│  emails          │  ← structured storage
│  emails_fts      │  ← FTS5 index
└──────────────────┘
   ▲          │
   │          ▼
[ search.py ]   FTS MATCH
   │
   ▼
FastAPI backend
   │
   ▼
Minimal JS frontend
(click → expand → load full .eml)
```

---

## 🗄️ Database Design

### `emails` (source metadata)

| column     | description                    |
| ---------- | ------------------------------ |
| id         | primary key                    |
| path       | absolute path to `.eml` file   |
| subject    | decoded subject                |
| sender     | normalized sender email        |
| recipients | comma-separated recipients     |
| body       | plain-text body (for indexing) |

### `emails_fts` (FTS5 index)

* External content table (`content='emails'`)
* Indexed fields:

  * subject
  * sender
  * recipients
  * body
* Ranked using `bm25`

---

## 🧠 Design Rationale & Philosophy

### 🗃️ Local-First, by Design

This project adopts a local-first, developer-oriented approach to information management. All indexing, querying, and processing run entirely on the local machine—no cloud services, external APIs, or accounts required. This ensures data sovereignty, predictable offline behavior, long-term viability, and privacy by default.

### 🛠️ Compositional, Not Monolithic

The system is intentionally built from simple, well-understood components rather than a heavyweight framework:

* SQLite + FTS5 for robust full-text search with minimal operational cost
* A lightweight Python backend for orchestration and cross-platform extensibility
* A browser-based UI as a thin interaction layer, not a dependency

This separation enables independent evolution of subsystems, easier debugging, and clear reasoning about system behavior.

### 🔍 Clarity Over Convenience

Transparency and inspectability are favored over automation and hidden abstractions:

* Explicit workflows instead of opaque pipelines
* Inspectable data formats instead of black boxes
* Clear failure modes instead of silent errors
* Programmatic access as a first-class interface

The Web UI is optional; all core functionality remains directly accessible through code.

### 🤖 Intentional Scope

To maintain focus and reduce maintenance burden, the project deliberately excludes:

* User accounts and multi-user features
* Cloud synchronization
* Heavy customization frameworks
* Binary-only distribution

These constraints keep the system centered on correctness, clarity, and understandability rather than feature breadth.

### 🙋 Software as an Engineering Artifact

Beyond utility, the codebase is designed to be readable as an engineering narrative. Architectural decisions are reflected in directory structure, module boundaries, naming, and documentation that explains *why* choices were made—not just *what* they do.

The result is a lean, compositional system that delivers practical functionality while remaining transparent, inspectable, and instructive by design.


---


## 🧪 Debugging & Inspection

### Inspect tables

```bash
sqlite3 eml-search.db ".tables"
```

### Test FTS manually

```bash
sqlite3 eml-search.db \
  "SELECT subject FROM emails_fts WHERE emails_fts MATCH 'campus card';"
```

### Verify index integrity

```bash
INSERT INTO emails_fts(emails_fts) VALUES('rebuild');
```

---


## 🔮 Possible Extensions

* HTML email rendering (`text/html`)
* Threading / conversation grouping
* Attachment indexing
* Advanced FTS ranking or custom scoring
* Scenario-based or semantic search integration

---

## 🏁 Change Logs

### Unreleased changes

- Adding `frontend/favicon.ico`
- Updating new run scripts in `scripts/`

### Release v1.0.0

✅ Core functionality complete
✅ Stable indexing and search
✅ UI interaction fully working

This is a **solid, extensible foundation**, not a throwaway prototype. Any contribution is welcomed!

Made with ❤️ by **Paradoxsolver** (*paradoxsolver@hotmail.com*)
