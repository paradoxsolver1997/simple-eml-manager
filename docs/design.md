
# Design Rationale

This project was designed as a **local-first, developer-oriented information management tool**, with the explicit goal of balancing **power, transparency, and long-term maintainability**.

## Design Philosophy

Rather than optimizing for mass-market usability or commercial distribution, the design prioritizes **inspectability, composability, and engineering clarity**, making the system suitable as both a practical tool and a demonstrable software artifact.

---

### 1. Local-First by Design

All data processing, indexing, and querying are performed **entirely on the local machine**.

This decision was driven by several considerations:

* **Privacy and data ownership**: No external services, APIs, or cloud dependencies are required.
* **Deterministic behavior**: The system remains usable offline and behaves predictably across environments.
* **Longevity**: A local-first architecture avoids vendor lock-in and external service deprecation.

This aligns with the philosophy that personal knowledge and archives should remain **under the user’s direct control**, both technically and conceptually.

---

### 2. Explicit Separation of Concerns

The system is structured around a clear separation between:

* **Data ingestion and indexing**
* **Search and retrieval logic**
* **Presentation layer (Web UI)**

This separation enables:

* Independent evolution of each subsystem
* Easier debugging and profiling
* Clear reasoning about system behavior

In particular, the Web UI is treated strictly as a **thin interaction layer**, not as the core of the system. All essential functionality remains accessible programmatically.

---

### 3. Choice of SQLite + FTS5

SQLite with FTS5 was deliberately chosen instead of heavier search stacks (e.g., Elasticsearch or external indexing services).

Rationale:

* **Zero operational overhead**
* **Mature, well-tested full-text search capabilities**
* **Excellent performance for single-user and moderate-scale datasets**
* **Transparent storage format that can be inspected and queried directly**

This choice reflects a preference for **simple, robust primitives** over distributed systems that introduce unnecessary complexity for the problem scope.

---

### 4. Web UI as an Interface, Not a Platform

The Web UI exists to improve discoverability and interaction, not to redefine the system as a web application.

Key principles:

* The UI is optional, not mandatory
* The application runs locally and exposes a browser-based interface for convenience
* No authentication, accounts, or persistent sessions are required

This design allows users to benefit from modern UI affordances while retaining the simplicity and debuggability of a local tool.

---

### 5. Scope Control and Intentional Non-Features

Several features were consciously excluded:

* User accounts or multi-user support
* Cloud synchronization
* Heavy customization frameworks
* Binary-only distribution as a primary delivery method

These omissions are intentional. They reduce maintenance burden and keep the project focused on **clarity and correctness**, rather than surface-level feature expansion.

---

### 6. Software as a Communicable Artifact

Beyond functionality, this project is intended to be **readable as an engineering narrative**.

Design choices are reflected clearly in:

* Directory structure
* Module boundaries
* Configuration interfaces
* Documentation and comments

The codebase is meant to communicate *why* decisions were made, not just *what* the system does.

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
