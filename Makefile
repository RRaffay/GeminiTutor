.PHONY: setup run

venv:
	python3 -m venv .venv

setup:
	source .venv/bin/activate
	pip install -r requirements.txt

run:
	source .venv/bin/activate
	python run.py