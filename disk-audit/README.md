# disk-audit

find what's eating your disk. stdlib only — `os.scandir` does the heavy lifting.

```bash
python3 disk-audit/audit.py ~/Downloads          # top 15 directories
python3 disk-audit/audit.py / -n 25 --min-size 1G
python3 disk-audit/audit.py ~ --exclude node_modules --json
```

## how it works

1. walks the tree with `os.scandir` (never follows symlinks — no loops)
2. aggregates sizes and file counts up through parent directories
3. renders a text bar chart of the top-N offenders
4. `--json` emits machine-readable output for pipes and scripts

skips `.git`, `node_modules`, `__pycache__`, `.cache` by default; override with `--exclude`.

run tests: `python3 -m unittest discover -s disk-audit -v`

`--csv out.csv` writes the top-N rows to a csv file (path,size_bytes,files) for spreadsheets and further tooling.
