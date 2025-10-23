# Question Answering System (CS480)

This project builds a simple question‑answering (QA) system backed by a relational database. This README is written for beginners and walks through three things in order:

1) Dataset you’ll use for documents
2) The minimal ER diagram that matches the assignment
3) The exact PostgreSQL schema and how to run it on Windows using `psql`

Source credit for the original dataset: megarhyme-wikinews.json from Kaggle
https://www.kaggle.com/datasets/datagator/wikinews-article-dataset/data


## 1) Dataset

- We use a small subset of Wikinews articles saved at `dataset/my_wikinews_subset.json`.
- Each entry roughly has:
	- `title` (string)
	- `text` (string)
	- `date` (YYYY‑MM‑DD)
	- `categories` (array of strings)

You can browse it in VS Code: `dataset/my_wikinews_subset.json`.


## 2) Minimal ER diagram (what the assignment requires)

We intentionally keep the ERD minimal so it exactly satisfies the rubric.

Entities:
- User: id, name, email, username, password_hash, role, last_activity_ts
- Document: id, title, type, source, added_by, created_at, processed
- QueryLog: id, user_id, query_text, created_at

Relationship (junction table):
- QueryRetrieval: (query_id, document_id) records which documents were retrieved for a given query.

Cardinality:
- User (1) → (M) Document, via `Document.added_by`
- User (1) → (M) QueryLog, via `QueryLog.user_id`
- QueryLog (M) ↔ (N) Document, resolved by `QueryRetrieval (query_id, document_id)`

Notes:
- The assignment says “record the IDs of the retrieved documents” for each query. That is exactly what `QueryRetrieval` does.
- We do NOT include extra tables like Chunk or Category here to keep grading simple.


## 3) PostgreSQL schema (matches the ER diagram exactly)

Create a file `setup.sql` in the project root (we already use this filename below). This script is PostgreSQL‑specific and can be re‑run safely. Tested on PostgreSQL 16.

```sql
BEGIN;

-- For UUIDs via gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Drop in dependency order for easy re-runs (optional but convenient)
DROP TABLE IF EXISTS queryretrieval, querylog, document, "user" CASCADE;

-- NOTE: "user" is reserved in SQL, so we quote it.
CREATE TABLE "user" (
	id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	name text NOT NULL,
	email text NOT NULL UNIQUE,
	username text NOT NULL UNIQUE,
	password_hash text NOT NULL,
	role text NOT NULL, -- 'admin' | 'curator' | 'enduser'
	last_activity_ts timestamptz
);

CREATE TABLE document (
	id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	title text NOT NULL,
	type text,
	source text,
	added_by uuid NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
	created_at timestamptz NOT NULL DEFAULT now(),
	processed boolean NOT NULL DEFAULT false
);

CREATE TABLE querylog (
	id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	user_id uuid REFERENCES "user"(id) ON DELETE SET NULL,
	query_text text NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now()
);

-- Junction table for QueryLog (M) ↔ (N) Document
CREATE TABLE queryretrieval (
	query_id uuid NOT NULL REFERENCES querylog(id) ON DELETE CASCADE,
	document_id uuid NOT NULL REFERENCES document(id) ON DELETE CASCADE,
	PRIMARY KEY (query_id, document_id)
);

-- Helpful indexes (optional)
CREATE INDEX IF NOT EXISTS idx_document_added_by ON document(added_by);
CREATE INDEX IF NOT EXISTS idx_querylog_user ON querylog(user_id);

COMMIT;
```


### How to run the schema on Windows (psql)

1) Open a terminal (Command Prompt) and connect to your DB (replace names if needed):

```bat
psql -U johne -d johne
```

2) From inside `psql`, run the script by path (use forward slashes or double backslashes):

```sql
\i C:/Users/johne/cs480-question-answering-system/setup.sql
```

3) Verify tables exist:

```sql
\dt
\d "user"
\d document
\d querylog
\d queryretrieval
```


### psql quick reference

- `\dt` list tables

- `main.py` — future place for app logic/scripts
- `dataset/my_wikinews_subset.json` — sample documents
- `megarhyme-wikinews.json` — original large dataset (reference)
- `setup.sql` — PostgreSQL schema matching the ER diagram (run with `\i` in psql)
