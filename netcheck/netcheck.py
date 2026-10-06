#!/usr/bin/env python3
"""netcheck - small network diagnostics. stdlib only."""

import argparse
import socket
import sys
import time
import urllib.request

DEFAULT_TIMEOUT = 3
