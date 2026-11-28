.PHONY: install demo test

install:
	pip install -r requirements.txt

demo:
	python3 run_all.py

test:
	pytest -v src/test_suite.py