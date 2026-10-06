#!/usr/bin/env python3
"""netcheck - small network diagnostics. stdlib only."""

import argparse
import socket
import sys
import time
import urllib.request

DEFAULT_TIMEOUT = 3

def check_port(host, port, timeout=DEFAULT_TIMEOUT):
    """return (ok, latency_ms) for a TCP connect."""
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, round((time.perf_counter() - start) * 1000, 1)
    except OSError:
        return False, None

def dns_time(host):
    """resolve a host, return ms or None."""
    start = time.perf_counter()
    try:
        socket.getaddrinfo(host, None)
        return round((time.perf_counter() - start) * 1000, 1)
    except OSError:
        return None
