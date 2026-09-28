#!/usr/bin/env python3
"""todo-cli - a json-backed todo list. stdlib only."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STORE = Path(__file__).with_name("todo.json")


def load():
    if STORE.exists():
        return json.loads(STORE.read_text())
    return []


def save(items):
    STORE.write_text(json.dumps(items, indent=2) + "\n")


def add(text):
    items = load()
    items.append({"task": text, "done": False,
                  "created": datetime.now(timezone.utc).isoformat()[:16]})
    save(items)
    return len(items)


def ls(show_all=False):
    items = load()
    rows = [(i + 1, it) for i, it in enumerate(items) if show_all or not it["done"]]
    for n, it in rows:
        mark = "x" if it["done"] else " "
        print(f"[{mark}] {n:>2}  {it['task']}  ({it['created']})")
    if not rows:
        print("nothing here. enjoy it or add something.")


def done(n, value=True):
    items = load()
    items[n - 1]["done"] = value
    save(items)


def rm(n):
    items = load()
    removed = items.pop(n - 1)
    save(items)
    return removed["task"]


def main():
    ap = argparse.ArgumentParser(prog="todo")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add")
    p_add.add_argument("text")
    p_ls = sub.add_parser("ls")
    p_ls.add_argument("-a", "--all", action="store_true")
    for name in ("done", "undone", "rm"):
        sub.add_parser(name).add_argument("n", type=int)
    a = ap.parse_args()

    if a.cmd == "add":
        print(f"added #{add(a.text)}")
    elif a.cmd == "ls":
        ls(a.all)
    elif a.cmd in ("done", "undone"):
        done(a.n, a.cmd == "done")
    elif a.cmd == "rm":
        try:
            print(f"removed: {rm(a.n)}")
        except IndexError:
            sys.exit(f"no item #{a.n}")


if __name__ == "__main__":
    main()
