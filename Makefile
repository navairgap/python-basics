PY ?= python3

.PHONY: test run-%

test:
	$(PY) -m unittest discover -s passgen -v
	$(PY) -m unittest discover -s todo-cli -v
	$(PY) -m unittest discover -s weather-cli -v

run-passgen:
	$(PY) passgen/passgen.py

run-todo:
	$(PY) todo-cli/todo.py ls -a

run-weather:
	$(PY) weather-cli/weather.py
