import argparse

import subprocess as sub

from pathlib import Path
from logger import Logger

class Git:
    def __init__(self, logger, username = None):
        self.logger = logger
        self.username = username

        if self.username == None:
            self.username = self.find_username()


    @staticmethod
    def username_from_gitconfig():
        gitconfig = Path(Path.home() / ".gitconfig")

        if gitconfig.exists():
            with open(gitconfig) as config_file:
                for line in config_file:
                    line = line.rstrip().strip()
                    if line.startswith("name"):
                        return line.replace("name", "").replace("=", "").strip()
        
        return None

    def find_username(self):
        username_gitconfig = Git.username_from_gitconfig()
        username = username_gitconfig

        if username == None:
            self.logger.log("We failed to find a git username in your ~/.gitconfig", important=True)
            username = self.logger.ask("Username:")

        self.logger.log("Using git username: " + username)

        if not self.logger.silent and username_gitconfig == None:
            choice = self.logger.ask_yn("Do you want to save '" + username + "' in your ~/.gitconfig?")
            if choice:
                sub.Popen(['git', 'config', '--global', 'user.name', username])
        
        return username

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--silent', '-s', action="store_true")
    args = parser.parse_args()

    Git(Logger(args.silent))

if __name__ == '__main__':
    main()