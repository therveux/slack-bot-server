run:
	PYTHONPATH=src poetry run uvicorn slack_bot_server.main:app --reload

export-reqs:
	poetry export -f requirements.txt --without-hashes > requirements.txt