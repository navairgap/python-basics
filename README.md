# python-projects

small python projects. stdlib only — no pip, no venv drama, no dependencies
that rot. learning in public.

## projects

| dir          | what                          | run it                        |
| ------------ | ----------------------------- | ----------------------------- |
| `passgen/`    | password generator (secrets)   | `python3 passgen/passgen.py`   |
| `todo-cli/`   | json-backed todo list          | `python3 todo-cli/todo.py ls`  |
| `weather-cli/`| weather via wttr.in            | `python3 weather-cli/weather.py pune` |
| `disk-audit/` | disk usage analyzer           | `python3 disk-audit/audit.py ~/Downloads` |
| `netcheck/`   | network diagnostics           | `python3 netcheck/netcheck.py port example.com 443` |
| `serveit/`    | static file server            | `python3 serveit/serveit.py ~/share` |

## rules i hold myself to

- standard library only, python 3.9+
- every project has tests (`python3 -m unittest discover -s .`) and they pass
- every project has a readme that fits in one screen
- small is the point. boring is a feature.

---
maintained · verified 2026-09-30
---
maintained · verified 2026-10-01
---
maintained · verified 2026-10-02

## Why stdlib only

Every project here runs on a fresh Python install with zero pip installs. It's a constraint on purpose: when you can't reach for a dependency, you learn what the standard library already does well — `secrets`, `json`, `urllib`, `argparse`.
