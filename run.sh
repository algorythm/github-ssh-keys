#!/usr/bin/env bash

if ! [ -x "$(command -v python3)" ]; then
  echo 'Error: python3 is not installed.' >&2
  exit 1
fi

if ! [ -x "$(command -v pip)" ]; then
  echo 'Error: pip is not installed.' >&2
  exit 1
fi

if ! [ -x "$(command -v virtualenv)" ]; then
  echo 'Error: virtualenv is not installed.' >&2
  exit 1
fi


if [ -d "venv" ]; then
  source venv/bin/activate
else
  virtualenv -p python3 venv
  source venv/bin/activate
  pip install -r requirements.txt
fi

python github-sshkeys.py "$@"
deactivate
