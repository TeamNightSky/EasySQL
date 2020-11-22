export BETTER_EXCEPTIONS=1

python -B examples.py

find . -name __pycache__ -exec rm -rf {} \;