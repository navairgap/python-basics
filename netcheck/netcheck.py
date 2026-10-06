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

def http_status(url, timeout=DEFAULT_TIMEOUT):
    """HEAD a url, return status code or None."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except OSError:
        return None

def local_ip():
    """best-effort local IP without sending any packets."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()

def main():
    ap = argparse.ArgumentParser(prog="netcheck", description="small network diagnostics")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("port"); p.add_argument("host"); p.add_argument("port", type=int)
    p = sub.add_parser("dns"); p.add_argument("host")
    p = sub.add_parser("http"); p.add_argument("url")
    sub.add_parser("ip")
    a = ap.parse_args()

    if a.cmd == "port":
        ok, ms = check_port(a.host, a.port)
        if ok:
            print(f"{a.host}:{a.port} open ({ms}ms)")
        else:
            print(f"{a.host}:{a.port} closed or filtered")

    elif a.cmd == "dns":
        ms = dns_time(a.host)
        print(f"{a.host} resolves in {ms}ms" if ms is not None else f"{a.host} does not resolve")

    elif a.cmd == "http":
        code = http_status(a.url)
        print(f"{a.url} -> {code}" if code else f"{a.url} unreachable")

    elif a.cmd == "ip":
        print(local_ip())


if __name__ == "__main__":
    main()
