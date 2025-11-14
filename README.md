# Question Answering System (CS480)

Question answering system using PostgreSQL and vector search.

Dataset source: https://www.kaggle.com/datasets/datagator/wikinews-article-dataset/data


## Dataset

Using `dataset/my_wikinews_subset.json` - 30 Wikinews articles with title, text, date, and categories.


## ER Diagram

Entities:
- User: id, name, email, username, password_hash, role, last_activity_ts
- Document: id, title, type, source, added_by, created_at, processed
- QueryLog: id, user_id, query_text, created_at

Relationship:
- QueryRetrieval: (query_id, document_id) tracks which documents were retrieved per query

Cardinality:
- User (1) → (M) Document, via `Document.added_by`
- User (1) → (M) QueryLog, via `QueryLog.user_id`
- QueryLog (M) ↔ (N) Document, via `QueryRetrieval`


## PostgreSQL Schema

Schema is in `setup.sql`.

Running it:

```bash
psql -U johne -d johne
```

Then in psql:
```sql
\i C:/Users/johne/cs480-question-answering-system/setup.sql
```

Verify:
```sql
\dt
```


## Phase 3: Vector Pipeline

### Install and Run

```bash
pip install -r requirements.txt
python query.py
```

### Implementation

#### Step 1: Text → Chunks (25 pts)
**Location:** `chunker.py` - `Chunker.chunk_text()`

Splits text into 500-char chunks with 50-char overlap.

Example:
```python
from chunker import Chunker

chunks = Chunker.chunk_text(text, chunk_size=500, overlap=50)
```

---

#### Step 2: Chunks → Vectors (25 pts)
**Location:** `embedder.py` - `Embedder` class

Model: `all-MiniLM-L6-v2` (384 dimensions)

Example:
```python
from embedder import Embedder

embedder = Embedder()
vector = embedder.embed("text")
```

---

#### Step 3: Vectors → VectorDB (25 pts)
**Location:** `vector_db.py` - `VectorDB` class

Uses FAISS with L2 distance.

Example:
```python
from vector_db import VectorDB

db = VectorDB(dimension=384)
db.add_vectors(embedder, texts, ids)
```

---

#### Step 4: Query → Retrieve (25 pts)
**Location:** `query.py` - `answer_query()` and `main()`

Embeds query, finds nearest neighbors, returns chunks.

Example:
```python
from query import answer_query

results = answer_query(db, embedder, "search query", top_k=3)
```


## Files

**Phase 3:**
- `chunker.py` - text chunking
- `embedder.py` - text embeddings
- `vector_db.py` - FAISS database
- `query.py` - main pipeline
- `parse_documents.py` - dataset utility

**Data:**
- `dataset/my_wikinews_subset.json` - 30 articles
- `megarhyme-wikinews.json` - full dataset

**Phase 2:**
- `setup.sql` - PostgreSQL schema
- `sql_schema.drawio` - ER diagram
- `sql_schema.png` - diagram image

**Config:**
- `requirements.txt` - dependencies
- `.gitignore` - git config
