#!/usr/bin/env python3
"""serveit - dead-simple static file server. stdlib only."""

import argparse
import functools
import http.server
import os
import sys

QUIET = False

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        if not QUIET:
            super().log_message(fmt, *args)
