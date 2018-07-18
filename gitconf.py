import requests
import getpass
import json
import argparse

from pathlib import Path

GITHUB_API = 'https://api.github.com'
SILENT = False

def get_username():
    gitconf = Path(Path.home() / ".gitconfig")

    if gitconf.exists():
        with open(gitconf) as file:
            for line in file:
                line = line.rstrip().strip()
                if line.startswith("name"):
                    username = line.replace("name", "").replace("=","").strip()
    else:
        if (not SILENT):
            print("No gitconfig was found on the system")

    try:
        username
    except NameError:
        print("We could not find any git username on your system.")
        username = input("Git username: ")
    finally:
        if not SILENT:
            print("Using git username:", username)

    return username

def fetch_public_keys(username):
    url = GITHUB_API + "/users/" + username + "/keys"
    req = requests.get(url)

    if req.status_code == 404:
        print("Username '", username, "' could not be found.", sep="")
        return None
    # elif req.status_code == 401:
    #     print("Username or password is incorrect, try again.")
    #     return None
    return req.json()

def get_list_of_public_keys():
    username = get_username()

    if not SILENT:
        print("Will now fetch your public keys from GitHub...")

    keys = fetch_public_keys(username)

    if keys == None:
        exit(-1)

    if len(keys) == 0:
        if not SILENT:
            print("You have no SSH keys saved on GitHub. Please save one and try again.")
        exit(-1)

    key_list = []
    for key in keys:
        key_list.append(key["key"])

    return key_list

def write_keys():
    keys = get_list_of_public_keys()

    ssh_folder = Path.home() / ".ssh"
    ssh_authorized_file = ssh_folder / "authorized_keys"

    if not ssh_folder.is_dir():
        if not SILENT:
            print(ssh_folder.resolve(), "does not exist yet. Creating folder with permission 700.")
        ssh_folder.mkdir(mode=0o700)
    if not ssh_authorized_file.is_file():
        if not SILENT:
            print(ssh_authorized_file, "does not exist yet. Creating file with permission 600.")
        ssh_authorized_file.touch(mode=0o600)

    with open(ssh_authorized_file) as authorized_keys:
        stored_keys = []
        for authorized_key in authorized_keys:
            if authorized_key.strip() != '':
                stored_keys.append(authorized_key.strip())

    if not SILENT:
        print()

    new_keys = []

    for key in keys:
        if key.strip() not in stored_keys:
            new_keys.append(key)

    if len(new_keys) > 0:
        if not SILENT:
            print("We found", len(new_keys), "new public keys.")

        with open(ssh_authorized_file, 'w') as authorized_keys:
            for key in keys:
                authorized_keys.write(key)
    else:
        if not SILENT:
            print("No new keys were found.")
        exit(0)

def main():
    parser = argparse.ArgumentParser(description='Fetches SSH keys from GitHub. The program will find the username in ~/.gitconfig or ask for one, if that file does not exist. \n\nIMPORTANT: This program will override all existing keys saved in ~/.authorized_keys!')
    parser.add_argument('--silent', '-s', help='Will supress unnecessary terminal output. Note: the program will still ask the user for information if needed.', action="store_true")
    args = parser.parse_args()

    SILENT = True if args.silent else False

    write_keys()

if __name__ == '__main__':
    main()