#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

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
  source $DIR/venv/bin/activate
else
  virtualenv -p python3 $DIR/venv
  source $DIR/venv/bin/activate
  pip install -r $DIR/requirements.txt
fi

python $DIR/github-sshkeys.py "$@"
deactivate
