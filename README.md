# Memory Guardian — Memory OS MVP

Memory OS is a production-ready memory subsystem designed for autonomous agents. It provides durable long-term memory, hybrid retrieval, consolidation, and context packing for safe LLM injection.

This MVP implements the four core pillars:

- ✅ Append-only event ledger
- ✅ Full-text search (FTS) retrieval
- ✅ Memory consolidation (daily summaries + durable facts)
- ✅ Token-bounded context packing

---

# Architecture Overview

Memory OS follows a file-first, agent-safe design:

```
memory_guardian/
├── pyproject.toml
├── data/
│   ├── memory/           # ledger.jsonl (append-only source of truth)
│   ├── daily/           # YYYY-MM-DD.md summaries
│   └── indexes/         # fts.sqlite, embed.sqlite
└── memory_os/
    ├── api.py           # Public API surface
    ├── cli.py           # CLI entrypoint
    ├── config.py
    ├── schemas.py
    ├── ledger.py
    ├── index_fts.py
    ├── index_embed.py
    ├── consolidate.py
    ├── retrieve.py
    └── pack.py
```

**Design principles:**

- Append-only source of truth
- Read-only retrieval for LLMs
- No tool execution from memory
- Bounded token injection
- Session-scoped by default

---

# Installation

From inside the repository:

```bash
pip install -e .
```

---

# Quick Start

## 1) Initialize Memory

```bash
python -m memory_os.cli init
```

Creates:

- `ledger.jsonl`
- FTS index
- data folders

## 2) Record an Event

```bash
python -m memory_os.cli record \
  --session test_session \
  --role HUMAN \
  --content "Phil wants boring progressive growth."
```

This appends to the ledger and indexes the content.

## 3) Search Memory

```bash
python -m memory_os.cli search \
  --session test_session \
  --query "growth strategy"
```

Returns ranked results from FTS (and embeddings if enabled).

## 4) Build a Context Block

```bash
python -m memory_os.cli context \
  --session test_session \
  --query "What is Phil focused on?" \
  --k 8 \
  --budget 900
```

Outputs a token-bounded context block safe for injection into an LLM prompt.

---

# Programmatic Usage

```python
from memory_os.api import MemoryOS
from memory_os.config import MemoryConfig

cfg = MemoryConfig()
memory = MemoryOS(cfg)

memory.record_event(
    session_id="room_1",
    role="HUMAN",
    content="We want stable infrastructure growth."
)

context_block = memory.build_context_block(
    session_id="room_1",
    user_query="What are we optimizing for?"
)

print(context_block)
```

---

# Consolidation

Consolidation extracts durable facts and creates daily summaries.

Run manually:

```bash
python -m memory_os.cli consolidate --session test_session
```

**Recommended:**

- Run hourly
- Or every N conversation turns
- Or via background worker

---

# Security Model

Memory OS is designed to prevent agent compromise:

- Memory retrieval is treated as data, not instructions.
- No automatic tool execution.
- Session-scoped retrieval by default.
- No environment variable storage.
- Token budget enforced during context packing.

---

# Roadmap

Planned v1 upgrades:

- Semantic embeddings ranking
- Graph-based entity memory
- Cross-session recall policies
- Reranker model integration
- Multi-agent shared memory mesh
- Memory decay + importance scoring
- Retrieval confidence scoring

---

# Philosophy

Memory OS is not a vector store. It is a memory operating system for agents. It enables:

- Persistent cognition
- Long-horizon planning
- Context compression
- Safer autonomous operation

---

# Status

Memory OS MVP — Operational

Designed for integration into OpenClaw, Sparkbot, and autonomous agent stacks.

---

**Built for durable autonomous systems.**
