# serveit

serve a directory over http. stdlib only — `http.server`.

```bash
python3 serveit/serveit.py ~/share          # http://127.0.0.1:8000
python3 serveit/serveit.py . -p 9000 -b 0.0.0.0 -q
```

`-q` silences the request log. binds localhost by default on purpose — pass
`-b 0.0.0.0` only on networks you trust.

run tests: `python3 -m unittest discover -s serveit -v`


## disabling listings

`--no-listing` returns 404 for directory requests while files still serve fine. Use it when sharing folders whose names you'd rather not advertise.
