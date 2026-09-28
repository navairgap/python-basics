# passgen

small password generator. stdlib only — no pip install, no excuses.

```bash
python3 passgen.py              # one 16-char password
python3 passgen.py -l 24 -n 5   # five 24-char passwords
python3 passgen.py --no-symbols # letters + digits only
```

uses `secrets`, guarantees at least one character from every selected set,
shuffles so the first chars aren't predictable.

run tests: `python3 -m unittest discover -s . -v`
