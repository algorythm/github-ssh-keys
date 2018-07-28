from gitcred import Git
from logger import Logger
from pathlib import Path
import argparse
import json
import requests
from pycheck import is_supported_python
import sys

GITHUB_API = 'https://api.github.com'

SSH_FOLDER = Path.home() / ".ssh"
SSH_AUTHORIZED_KEYS_FILE = SSH_FOLDER / "authorized_keys"

###
### Fetches a user's public keys from GitHub
###
def fetch_public_keys(logger, username):
    url = GITHUB_API + "/users/" + username + "/keys"

    logger.log("Fetching public keys from GitHub...")

    req = requests.get(url)

    if req.status_code == 404:
        ### Unsupported in Python versions prior to Python 3.6
        # logger.log(f"Username {username} could not be found.")
        logger.log("Username %s could not be found" % username)
        return None

    return req.json()

###
### Ensures that .ssh folder and .authorized_keys file exists and both have
### the correct permissions
###
def ensure_authorized_keys_file(logger):
    if not SSH_FOLDER.is_dir():
        logger.log("\"~/.ssh\" folder does not exist yet. Creating folder with permission 700.")
        SSH_FOLDER.mkdir(mode=0o700)
    if not SSH_AUTHORIZED_KEYS_FILE.is_file():
        logger.log("\"~/.ssh/authorized_keys\" does not exist yet. Creating file with permission 600.")
        SSH_AUTHORIZED_KEYS_FILE.touch(mode=0o600)

###
### Reads ~/.ssh/authorized_keys and returns a list
###
def get_authorized_keys(logger):
    ensure_authorized_keys_file(logger)

    with open(str(SSH_AUTHORIZED_KEYS_FILE.resolve())) as authorized_keys:
        stored_keys = []
        for authorized_key in authorized_keys:
            if authorized_key.strip() != '':
                stored_keys.append(authorized_key.strip())

    return stored_keys

###
### Compares the list with local keys with the fetched keys from GitHub
### Return: a list of the new keys from GitHub that does not exist locally
###
def compare_key_lists(local_keys, github_keys):
    new_keys = []

    for key in github_keys:
        key = key["key"]
        if key.strip() not in local_keys:
            new_keys.append(key)

    return new_keys

def main():
    parser = argparse.ArgumentParser(description='Fetches SSH keys from GitHub. The program will find the username in ~/.gitconfig or ask for one, if that file does not exist. \n\nIMPORTANT: This program will override all existing keys saved in ~/.authorized_keys!')
    parser.add_argument('--silent', '-s', help='Will supress unnecessary terminal output. Note: the program will still ask the user for information if needed.', action="store_true")
    args = parser.parse_args()

    git = Git(Logger(args.silent))

    # Fetch all SSH keys from GitHub
    github_keys = fetch_public_keys(git.logger, git.username)

    if github_keys == None:
        git.logger.log("We failed to fetch SSH keys from GitHub.")
        sys.exit(-1)

    # Exit if the user have no keys on his GitHub account
    if len(github_keys) == 0:
        git.logger.log("You have no SSH keys saved on GitHub. Please save one and try again.")
        sys.exit(-1)

    # Ensure that ~/.ssh and ~/.ssh/authorized_keys exist
    ensure_authorized_keys_file(git.logger)
    # Retrieve all public keys from ~/.ssh/authorized_keys
    local_keys = get_authorized_keys(git.logger)
    # How many new keys?
    new_keys_count = len(compare_key_lists(local_keys, github_keys))

    # If there are new keys, save them in ~/.ssh/authorized_keys
    if new_keys_count > 0:
        with open(str(SSH_AUTHORIZED_KEYS_FILE.resolve()), 'w') as authorized_keys:
            for key in github_keys:
                authorized_keys.write(key["key"])
        
        git.logger.log(str(new_keys_count) + " new keys were added to " + str(SSH_AUTHORIZED_KEYS_FILE.resolve()), True)
    # Otherwise sys.exit
    else:
        git.logger.log("No keys were found.")
        sys.exit(0)

if __name__ == '__main__':
    main()