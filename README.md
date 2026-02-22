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

```bash
python -m memory_os.cli status --data-dir ./data
python -m memory_os.cli remember --data-dir ./data --session test_session --role HUMAN --content "Phil wants boring progressive growth."
python -m memory_os.cli recall --data-dir ./data --session test_session --query "growth" --k 8
python -m memory_os.cli context --data-dir ./data --session test_session --query "What is Phil focused on?" --k 8 --budget 900
python -m memory_os.cli consolidate --data-dir ./data --session test_session
```

## Commands Explained

| Command | Purpose |
|---------|---------|
| `status` | Show memory stats (total events, data dir, max tokens) |
| `remember` | Store an event in the ledger |
| `recall` | Search memory using FTS |
| `context` | Build a token-bounded context block for LLM injection |
| `consolidate` | Extract facts and create daily summaries |

---

# Programmatic Usage

```python
from memory_os.api import MemoryGuardian
from memory_os.config import Config

config = Config(data_dir="./data")
memory = MemoryGuardian(config)

# Remember something
memory.remember_message(
    role="HUMAN",
    content="We want stable infrastructure growth.",
    session_id="room_1"
)

# Get context for LLM
context = memory.get_context(
    query="What are we optimizing for?",
    limit=8
)

print(context)
```

---

# Consolidation

Consolidation extracts durable facts and creates daily summaries.

```bash
python -m memory_os.cli consolidate --data-dir ./data --session test_session
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
