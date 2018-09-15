#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

function questionY() {
	echo -e -n "[$COLOR_YELLOW""?""$COLOR_RESET] " $1 "[Y/n]? "
	read response
	case "$response" in
		[nN][oO]|[nN])
			false
			;;
		*)
			true
			;;
	esac
}

function install() {
  if questionY "Do you want to install it"
  then
    if ! [ -x "$(command -v apt-get)" ]; then
      echo "Error: apt-get does not exist."
      exit 1
    else
      sudo apt-get install $1
    fi
  else
    exit 1
  fi
}
function pipinstall() {
  if questionY "Do you want to install it"
  then
    if ! [ -x "$(pip3)" ]; then
      echo "Error: pip3 does not exist."
      exit 1
    else
      sudo pip3 install $1
    fi
  else
    exit 1
  fi
}

if ! [ -x "$(command -v python3)" ]; then
  echo 'Error: python3 is not installed.' >&2
  install python3
fi

if ! [ -x "$(command -v pip3)" ]; then
  echo 'Error: pip3 is not installed.' >&2
  echo 'Run: sudo apt-get install -y python3-pip' >&2
  install python3-pip
fi

if ! [ -x "$(command -v virtualenv)" ]; then
  echo 'Error: virtualenv is not installed.' >&2
  echo 'Run: sudo pip3 install virtualenv' >&2
  pipinstall virtualenv
fi


if [ -d "$DIR/venv" ]; then
  source $DIR/venv/bin/activate
else
  virtualenv -p python3 $DIR/venv
  source $DIR/venv/bin/activate
  pip install -r $DIR/requirements.txt
fi

python $DIR/github-sshkeys.py "$@"
deactivate
