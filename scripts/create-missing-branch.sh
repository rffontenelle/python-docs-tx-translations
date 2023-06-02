#!/bin/sh
# Receives a branch name as input and creates it if missing

if [ $# -ne 1 ]; then
  echo "A branch name as argument is required."
  exit 1
fi

if ! git show-branch $1 2>/dev/null; then
  git branch $1
  echo "$1 created"
fi
