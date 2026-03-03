.PHONY: test install clean run lint help

help:
	@echo "Kelvin Capital - Available Commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run all unit tests"
	@echo "  make run        - Run the trading bot"
	@echo "  make lint       - Run code linting"
	@echo "  make clean      - Remove build artifacts"
	@echo "  make scan       - Quick market scan"

install:
	pip install -r requirements.txt
	pip install -e .

test:
	python -m unittest discover tests/ -v

run:
	python run_bot.py

lint:
	python -m pylint src/ --disable=C0111
	python -m flake8 src/ --max-line-length=100

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache

scan:
	python -c "from src.scanner import CSPScanner; s = CSPScanner('', ''); print('Scanner loaded successfully')"
