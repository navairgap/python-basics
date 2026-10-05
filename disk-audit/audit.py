#!/usr/bin/env python3
"""disk-audit - find what's eating your disk. stdlib only."""

import argparse
import json
import os
import sys
from dataclasses import dataclass, field

EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".cache"}

@dataclass
class DirStat:
    path: str
    size: int = 0
    files: int = 0

def format_size(n):
    for unit in ["B", "K", "M", "G", "T"]:
        if n < 1024 or unit == "T":
            return f"{n}B" if unit == "B" else f"{n:.1f}{unit}"
        n /= 1024
