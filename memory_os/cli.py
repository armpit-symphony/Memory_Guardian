"""CLI for Memory Guardian."""

import argparse
import json
import sys
from pathlib import Path

from memory_os import __version__
from memory_os.api import MemoryGuardian
from memory_os.config import Config


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="memory-guardian",
        description="Memory OS - Persistent memory for AI agents"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--data-dir", type=Path, help="Data directory path")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Remember command
    remember_parser = subparsers.add_parser("remember", help="Store something in memory")
    remember_parser.add_argument("content", help="Content to remember")
    remember_parser.add_argument("--role", default="user", help="Role (user/assistant/system)")
    remember_parser.add_argument("--session", help="Session ID")
    
    # Recall command
    recall_parser = subparsers.add_parser("recall", help="Search memory")
    recall_parser.add_argument("query", help="Search query")
    recall_parser.add_argument("--limit", type=int, default=10, help="Max results")
    
    # Recent command
    recent_parser = subparsers.add_parser("recent", help="Get recent memories")
    recent_parser.add_argument("-n", "--count", type=int, default=10, help="Number of memories")
    recent_parser.add_argument("--session", help="Session ID filter")
    
    # Context command
    context_parser = subparsers.add_parser("context", help="Get packed context block")
    context_parser.add_argument("query", help="Search query")
    context_parser.add_argument("--limit", type=int, default=10, help="Max events")
    
    # Consolidate command
    subparsers.add_parser("consolidate", help="Run consolidation job")
    
    # Status command
    subparsers.add_parser("status", help="Show memory status")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize
    config = Config(data_dir=str(args.data_dir)) if args.data_dir else Config()
    mg = MemoryGuardian(config)
    
    # Execute command
    if args.command == "remember":
        event = mg.remember(args.content, role=args.role, session_id=args.session)
        print(json.dumps({"id": event.id, "status": "stored"}))
    
    elif args.command == "recall":
        events = mg.recall(args.query, limit=args.limit)
        for e in events:
            print(f"[{e.timestamp.strftime('%H:%M')}] {e.role or e.type.value}: {e.content}")
    
    elif args.command == "recent":
        events = mg.recall_recent(n=args.count, session_id=args.session)
        for e in events:
            print(f"[{e.timestamp.strftime('%H:%M')}] {e.role or e.type.value}: {e.content}")
    
    elif args.command == "context":
        context = mg.get_context(args.query, limit=args.limit)
        print(context)
    
    elif args.command == "consolidate":
        result = mg.consolidate()
        print(json.dumps(result, indent=2))
    
    elif args.command == "status":
        status = mg.status()
        print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
