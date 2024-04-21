.PHONY: setup run

venv:
	python3 -m venv .gemini_venv

setup:
	source .gemini_venv/bin/activate
	pip install -r requirements.txt

run:
	source gemini_venv/bin/activate
	python run.py