run:
	PYTHONPATH=src uvicorn slack_bot_server.main:app --host 0.0.0.0 --port 8000

dev:
	PYTHONPATH=src poetry run uvicorn slack_bot_server.main:app --reload

export-reqs:
	poetry export -f requirements.txt --without-hashes > requirements.txt