# 📧 Easy Mail Librarian (EML)

**Organize old emails like a library.** 

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

## 📚 Philosophy

### 🗃️ Local First, Always

Your data should remain yours—stored locally, processed locally, and accessible without external dependencies.

This project does not require accounts, subscriptions, or network services. Everything runs on your machine, under your control.

---

### 🛠️ Simple Tools, Carefully Composed

Instead of complex stacks or large frameworks, the system is built on a small number of well-understood components:

* A lightweight local database
* Native full-text search
* A minimal Web UI for interaction

The goal is not novelty, but **reliability through restraint**.

---

### ⚖️ Lean, compositional system design.

The system deliberately reuses existing platforms and tools, clearly separating responsibilities: 

- Browser-based UI, allowing for easy extension with web pages and JS plugins
- Database-backed search over minimal metadata, and on-demand access to original .eml sources. 
- A lightweight Python backend orchestrates components, enabling cross-platform extensibility without unnecessary architectural complexity.

---

### 🔍 Transparency Over Automation

Automation is useful—but only when its behavior is understandable.

This project favors:

* Explicit workflows over hidden pipelines
* Inspectable data over black-box processing
* Clear failure modes over silent magic

Users should be able to reason about what the system is doing at every stage.

---

### 🙋 Designed for Curious Users

This tool is not optimized for mass adoption. It is designed for users who:

* Prefer tools they can understand
* Value control over convenience
* Enjoy exploring how systems work

If you like reading source code, tweaking behavior, or repurposing tools for your own workflows, this project is built with you in mind.

---


## 🚀 Getting Started

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

### 3️⃣ Build the index

```bash
python -m backend.indexer
```

This will:

* Parse all `.eml` files
* Populate `emails`
* Rebuild the FTS index

Alternatively, you can also build the database in the front-end at step 5️⃣.

---

### 4️⃣ Start the backend

```bash
uvicorn backend.api:app --reload
```
or simply run
```powershell
# In Windows Powershell
.\scripts\run.ps1
# In Linux
./scripts/run.sh
```
---

### 5️⃣ Open the frontend

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

## 🏁 Status

✅ Core functionality complete
✅ Stable indexing and search
✅ UI interaction fully working

This is a **solid, extensible foundation**, not a throwaway prototype. Any contribution is welcomed!

Made with ❤️ by **Paradoxsolver** (*paradoxsolver@hotmail.com*)
