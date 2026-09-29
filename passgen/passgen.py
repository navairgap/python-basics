#!/usr/bin/env python3
"""passgen - a small password generator. stdlib only."""

import argparse
import secrets
import string

SETS = {
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "digits": string.digits,
    "symbols": "!@#$%^&*()-_=+[]{};:,.<>?",
}


AMBIGUOUS = set("l1IO0")


def generate(length=16, lower=True, upper=True, digits=True, symbols=True, count=1,
             no_ambiguous=False):
    pools = [chars for chars, on in (
        (SETS["lower"], lower), (SETS["upper"], upper),
        (SETS["digits"], digits), (SETS["symbols"], symbols),
    ) if on]
    if not pools:
        raise ValueError("at least one character set must be enabled")
    if length < len(pools):
        raise ValueError(f"length {length} too short for {len(pools)} character sets")

    alphabet = "".join(pools)
    if no_ambiguous:
        pools = ["".join(c for c in pool if c not in AMBIGUOUS) for pool in pools]
        pools = [pool for pool in pools if pool]
        if not pools:
            raise ValueError("no characters left after removing ambiguous ones")
        alphabet = "".join(pools)
    rng = secrets.SystemRandom()
    out = []
    for _ in range(count):
        chars = [secrets.choice(p) for p in pools]  # guarantee coverage
        chars += [secrets.choice(alphabet) for _ in range(length - len(pools))]
        rng.shuffle(chars)
        out.append("".join(chars))
    return out


def main():
    ap = argparse.ArgumentParser(description="generate passwords")
    ap.add_argument("-l", "--length", type=int, default=16)
    ap.add_argument("-n", "--count", type=int, default=1)
    ap.add_argument("--no-lower", action="store_true")
    ap.add_argument("--no-upper", action="store_true")
    ap.add_argument("--no-digits", action="store_true")
    ap.add_argument("--no-symbols", action="store_true")
    a = ap.parse_args()
    try:
        for pwd in generate(a.length, not a.no_lower, not a.no_upper,
                            not a.no_digits, not a.no_symbols, a.count,
                            a.no_ambiguous):
            print(pwd)
    except ValueError as e:
        ap.error(str(e))


if __name__ == "__main__":
    main()
