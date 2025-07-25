#!/bin/sh

changed_files=$(git diff --cached --name-only)

if echo "$changed_files" | grep -qE '^(pyproject.toml|poetry.lock)$'; then
  echo "⚠️  pyproject.toml or poetry.lock has changed."
  echo "Regenerating requirements.txt..."
  make export-deps

  if ! git diff --quiet requirements.txt; then
    echo "requirements.txt has been updated but not staged."
    echo "Please add requirements.txt to the commit and try again."
    exit 1
  fi

  if ! git diff --cached --quiet requirements.txt; then
    echo "requirements.txt is staged and ready."
    echo "Proceeding with commit."
  else
    echo "requirements.txt changes are not staged."
    echo "Please stage requirements.txt and try again."
    exit 1
  fi
fi

exit 0