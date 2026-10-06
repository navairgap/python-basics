# todo-cli

a json-backed todo list. stdlib only.

```bash
python3 todo.py add "write tests"
python3 todo.py ls            # open items
python3 todo.py ls -a         # everything, done included
python3 todo.py done 2
python3 todo.py undone 2
python3 todo.py rm 1
```

state lives in `todo.json` next to the script. it's json — diff it, back it
up, whatever. not cloud, not a startup, just a file.

run tests: `python3 -m unittest discover -s . -v`

items carry a `priority` field (default `normal`) in `todo.json` — set it by editing the file for now; cli support is on the roadmap.
