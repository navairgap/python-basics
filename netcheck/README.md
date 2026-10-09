# netcheck

small network diagnostics. stdlib only — `socket` + `urllib`.

```bash
python3 netcheck/netcheck.py port example.com 443   # tcp connect + latency
python3 netcheck/netcheck.py dns example.com        # resolve timing
python3 netcheck/netcheck.py http https://example.com
python3 netcheck/netcheck.py ip                     # local ip
```

exit codes: `0` success, `1` failure — scriptable in pipelines.

run tests: `python3 -m unittest discover -s netcheck -v`


## scanning several ports

`netcheck port host 443 80 22 -t 1` checks all three with a 1s timeout and exits non-zero if any is closed — made for health checks and pre-deploy smoke tests.
